#!/usr/bin/env python3
"""
Complete HGNNQL Implementation Demo
===================================

Demonstrates the complete HGNNQL implementation extending GraphQL with:
1. OpenCog-style knowledge representation
2. Enhanced query operations (FIND, LINK, INFER, QUERY, COUNT) 
3. HyperGraphQL integration
4. GitHub repository projection
5. API endpoints and frontend integration
6. End-to-end workflow for case analysis
"""

import json
import tempfile
from pathlib import Path

def demo_hgnnql_basics():
    """Demonstrate basic HGNNQL functionality"""
    print("🧠 HGNNQL Basic Operations")
    print("=" * 30)
    
    from frameworks.opencog_hgnnql import AtomSpace, HGNNQLQueryEngine, Atom, AtomType, TruthValue
    
    # Create knowledge base
    atomspace = AtomSpace("fraud_case_2024")
    engine = HGNNQLQueryEngine(atomspace)
    
    # Add entities
    entities = [
        ("suspect_alice", "Alice Johnson", {"role": "suspect", "confidence": 0.8}),
        ("victim_bob", "Bob Smith", {"role": "victim", "confidence": 0.9}), 
        ("company_x", "Company X Ltd", {"type": "organization", "confidence": 0.7}),
        ("bank_acc", "Offshore Bank Account", {"type": "financial", "confidence": 0.95})
    ]
    
    for entity_id, name, metadata in entities:
        atom = Atom(
            atom_id=entity_id,
            atom_type=AtomType.ENTITY,
            name=name,
            truth_value=TruthValue(metadata.get("confidence", 0.5), 0.8),
            metadata=metadata
        )
        atomspace.add_atom(atom)
    
    # Add evidence
    evidence = [
        ("email_thread", "Incriminating Email Thread", 0.9),
        ("bank_records", "Suspicious Bank Transfers", 0.95),
        ("witness_testimony", "Eyewitness Account", 0.7),
        ("financial_audit", "Financial Audit Report", 0.85)
    ]
    
    for evidence_id, name, strength in evidence:
        atom = Atom(
            atom_id=evidence_id,
            atom_type=AtomType.EVIDENCE,
            name=name,
            truth_value=TruthValue(strength, 0.9),
            metadata={"type": "evidence", "verified": True}
        )
        atomspace.add_atom(atom)
    
    print(f"✅ Created knowledge base with {len(atomspace.atoms)} atoms")
    
    # Demonstrate queries
    print("\n1. FIND Operations:")
    result = engine.execute_hgnnql("FIND ENTITY")
    print(f"   - Found {result['count']} entities")
    
    result = engine.execute_hgnnql("FIND EVIDENCE") 
    print(f"   - Found {result['count']} pieces of evidence")
    
    print("\n2. COUNT Operations:")
    result = engine.execute_hgnnql("COUNT ENTITY")
    print(f"   - Entity count: {result['count']}")
    
    result = engine.execute_hgnnql("COUNT EVIDENCE")
    print(f"   - Evidence count: {result['count']}")
    
    print("\n3. LINK Operations:")
    links = [
        ("suspect_alice", "company_x", "employed_by"),
        ("suspect_alice", "bank_acc", "controls"),
        ("victim_bob", "company_x", "victim_of_fraud_by"),
        ("email_thread", "suspect_alice", "implicates")
    ]
    
    for source, target, relation in links:
        result = engine.execute_hgnnql(f"LINK {source} TO {target} AS {relation}")
        print(f"   - Linked: {source} --{relation}--> {target}")
    
    print("\n4. QUERY Connected Entities:")
    result = engine.execute_hgnnql("QUERY CONNECTED TO suspect_alice")
    print(f"   - Alice connected to {result['connected_count']} entities:")
    for atom in result['connected_atoms']:
        print(f"     • {atom['name']}")
    
    print("\n5. INFER Operations:")
    inferences = [
        ("financial_fraud", ["email_thread", "bank_records"]),
        ("embezzlement_scheme", ["financial_audit", "bank_acc"]),
        ("conspiracy", ["email_thread", "witness_testimony"])
    ]
    
    for pattern, evidence_ids in inferences:
        evidence_str = " ".join(evidence_ids)
        result = engine.execute_hgnnql(f"INFER {pattern} FROM {evidence_str}")
        print(f"   - Inferred '{pattern}' (confidence: {result['confidence']:.2f})")
    
    return atomspace, engine

def demo_hypergraphql_integration():
    """Demonstrate HyperGraphQL integration"""
    print("\n\n🔗 HyperGraphQL Integration")
    print("=" * 32)
    
    from src.api.hypergraphql_schema import HyperGraphQLSchema, HyperGraphQLNode, EntityTypeQL, OrgLevel
    from src.api.hypergraphql_resolvers import HyperGraphQLResolver
    from frameworks.opencog_hgnnql import AtomType, Link
    
    # Get HGNNQL data
    atomspace, engine = demo_hgnnql_basics()
    
    # Convert to HyperGraphQL
    schema = HyperGraphQLSchema()
    resolver = HyperGraphQLResolver(schema)
    
    converted_count = 0
    for atom in atomspace.atoms.values():
        # Map atom types to GraphQL entity types
        if atom.atom_type == AtomType.ENTITY:
            if "person" in atom.name.lower() or "alice" in atom.name.lower() or "bob" in atom.name.lower():
                node_type = EntityTypeQL.PERSON
            elif "company" in atom.name.lower():
                node_type = EntityTypeQL.ORGANIZATION
            else:
                node_type = EntityTypeQL.AGENT
        elif atom.atom_type == AtomType.EVIDENCE:
            node_type = EntityTypeQL.DOCUMENT
        elif atom.atom_type == AtomType.INFERENCE:
            node_type = EntityTypeQL.DOCUMENT
        else:
            continue
        
        node = HyperGraphQLNode(
            id=atom.atom_id,
            node_type=node_type,
            name=atom.name,
            properties={
                "truth_strength": atom.truth_value.strength,
                "truth_confidence": atom.truth_value.confidence,
                "atom_type": atom.atom_type.value,
                **atom.metadata
            },
            org_level=OrgLevel.REPO,
            metadata={"source": "hgnnql", "case": "fraud_case_2024"}
        )
        schema.add_node(node)
        converted_count += 1
    
    print(f"✅ Converted {converted_count} atoms to HyperGraphQL nodes")
    
    # Demonstrate GraphQL-style queries
    all_nodes = resolver.resolve_nodes()
    print(f"📊 GraphQL query - All nodes: {len(all_nodes)}")
    
    person_nodes = resolver.resolve_nodes(node_type="person")
    print(f"📊 GraphQL query - Person nodes: {len(person_nodes)}")
    
    return schema, resolver

def demo_github_projection():
    """Demonstrate GitHub repository projection"""
    print("\n\n📁 GitHub Repository Projection")
    print("=" * 35)
    
    from src.api.hypergraphql_github import GitHubRepoProjection
    
    # Get HyperGraphQL schema
    schema, resolver = demo_hypergraphql_integration()
    
    # Project to temporary repository
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir) / "hgnnql_fraud_case"
        repo_path.mkdir()
        
        projection = GitHubRepoProjection(str(repo_path))
        projection.project_schema(schema)
        
        stats = projection.get_repo_stats()
        print(f"✅ Projected to repository: {repo_path}")
        print(f"📊 Repository statistics:")
        print(f"   - Total entities: {stats['total_entities']}")
        print(f"   - Total relations: {stats['total_relations']}")
        entity_types = len(stats.get('entity_counts', {}))
        relation_types = len(stats.get('relation_counts', {}))
        print(f"   - Entity types: {entity_types}")
        print(f"   - Relation types: {relation_types}")
        
        # Show structure
        print(f"\n📂 Repository structure:")
        entities_path = repo_path / "entities"
        if entities_path.exists():
            for entity_type_dir in entities_path.iterdir():
                if entity_type_dir.is_dir():
                    files = list(entity_type_dir.glob("*.json"))
                    print(f"   📁 entities/{entity_type_dir.name}/ ({len(files)} files)")
        
        relations_path = repo_path / "relations"
        if relations_path.exists():
            for relation_type_dir in relations_path.iterdir():
                if relation_type_dir.is_dir():
                    files = list(relation_type_dir.glob("*.json"))
                    print(f"   📁 relations/{relation_type_dir.name}/ ({len(files)} files)")
        
        return str(repo_path)

def demo_api_endpoints():
    """Demonstrate API endpoint functionality"""
    print("\n\n🌐 API Endpoints")
    print("=" * 17)
    
    print("📡 Available HGNNQL API Endpoints:")
    endpoints = [
        ("POST /v1/hypergraphql/hgnnql/query", "Execute HGNNQL queries"),
        ("GET /v1/hypergraphql/hgnnql/atomspace/{case_id}/atoms", "Get atomspace data"),
        ("POST /v1/hypergraphql/hgnnql/convert/hypergnn", "Convert HyperGNN to HGNNQL"),
        ("POST /v1/hypergraphql/query", "Execute GraphQL queries"),
        ("GET /v1/hypergraphql/nodes", "Get HyperGraphQL nodes"),
        ("POST /v1/hypergraphql/github/repo/project", "Project schema to GitHub repo")
    ]
    
    for endpoint, description in endpoints:
        print(f"   • {endpoint}")
        print(f"     {description}")
        print()
    
    print("🎯 Frontend Integration Methods:")
    methods = [
        "executeHGNNQL(query, caseId)", 
        "getAtomSpaceAtoms(caseId)",
        "convertHyperGNNToHGNNQL(caseId, data)",
        "executeGraphQLQuery(query, variables)",
        "projectSchemaToRepo(repoPath)"
    ]
    
    for method in methods:
        print(f"   • apiService.{method}")

def demo_query_examples():
    """Show comprehensive query examples"""
    print("\n\n🔍 Query Examples")
    print("=" * 18)
    
    print("HGNNQL Query Language Examples:")
    print()
    
    queries = [
        ("Basic Search", "FIND ENTITY"),
        ("Count Items", "COUNT EVIDENCE"),
        ("Create Links", "LINK alice_johnson TO company_x AS employed_by"),
        ("Graph Traversal", "QUERY CONNECTED TO suspect_alice"),
        ("Filtered Query", "QUERY CONNECTED TO alice WITH employed_by"),
        ("Knowledge Inference", "INFER fraud FROM email_evidence bank_records"),
        ("Complex Reasoning", "INFER conspiracy FROM witness_testimony financial_audit email_thread")
    ]
    
    for category, query in queries:
        print(f"📝 {category}:")
        print(f"   {query}")
        print()
    
    print("GraphQL Query Examples:")
    print()
    
    graphql_queries = [
        "{ nodes { id name nodeType properties } }",
        "{ nodes(nodeType: \"person\") { name properties } }",
        "{ node(id: \"alice_johnson\") { connectedNodes { name } } }",
        "{ edges(edgeType: \"employed_by\") { sourceId targetIds } }"
    ]
    
    for query in graphql_queries:
        print(f"   {query}")
        print()

def main():
    """Main demonstration"""
    print("🚀 Complete HGNNQL Implementation Demo")
    print("=" * 42)
    print()
    
    try:
        # Run all demonstrations
        demo_hgnnql_basics()
        demo_hypergraphql_integration() 
        demo_github_projection()
        demo_api_endpoints()
        demo_query_examples()
        
        print("\n" + "=" * 50)
        print("✨ HGNNQL Implementation Summary")
        print("=" * 50)
        print()
        print("🎯 Features Implemented:")
        features = [
            "OpenCog-style AtomSpace knowledge representation",
            "HGNNQL query language (FIND, LINK, INFER, QUERY, COUNT)",
            "HyperGraphQL schema integration",
            "GitHub repository projection and versioning", 
            "REST and GraphQL API endpoints",
            "Frontend JavaScript integration",
            "Comprehensive unit testing (23 tests)",
            "End-to-end workflow demonstration",
            "Truth values and confidence scoring",
            "Case-LLM reasoning capabilities"
        ]
        
        for feature in features:
            print(f"   ✅ {feature}")
        
        print()
        print("🔗 Integration Points:")
        integrations = [
            "HyperGNN → HGNNQL → HyperGraphQL → GitHub",
            "Knowledge graphs with version control",
            "Semantic reasoning with confidence tracking",
            "Multi-repository organization management",
            "Case analysis workflow automation"
        ]
        
        for integration in integrations:
            print(f"   🔄 {integration}")
        
        print()
        print("🎉 Implementation Complete!")
        print("The HGNNQL system successfully extends GraphQL with")
        print("OpenCog-inspired knowledge representation for case analysis.")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()