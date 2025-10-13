#!/usr/bin/env python3
"""
HyperGraphQL Demonstration Script
===================================

Demonstrates the HyperGraphQL API functionality including:
- Schema creation and management
- GitHub repository projection
- Org-aware operations
- Scaling capabilities
"""

import json
import sys
import tempfile
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.api.hypergraphql_schema import (
    EntityTypeQL,
    HyperGraphQLEdge,
    HyperGraphQLNode,
    HyperGraphQLOrgMapping,
    HyperGraphQLSchema,
    OrgLevel,
    RelationTypeQL,
)
from src.api.hypergraphql_resolvers import HyperGraphQLResolver
from src.api.hypergraphql_github import GitHubRepoProjection, OrgAwareManager


def demo_schema_creation():
    """Demonstrate schema creation and basic operations"""
    print("\n" + "="*60)
    print("DEMO 1: Schema Creation and Basic Operations")
    print("="*60)
    
    schema = HyperGraphQLSchema()
    
    # Add nodes
    print("\n1. Adding nodes to schema...")
    nodes = [
        HyperGraphQLNode(
            id="person_alice",
            node_type=EntityTypeQL.PERSON,
            name="Alice Johnson",
            properties={"age": 35, "role": "Investigator"},
            org_level=OrgLevel.REPO
        ),
        HyperGraphQLNode(
            id="person_bob",
            node_type=EntityTypeQL.PERSON,
            name="Bob Smith",
            properties={"age": 42, "role": "Analyst"},
            org_level=OrgLevel.REPO
        ),
        HyperGraphQLNode(
            id="org_company_a",
            node_type=EntityTypeQL.ORGANIZATION,
            name="Company A Ltd",
            properties={"industry": "Technology", "size": "Large"},
            org_level=OrgLevel.REPO
        ),
        HyperGraphQLNode(
            id="event_meeting_1",
            node_type=EntityTypeQL.EVENT,
            name="Board Meeting 2025-01-15",
            properties={"date": "2025-01-15", "location": "HQ"},
            org_level=OrgLevel.REPO
        )
    ]
    
    for node in nodes:
        schema.add_node(node)
        print(f"   ✓ Added {node.node_type.value}: {node.name}")
    
    # Add edges
    print("\n2. Adding relations (edges)...")
    edges = [
        HyperGraphQLEdge(
            id="edge_alice_works_at",
            edge_type=RelationTypeQL.MEMBER_OF,
            source_id="person_alice",
            target_ids=["org_company_a"],
            strength=0.9,
            properties={"position": "Lead Investigator"}
        ),
        HyperGraphQLEdge(
            id="edge_bob_works_at",
            edge_type=RelationTypeQL.MEMBER_OF,
            source_id="person_bob",
            target_ids=["org_company_a"],
            strength=0.85,
            properties={"position": "Senior Analyst"}
        ),
        HyperGraphQLEdge(
            id="edge_alice_bob_comm",
            edge_type=RelationTypeQL.COMMUNICATES_WITH,
            source_id="person_alice",
            target_ids=["person_bob"],
            strength=0.7
        ),
        HyperGraphQLEdge(
            id="edge_meeting_participants",
            edge_type=RelationTypeQL.PARTICIPATES_IN,
            source_id="event_meeting_1",
            target_ids=["person_alice", "person_bob"],  # Hyperedge with multiple targets
            strength=1.0
        )
    ]
    
    for edge in edges:
        schema.add_edge(edge)
        print(f"   ✓ Added {edge.edge_type.value}: {edge.source_id} -> {edge.target_ids}")
    
    # Query schema
    print("\n3. Querying schema...")
    print(f"   Total nodes: {len(schema.nodes)}")
    print(f"   Total edges: {len(schema.edges)}")
    
    person_nodes = schema.get_nodes_by_type(EntityTypeQL.PERSON)
    print(f"   Person nodes: {len(person_nodes)}")
    
    connected = schema.get_connected_nodes("person_alice")
    print(f"   Nodes connected to Alice: {[n.name for n in connected]}")
    
    return schema


def demo_github_projection(schema):
    """Demonstrate GitHub repository projection"""
    print("\n" + "="*60)
    print("DEMO 2: GitHub Repository Projection")
    print("="*60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir) / "demo_repo"
        repo_path.mkdir()
        
        print(f"\n1. Creating projection in: {repo_path}")
        projection = GitHubRepoProjection(str(repo_path))
        
        print("\n2. Initializing repository structure...")
        projection.initialize_repo_structure()
        print("   ✓ Created entities/ folder structure")
        print("   ✓ Created relations/ folder structure")
        print("   ✓ Created README files")
        
        print("\n3. Projecting schema to repository...")
        projection.project_schema(schema)
        
        stats = projection.get_repo_stats()
        print(f"\n4. Repository statistics:")
        print(f"   Total entities: {stats['total_entities']}")
        print(f"   Total relations: {stats['total_relations']}")
        print(f"   Entity breakdown:")
        for entity_type, count in stats['entity_counts'].items():
            print(f"      - {entity_type}: {count}")
        
        print("\n5. Listing created files:")
        for entity_file in sorted((repo_path / "entities").rglob("*.json")):
            rel_path = entity_file.relative_to(repo_path)
            print(f"   📄 {rel_path}")
        
        for relation_file in sorted((repo_path / "relations").rglob("*.json")):
            rel_path = relation_file.relative_to(repo_path)
            print(f"   📄 {rel_path}")
        
        print("\n6. Sample entity file content:")
        sample_file = repo_path / "entities" / "person" / "person_alice.json"
        if sample_file.exists():
            with open(sample_file, 'r') as f:
                content = json.load(f)
            print(f"   {json.dumps(content, indent=2)}")


def demo_resolver_operations():
    """Demonstrate resolver operations"""
    print("\n" + "="*60)
    print("DEMO 3: Resolver Operations")
    print("="*60)
    
    schema = HyperGraphQLSchema()
    resolver = HyperGraphQLResolver(schema)
    
    print("\n1. Adding nodes via resolver...")
    node_input = {
        "nodeType": "person",
        "name": "Charlie Brown",
        "properties": {"age": 28, "role": "Junior Analyst"},
        "orgLevel": "repo"
    }
    created_node = resolver.resolve_add_node(node_input)
    print(f"   ✓ Created node: {created_node['name']}")
    
    print("\n2. Querying nodes...")
    all_nodes = resolver.resolve_nodes()
    print(f"   Found {len(all_nodes)} nodes")
    
    print("\n3. Adding edge via resolver...")
    edge_input = {
        "edgeType": "related_to",
        "sourceId": created_node['id'],
        "targetIds": ["person_alice"],
        "strength": 0.6,
        "orgLevel": "repo"
    }
    created_edge = resolver.resolve_add_edge(edge_input)
    print(f"   ✓ Created edge: {created_edge['edgeType']}")
    
    print("\n4. Exporting schema...")
    exported = resolver.resolve_export_schema()
    print(f"   Exported {exported['metadata']['nodeCount']} nodes")
    print(f"   Exported {exported['metadata']['edgeCount']} edges")


def demo_org_management():
    """Demonstrate org-aware management"""
    print("\n" + "="*60)
    print("DEMO 4: Organization-Aware Management")
    print("="*60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir)
        
        # Create multiple repos
        print("\n1. Creating multiple repositories...")
        repos = {}
        for i in range(1, 4):
            repo_path = base_path / f"repo{i}"
            repo_path.mkdir()
            
            # Create schema for each repo
            schema = HyperGraphQLSchema()
            schema.add_node(HyperGraphQLNode(
                id=f"person_{i}",
                node_type=EntityTypeQL.PERSON,
                name=f"Person {i}",
                properties={"repo": f"repo{i}"},
                org_level=OrgLevel.REPO
            ))
            
            # Project to repo
            projection = GitHubRepoProjection(str(repo_path))
            projection.project_schema(schema)
            
            repos[f"repo{i}"] = repo_path
            print(f"   ✓ Created repo{i}")
        
        # Create org manager
        print("\n2. Creating organization manager...")
        manager = OrgAwareManager("demo-org", OrgLevel.ORG)
        
        print("\n3. Registering repositories...")
        for repo_name, repo_path in repos.items():
            manager.register_repo(repo_name, str(repo_path))
            print(f"   ✓ Registered {repo_name}")
        
        print("\n4. Aggregating schemas across repos...")
        aggregated_schema = manager.aggregate_schemas()
        print(f"   ✓ Aggregated {len(aggregated_schema.nodes)} nodes")
        print(f"   ✓ Aggregated {len(aggregated_schema.edges)} edges")
        
        print("\n5. Getting organization statistics...")
        stats = manager.get_org_stats()
        print(f"   Organization: {stats['org_name']}")
        print(f"   Total repos: {stats['repo_count']}")
        print(f"   Total entities: {stats['total_entities']}")
        print(f"   Repo breakdown:")
        for repo_name, repo_stats in stats['repos'].items():
            print(f"      - {repo_name}: {repo_stats['total_entities']} entities")


def demo_scaling_capabilities():
    """Demonstrate scaling capabilities"""
    print("\n" + "="*60)
    print("DEMO 5: Scaling Capabilities")
    print("="*60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir)
        repo_path = base_path / "scale_demo_repo"
        repo_path.mkdir()
        
        # Create a substantial schema
        print("\n1. Creating schema with multiple entity types...")
        schema = HyperGraphQLSchema()
        
        entity_counts = {
            EntityTypeQL.PERSON: 5,
            EntityTypeQL.ORGANIZATION: 3,
            EntityTypeQL.EVENT: 4,
            EntityTypeQL.EVIDENCE: 2
        }
        
        for entity_type, count in entity_counts.items():
            for i in range(count):
                schema.add_node(HyperGraphQLNode(
                    id=f"{entity_type.value}_{i}",
                    node_type=entity_type,
                    name=f"{entity_type.value.title()} {i}",
                    org_level=OrgLevel.REPO
                ))
        
        print(f"   ✓ Created {len(schema.nodes)} nodes")
        
        # Project to repo
        print("\n2. Projecting to repository...")
        projection = GitHubRepoProjection(str(repo_path))
        projection.project_schema(schema)
        
        # Show scaling down (compression)
        print("\n3. Demonstrating scale-down (compression)...")
        manager = OrgAwareManager("scale-demo-org", OrgLevel.ORG)
        manager.register_repo("demo_repo", str(repo_path))
        
        archive_path = manager.compress_repo("demo_repo", str(base_path))
        archive_size = archive_path.stat().st_size
        print(f"   ✓ Compressed to: {archive_path.name}")
        print(f"   ✓ Archive size: {archive_size:,} bytes")
        
        # Calculate original size
        original_size = sum(
            f.stat().st_size 
            for f in repo_path.rglob("*.json")
        )
        print(f"   ✓ Original size: {original_size:,} bytes")
        print(f"   ✓ Compression ratio: {original_size/archive_size:.2f}x")


def main():
    """Run all demonstrations"""
    print("\n" + "🚀" * 30)
    print("   HyperGraphQL API Demonstration")
    print("🚀" * 30)
    
    try:
        # Demo 1: Schema creation
        schema = demo_schema_creation()
        
        # Demo 2: GitHub projection
        demo_github_projection(schema)
        
        # Demo 3: Resolver operations
        demo_resolver_operations()
        
        # Demo 4: Org management
        demo_org_management()
        
        # Demo 5: Scaling
        demo_scaling_capabilities()
        
        print("\n" + "="*60)
        print("✅ All demonstrations completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
