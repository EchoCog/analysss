#!/usr/bin/env python3
"""
Unit tests for HyperGraphQL Schema
===================================
"""

import pytest
from datetime import datetime
from src.api.hypergraphql_schema import (
    EntityTypeQL,
    HyperGraphQLEdge,
    HyperGraphQLNode,
    HyperGraphQLOrgMapping,
    HyperGraphQLSchema,
    OrgLevel,
    RelationTypeQL,
)


class TestHyperGraphQLNode:
    """Test HyperGraphQLNode dataclass"""
    
    def test_node_creation(self):
        """Test creating a node"""
        node = HyperGraphQLNode(
            id="test_node_1",
            node_type=EntityTypeQL.PERSON,
            name="Test Person",
            properties={"age": 30},
            org_level=OrgLevel.REPO
        )
        
        assert node.id == "test_node_1"
        assert node.node_type == EntityTypeQL.PERSON
        assert node.name == "Test Person"
        assert node.properties["age"] == 30
        assert node.org_level == OrgLevel.REPO
        
    def test_node_to_graphql_type(self):
        """Test converting node to GraphQL type"""
        node = HyperGraphQLNode(
            id="test_node_1",
            node_type=EntityTypeQL.PERSON,
            name="Test Person",
            properties={"age": 30},
            org_level=OrgLevel.REPO,
            repo_path="/path/to/repo"
        )
        
        gql_type = node.to_graphql_type()
        
        assert gql_type["id"] == "test_node_1"
        assert gql_type["nodeType"] == "person"
        assert gql_type["name"] == "Test Person"
        assert gql_type["properties"]["age"] == 30
        assert gql_type["orgLevel"] == "repo"
        assert gql_type["repoPath"] == "/path/to/repo"


class TestHyperGraphQLEdge:
    """Test HyperGraphQLEdge dataclass"""
    
    def test_edge_creation(self):
        """Test creating an edge"""
        edge = HyperGraphQLEdge(
            id="test_edge_1",
            edge_type=RelationTypeQL.OWNS,
            source_id="node_1",
            target_ids=["node_2", "node_3"],
            strength=0.8
        )
        
        assert edge.id == "test_edge_1"
        assert edge.edge_type == RelationTypeQL.OWNS
        assert edge.source_id == "node_1"
        assert len(edge.target_ids) == 2
        assert edge.strength == 0.8
        
    def test_edge_to_graphql_type(self):
        """Test converting edge to GraphQL type"""
        timestamp = datetime.now()
        edge = HyperGraphQLEdge(
            id="test_edge_1",
            edge_type=RelationTypeQL.OWNS,
            source_id="node_1",
            target_ids=["node_2"],
            strength=0.8,
            timestamp=timestamp
        )
        
        gql_type = edge.to_graphql_type()
        
        assert gql_type["id"] == "test_edge_1"
        assert gql_type["edgeType"] == "owns"
        assert gql_type["sourceId"] == "node_1"
        assert gql_type["targetIds"] == ["node_2"]
        assert gql_type["strength"] == 0.8
        assert gql_type["timestamp"] == timestamp.isoformat()


class TestHyperGraphQLSchema:
    """Test HyperGraphQLSchema class"""
    
    @pytest.fixture
    def schema(self):
        """Create a test schema"""
        return HyperGraphQLSchema()
        
    @pytest.fixture
    def sample_nodes(self):
        """Create sample nodes"""
        return [
            HyperGraphQLNode(
                id="person_1",
                node_type=EntityTypeQL.PERSON,
                name="Alice",
                org_level=OrgLevel.REPO
            ),
            HyperGraphQLNode(
                id="person_2",
                node_type=EntityTypeQL.PERSON,
                name="Bob",
                org_level=OrgLevel.REPO
            ),
            HyperGraphQLNode(
                id="org_1",
                node_type=EntityTypeQL.ORGANIZATION,
                name="Company A",
                org_level=OrgLevel.ORG
            )
        ]
        
    @pytest.fixture
    def sample_edges(self):
        """Create sample edges"""
        return [
            HyperGraphQLEdge(
                id="edge_1",
                edge_type=RelationTypeQL.MEMBER_OF,
                source_id="person_1",
                target_ids=["org_1"],
                strength=0.9
            ),
            HyperGraphQLEdge(
                id="edge_2",
                edge_type=RelationTypeQL.COMMUNICATES_WITH,
                source_id="person_1",
                target_ids=["person_2"],
                strength=0.7
            )
        ]
        
    def test_add_node(self, schema, sample_nodes):
        """Test adding nodes to schema"""
        for node in sample_nodes:
            schema.add_node(node)
            
        assert len(schema.nodes) == 3
        assert "person_1" in schema.nodes
        assert "person_2" in schema.nodes
        assert "org_1" in schema.nodes
        
    def test_add_edge(self, schema, sample_edges):
        """Test adding edges to schema"""
        for edge in sample_edges:
            schema.add_edge(edge)
            
        assert len(schema.edges) == 2
        assert "edge_1" in schema.edges
        assert "edge_2" in schema.edges
        
    def test_get_node(self, schema, sample_nodes):
        """Test retrieving a node"""
        schema.add_node(sample_nodes[0])
        
        node = schema.get_node("person_1")
        assert node is not None
        assert node.name == "Alice"
        
        missing_node = schema.get_node("nonexistent")
        assert missing_node is None
        
    def test_get_nodes_by_type(self, schema, sample_nodes):
        """Test filtering nodes by type"""
        for node in sample_nodes:
            schema.add_node(node)
            
        person_nodes = schema.get_nodes_by_type(EntityTypeQL.PERSON)
        assert len(person_nodes) == 2
        
        org_nodes = schema.get_nodes_by_type(EntityTypeQL.ORGANIZATION)
        assert len(org_nodes) == 1
        
    def test_get_nodes_by_org_level(self, schema, sample_nodes):
        """Test filtering nodes by org level"""
        for node in sample_nodes:
            schema.add_node(node)
            
        repo_nodes = schema.get_nodes_by_type(EntityTypeQL.PERSON, OrgLevel.REPO)
        assert len(repo_nodes) == 2
        
        org_level_nodes = schema.get_nodes_by_type(EntityTypeQL.ORGANIZATION, OrgLevel.ORG)
        assert len(org_level_nodes) == 1
        
    def test_get_connected_nodes(self, schema, sample_nodes, sample_edges):
        """Test finding connected nodes"""
        for node in sample_nodes:
            schema.add_node(node)
        for edge in sample_edges:
            schema.add_edge(edge)
            
        connected = schema.get_connected_nodes("person_1")
        connected_ids = [n.id for n in connected]
        
        assert "org_1" in connected_ids
        assert "person_2" in connected_ids
        
    def test_export_schema(self, schema, sample_nodes, sample_edges):
        """Test exporting schema"""
        for node in sample_nodes:
            schema.add_node(node)
        for edge in sample_edges:
            schema.add_edge(edge)
            
        exported = schema.export_schema()
        
        assert "nodes" in exported
        assert "edges" in exported
        assert "metadata" in exported
        assert len(exported["nodes"]) == 3
        assert len(exported["edges"]) == 2
        assert exported["metadata"]["nodeCount"] == 3
        assert exported["metadata"]["edgeCount"] == 2
        
    def test_export_schema_with_org_level_filter(self, schema, sample_nodes):
        """Test exporting schema filtered by org level"""
        for node in sample_nodes:
            schema.add_node(node)
            
        exported = schema.export_schema(OrgLevel.REPO)
        
        assert len(exported["nodes"]) == 2  # Only REPO level nodes
        
    def test_add_org_mapping(self, schema):
        """Test adding org mapping"""
        mapping = HyperGraphQLOrgMapping(
            org_name="test-org",
            org_level=OrgLevel.ORG,
            repos=["repo1", "repo2"],
            entity_folders=["entities/persons", "entities/orgs"],
            compression_enabled=True
        )
        
        schema.add_org_mapping(mapping)
        
        assert "test-org" in schema.org_mappings
        assert schema.org_mappings["test-org"].compression_enabled


class TestGraphQLSchemaDefinition:
    """Test GraphQL schema definition generation"""
    
    def test_get_graphql_schema_definition(self):
        """Test generating GraphQL schema definition"""
        schema = HyperGraphQLSchema()
        definition = schema.get_graphql_schema_definition()
        
        # Check for key types
        assert "type HyperGraphQLNode" in definition
        assert "type HyperGraphQLEdge" in definition
        assert "type HyperGraphQLOrgMapping" in definition
        assert "type Query" in definition
        assert "type Mutation" in definition
        
        # Check for key fields
        assert "nodeType: String!" in definition
        assert "edgeType: String!" in definition
        assert "orgLevel: String!" in definition
        
        # Check for scalars
        assert "scalar JSON" in definition
        assert "scalar DateTime" in definition
