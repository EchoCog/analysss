#!/usr/bin/env python3
"""
HyperGraphQL API Endpoints
============================

Flask-based REST and GraphQL API endpoints for HyperGraphQL functionality.
Provides:
- GraphQL query endpoint
- REST endpoints for GitHub repo management
- Org-aware operations
- Scaling and compression utilities
"""

import json
import logging
from typing import Any, Dict, Optional

from flask import Blueprint, jsonify, request

from .hypergraphql_github import GitHubRepoProjection, OrgAwareManager
from .hypergraphql_resolvers import HyperGraphQLResolver
from .hypergraphql_schema import HyperGraphQLSchema, OrgLevel

logger = logging.getLogger(__name__)

# Create Blueprint for HyperGraphQL endpoints
hypergraphql_bp = Blueprint("hypergraphql", __name__, url_prefix="/api/v1/hypergraphql")

# Global instances (in production, these should be properly managed)
_schema = HyperGraphQLSchema()
_resolver = HyperGraphQLResolver(_schema)
_org_managers: Dict[str, OrgAwareManager] = {}


@hypergraphql_bp.route("/schema", methods=["GET"])
def get_schema_definition():
    """Get the GraphQL schema definition"""
    try:
        schema_def = _schema.get_graphql_schema_definition()
        return jsonify({"success": True, "schema": schema_def})
    except Exception as e:
        logger.error(f"Error getting schema definition: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/query", methods=["POST"])
def graphql_query():
    """
    Execute a GraphQL query.

    Request body:
    {
        "query": "query { nodes { id name } }",
        "variables": {}
    }
    """
    try:
        data = request.get_json()
        query = data.get("query", "")
        variables = data.get("variables", {})

        # Simple query parsing and routing
        # In production, use a proper GraphQL library like graphene or strawberry
        result = _execute_query(query, variables)

        return jsonify({"success": True, "data": result})
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


def _execute_query(query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simple query executor (proof of concept).
    In production, use a proper GraphQL library.
    """
    # Parse query type from string (simplified)
    query_lower = query.lower()

    if "node(" in query_lower:
        node_id = variables.get("id") or _extract_id_from_query(query, "node")
        return {"node": _resolver.resolve_node(node_id)}

    elif "nodes" in query_lower:
        node_type = variables.get("nodeType")
        org_level = variables.get("orgLevel")
        return {"nodes": _resolver.resolve_nodes(node_type, org_level)}

    elif "edge(" in query_lower:
        edge_id = variables.get("id") or _extract_id_from_query(query, "edge")
        return {"edge": _resolver.resolve_edge(edge_id)}

    elif "edges" in query_lower:
        edge_type = variables.get("edgeType")
        org_level = variables.get("orgLevel")
        return {"edges": _resolver.resolve_edges(edge_type, org_level)}

    elif "connectedNodes" in query_lower or "connectednodes" in query_lower:
        node_id = variables.get("nodeId") or _extract_id_from_query(
            query, "connectedNodes"
        )
        return {"connectedNodes": _resolver.resolve_connected_nodes(node_id)}

    elif "exportSchema" in query_lower or "exportschema" in query_lower:
        org_level = variables.get("orgLevel")
        return {"exportSchema": _resolver.resolve_export_schema(org_level)}

    else:
        return {"error": "Unsupported query"}


def _extract_id_from_query(query: str, field: str) -> Optional[str]:
    """Extract ID parameter from query string (simplified)"""
    try:
        start = query.find(f"{field}(")
        if start == -1:
            return None
        start = query.find("id:", start) + 3
        end = query.find(")", start)
        id_str = query[start:end].strip().strip("\"'")
        return id_str
    except Exception:
        return None


@hypergraphql_bp.route("/nodes", methods=["GET"])
def get_nodes():
    """REST endpoint to get nodes with filtering"""
    try:
        node_type = request.args.get("type")
        org_level = request.args.get("orgLevel")

        nodes = _resolver.resolve_nodes(node_type, org_level)

        return jsonify({"success": True, "count": len(nodes), "nodes": nodes})
    except Exception as e:
        logger.error(f"Error getting nodes: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/nodes/<node_id>", methods=["GET"])
def get_node(node_id: str):
    """REST endpoint to get a specific node"""
    try:
        node = _resolver.resolve_node(node_id)

        if not node:
            return jsonify({"success": False, "error": "Node not found"}), 404

        return jsonify({"success": True, "node": node})
    except Exception as e:
        logger.error(f"Error getting node: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/nodes", methods=["POST"])
def create_node():
    """REST endpoint to create a node"""
    try:
        data = request.get_json()
        node = _resolver.resolve_add_node(data)

        return jsonify({"success": True, "node": node}), 201
    except Exception as e:
        logger.error(f"Error creating node: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/edges", methods=["GET"])
def get_edges():
    """REST endpoint to get edges with filtering"""
    try:
        edge_type = request.args.get("type")
        org_level = request.args.get("orgLevel")

        edges = _resolver.resolve_edges(edge_type, org_level)

        return jsonify({"success": True, "count": len(edges), "edges": edges})
    except Exception as e:
        logger.error(f"Error getting edges: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/edges/<edge_id>", methods=["GET"])
def get_edge(edge_id: str):
    """REST endpoint to get a specific edge"""
    try:
        edge = _resolver.resolve_edge(edge_id)

        if not edge:
            return jsonify({"success": False, "error": "Edge not found"}), 404

        return jsonify({"success": True, "edge": edge})
    except Exception as e:
        logger.error(f"Error getting edge: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/edges", methods=["POST"])
def create_edge():
    """REST endpoint to create an edge"""
    try:
        data = request.get_json()
        edge = _resolver.resolve_add_edge(data)

        return jsonify({"success": True, "edge": edge}), 201
    except Exception as e:
        logger.error(f"Error creating edge: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/github/repo/init", methods=["POST"])
def init_repo_structure():
    """
    Initialize GitHub repo structure for entities and relations.

    Request body:
    {
        "repoPath": "/path/to/repo"
    }
    """
    try:
        data = request.get_json()
        repo_path = data.get("repoPath")

        if not repo_path:
            return jsonify({"success": False, "error": "repoPath is required"}), 400

        projection = GitHubRepoProjection(repo_path)
        projection.initialize_repo_structure()

        stats = projection.get_repo_stats()

        return jsonify(
            {"success": True, "message": "Repo structure initialized", "stats": stats}
        )
    except Exception as e:
        logger.error(f"Error initializing repo structure: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/github/repo/project", methods=["POST"])
def project_schema_to_repo():
    """
    Project current schema to GitHub repo structure.

    Request body:
    {
        "repoPath": "/path/to/repo"
    }
    """
    try:
        data = request.get_json()
        repo_path = data.get("repoPath")

        if not repo_path:
            return jsonify({"success": False, "error": "repoPath is required"}), 400

        projection = GitHubRepoProjection(repo_path)
        projection.project_schema(_schema)

        stats = projection.get_repo_stats()

        return jsonify(
            {"success": True, "message": "Schema projected to repo", "stats": stats}
        )
    except Exception as e:
        logger.error(f"Error projecting schema: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/github/repo/load", methods=["POST"])
def load_from_repo():
    """
    Load entities and relations from GitHub repo structure.

    Request body:
    {
        "repoPath": "/path/to/repo",
        "orgName": "organization-name"
    }
    """
    try:
        data = request.get_json()
        repo_path = data.get("repoPath")
        org_name = data.get("orgName", "default-org")

        if not repo_path:
            return jsonify({"success": False, "error": "repoPath is required"}), 400

        _resolver.load_from_repo_structure(repo_path, org_name)

        return jsonify(
            {
                "success": True,
                "message": "Data loaded from repo",
                "nodeCount": len(_schema.nodes),
                "edgeCount": len(_schema.edges),
            }
        )
    except Exception as e:
        logger.error(f"Error loading from repo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/github/org/register", methods=["POST"])
def register_org():
    """
    Register an organization for multi-repo management.

    Request body:
    {
        "orgName": "org-name",
        "orgLevel": "ORG" | "ENTERPRISE"
    }
    """
    try:
        data = request.get_json()
        org_name = data.get("orgName")
        org_level_str = data.get("orgLevel", "ORG")

        if not org_name:
            return jsonify({"success": False, "error": "orgName is required"}), 400

        org_level = OrgLevel[org_level_str.upper()]
        manager = OrgAwareManager(org_name, org_level)
        _org_managers[org_name] = manager

        return jsonify(
            {
                "success": True,
                "message": f"Organization {org_name} registered",
                "orgLevel": org_level.value,
            }
        )
    except Exception as e:
        logger.error(f"Error registering org: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/github/org/<org_name>/repos", methods=["POST"])
def register_repo_to_org(org_name: str):
    """
    Register a repo to an organization.

    Request body:
    {
        "repoName": "repo-name",
        "repoPath": "/path/to/repo"
    }
    """
    try:
        if org_name not in _org_managers:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Organization {org_name} not registered",
                    }
                ),
                404,
            )

        data = request.get_json()
        repo_name = data.get("repoName")
        repo_path = data.get("repoPath")

        if not repo_name or not repo_path:
            return (
                jsonify(
                    {"success": False, "error": "repoName and repoPath are required"}
                ),
                400,
            )

        manager = _org_managers[org_name]
        manager.register_repo(repo_name, repo_path)

        return jsonify(
            {"success": True, "message": f"Repo {repo_name} registered to {org_name}"}
        )
    except Exception as e:
        logger.error(f"Error registering repo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/github/org/<org_name>/aggregate", methods=["POST"])
def aggregate_org_schemas(org_name: str):
    """Aggregate schemas from all repos in an organization"""
    try:
        if org_name not in _org_managers:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Organization {org_name} not registered",
                    }
                ),
                404,
            )

        manager = _org_managers[org_name]
        aggregated_schema = manager.aggregate_schemas()

        return jsonify(
            {
                "success": True,
                "message": f"Schemas aggregated for {org_name}",
                "nodeCount": len(aggregated_schema.nodes),
                "edgeCount": len(aggregated_schema.edges),
                "repoCount": len(manager.repos),
            }
        )
    except Exception as e:
        logger.error(f"Error aggregating schemas: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/github/org/<org_name>/stats", methods=["GET"])
def get_org_stats(org_name: str):
    """Get statistics for an organization"""
    try:
        if org_name not in _org_managers:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Organization {org_name} not registered",
                    }
                ),
                404,
            )

        manager = _org_managers[org_name]
        stats = manager.get_org_stats()

        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        logger.error(f"Error getting org stats: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/github/repo/compress", methods=["POST"])
def compress_repo():
    """
    Compress a repo for storage.

    Request body:
    {
        "orgName": "org-name",
        "repoName": "repo-name",
        "outputPath": "/path/to/output"
    }
    """
    try:
        data = request.get_json()
        org_name = data.get("orgName")
        repo_name = data.get("repoName")
        output_path = data.get("outputPath")

        if not all([org_name, repo_name, output_path]):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "orgName, repoName, and outputPath are required",
                    }
                ),
                400,
            )

        if org_name not in _org_managers:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Organization {org_name} not registered",
                    }
                ),
                404,
            )

        manager = _org_managers[org_name]
        archive_path = manager.compress_repo(repo_name, output_path)

        return jsonify(
            {
                "success": True,
                "message": f"Repo {repo_name} compressed",
                "archivePath": str(archive_path),
            }
        )
    except Exception as e:
        logger.error(f"Error compressing repo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/export", methods=["GET"])
def export_schema():
    """Export the current schema"""
    try:
        org_level = request.args.get("orgLevel")
        exported = _resolver.resolve_export_schema(org_level)

        return jsonify({"success": True, "schema": exported})
    except Exception as e:
        logger.error(f"Error exporting schema: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# HGNNQL Integration Endpoints
@hypergraphql_bp.route("/hgnnql/query", methods=["POST"])
def execute_hgnnql():
    """
    Execute a HGNNQL query.

    Request body:
    {
        "query": "FIND ENTITY",
        "case_id": "case_001"
    }
    """
    try:
        from frameworks.opencog_hgnnql import AtomSpace, HGNNQLQueryEngine

        data = request.get_json()
        query = data.get("query")
        case_id = data.get("case_id", "default_case")

        if not query:
            return jsonify({"success": False, "error": "query is required"}), 400

        # For now, create a temporary atomspace
        # In production, this should be managed globally
        atomspace = AtomSpace(case_id)
        query_engine = HGNNQLQueryEngine(atomspace)

        result = query_engine.execute_hgnnql(query)

        return jsonify(
            {"success": True, "query": query, "case_id": case_id, "result": result}
        )
    except Exception as e:
        logger.error(f"Error executing HGNNQL query: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/hgnnql/atomspace/<case_id>/atoms", methods=["GET"])
def get_atomspace_atoms(case_id: str):
    """Get all atoms in an atomspace for a specific case"""
    try:
        # This is a simplified implementation
        # In production, you'd maintain active atomspaces
        return jsonify(
            {
                "success": True,
                "case_id": case_id,
                "message": "This endpoint would return atoms for the specified case",
                "atoms": [],
            }
        )
    except Exception as e:
        logger.error(f"Error getting atomspace atoms: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@hypergraphql_bp.route("/hgnnql/convert/hypergnn", methods=["POST"])
def convert_hypergnn_to_hgnnql():
    """
    Convert HyperGNN framework data to HGNNQL AtomSpace.

    Request body:
    {
        "case_id": "case_001",
        "hypergnn_data": {...}
    }
    """
    try:
        from frameworks.opencog_hgnnql import Atom, AtomSpace, AtomType, TruthValue

        data = request.get_json()
        case_id = data.get("case_id")
        hypergnn_data = data.get("hypergnn_data", {})

        if not case_id:
            return jsonify({"success": False, "error": "case_id is required"}), 400

        # Create atomspace and convert data
        atomspace = AtomSpace(case_id)

        # Convert agents to entities
        agents = hypergnn_data.get("agents", {})
        for agent_id, agent_data in agents.items():
            atom = Atom(
                atom_id=agent_id,
                atom_type=AtomType.ENTITY,
                name=agent_data.get("name", agent_id),
                truth_value=TruthValue(0.8, 0.9),
                metadata=agent_data,
            )
            atomspace.add_atom(atom)

        # Convert events
        events = hypergnn_data.get("events", {})
        for event_id, event_data in events.items():
            atom = Atom(
                atom_id=event_id,
                atom_type=AtomType.EVENT,
                name=event_data.get("description", event_id),
                truth_value=TruthValue(0.7, 0.8),
                metadata=event_data,
            )
            atomspace.add_atom(atom)

        return jsonify(
            {
                "success": True,
                "case_id": case_id,
                "atoms_created": len(atomspace.atoms),
                "message": "HyperGNN data converted to HGNNQL AtomSpace",
            }
        )
    except Exception as e:
        logger.error(f"Error converting HyperGNN to HGNNQL: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# Helper function to get resolver instance
def get_resolver() -> HyperGraphQLResolver:
    """Get the global resolver instance"""
    return _resolver


# Helper function to get schema instance
def get_schema() -> HyperGraphQLSchema:
    """Get the global schema instance"""
    return _schema
