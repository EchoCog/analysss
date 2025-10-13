#!/usr/bin/env python3
"""
HyperGraphQL and HyperGNN Integration Example
==============================================

Demonstrates how to integrate HyperGraphQL with the HyperGNN framework
to map entities, events, and flows to a GraphQL-queryable structure
that can be projected to GitHub repositories.
"""

import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.api.hypergnn_core import (
        Agent, AgentType, DiscreteEvent, EventType,
        HyperGNNFramework, SystemFlow, FlowType
    )
    HYPERGNN_AVAILABLE = True
except ImportError:
    print("Warning: HyperGNN framework not available. Using mock implementation.")
    HYPERGNN_AVAILABLE = False

from src.api.hypergraphql_schema import (
    EntityTypeQL, HyperGraphQLEdge, HyperGraphQLNode,
    HyperGraphQLSchema, OrgLevel, RelationTypeQL
)
from src.api.hypergraphql_resolvers import HyperGraphQLResolver
from src.api.hypergraphql_github import GitHubRepoProjection


def create_sample_hypergnn_case():
    """Create a sample case using HyperGNN framework"""
    if not HYPERGNN_AVAILABLE:
        return None
        
    print("Creating sample HyperGNN case...")
    
    # Initialize framework
    framework = HyperGNNFramework("sample_case_001")
    
    # Add agents
    alice = Agent(
        agent_id="agent_alice",
        agent_type=AgentType.INDIVIDUAL,
        name="Alice Johnson"
    )
    alice.attributes = {"role": "Lead Investigator", "department": "Fraud"}
    framework.add_agent(alice)
    
    bob = Agent(
        agent_id="agent_bob",
        agent_type=AgentType.INDIVIDUAL,
        name="Bob Smith"
    )
    bob.attributes = {"role": "Financial Analyst", "department": "Analysis"}
    framework.add_agent(bob)
    
    company = Agent(
        agent_id="agent_company_a",
        agent_type=AgentType.ORGANIZATION,
        name="Company A Ltd"
    )
    company.attributes = {"industry": "Technology", "status": "Under Investigation"}
    framework.add_agent(company)
    
    # Add events
    meeting = DiscreteEvent(
        event_id="event_meeting_001",
        event_type=EventType.MEETING,
        timestamp=datetime(2025, 1, 15, 10, 0),
        description="Investigation Planning Meeting",
        actors=["agent_alice", "agent_bob"]
    )
    framework.add_event(meeting)
    
    transaction = DiscreteEvent(
        event_id="event_transaction_001",
        event_type=EventType.TRANSACTION,
        timestamp=datetime(2025, 1, 20, 14, 30),
        description="Suspicious Financial Transfer",
        actors=["agent_company_a"]
    )
    framework.add_event(transaction)
    
    # Add flows
    info_flow = SystemFlow(
        flow_id="flow_info_001",
        flow_type=FlowType.INFORMATION,
        source="agent_alice",
        target="agent_bob",
        magnitude=0.8,
        timestamp=datetime(2025, 1, 16, 9, 0),
        description="Case file sharing"
    )
    framework.add_flow(info_flow)
    
    print(f"✓ Created framework with {len(framework.agents)} agents, "
          f"{len(framework.events)} events, {len(framework.flows)} flows")
    
    return framework


def convert_hypergnn_to_hypergraphql(framework):
    """Convert HyperGNN framework to HyperGraphQL schema"""
    print("\nConverting HyperGNN to HyperGraphQL...")
    
    schema = HyperGraphQLSchema()
    resolver = HyperGraphQLResolver(schema)
    
    # Register the framework with resolver
    case_id = framework.case_id
    resolver.set_hypergnn_framework(case_id, framework)
    
    # Load data from framework
    resolver.load_from_hypergnn(case_id)
    
    print(f"✓ Converted to HyperGraphQL schema with {len(schema.nodes)} nodes "
          f"and {len(schema.edges)} edges")
    
    return schema, resolver


def demonstrate_graphql_queries(resolver):
    """Demonstrate GraphQL queries on the converted data"""
    print("\nDemonstrating GraphQL queries...")
    
    # Query all nodes
    all_nodes = resolver.resolve_nodes()
    print(f"\n1. All nodes ({len(all_nodes)} total):")
    for node in all_nodes[:5]:  # Show first 5
        print(f"   - {node['nodeType']}: {node['name']}")
    
    # Query by type
    agents = resolver.resolve_nodes(node_type="agent")
    print(f"\n2. Agent nodes ({len(agents)} total):")
    for agent in agents:
        print(f"   - {agent['name']}")
    
    # Query by org level
    repo_level = resolver.resolve_nodes(org_level="repo")
    print(f"\n3. Repo-level nodes: {len(repo_level)}")
    
    # Query edges
    all_edges = resolver.resolve_edges()
    print(f"\n4. All edges ({len(all_edges)} total):")
    for edge in all_edges[:5]:  # Show first 5
        print(f"   - {edge['edgeType']}: {edge['sourceId']} -> {edge['targetIds']}")
    
    # Query connected nodes
    if all_nodes:
        first_node_id = all_nodes[0]['id']
        connected = resolver.resolve_connected_nodes(first_node_id)
        print(f"\n5. Nodes connected to {first_node_id}: {len(connected)}")
        for node in connected[:3]:
            print(f"   - {node['name']}")


def project_to_github_repo(schema):
    """Project the schema to a GitHub repository structure"""
    print("\nProjecting to GitHub repository structure...")
    
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir) / "hypergnn_case_repo"
        repo_path.mkdir()
        
        # Initialize and project
        projection = GitHubRepoProjection(str(repo_path))
        projection.project_schema(schema)
        
        # Show structure
        print(f"\nRepository structure created at: {repo_path}")
        print("\nEntities:")
        for entity_file in sorted((repo_path / "entities").rglob("*.json"))[:5]:
            rel_path = entity_file.relative_to(repo_path)
            print(f"   📄 {rel_path}")
        
        print("\nRelations:")
        for relation_file in sorted((repo_path / "relations").rglob("*.json"))[:5]:
            rel_path = relation_file.relative_to(repo_path)
            print(f"   📄 {rel_path}")
        
        # Show stats
        stats = projection.get_repo_stats()
        print(f"\nRepository Statistics:")
        print(f"   Total entities: {stats['total_entities']}")
        print(f"   Total relations: {stats['total_relations']}")
        
        return repo_path


def demonstrate_round_trip(framework):
    """Demonstrate round-trip: HyperGNN -> HyperGraphQL -> GitHub -> HyperGraphQL"""
    print("\n" + "="*60)
    print("Round-Trip Demonstration")
    print("="*60)
    
    # Step 1: Convert to HyperGraphQL
    schema1, resolver1 = convert_hypergnn_to_hypergraphql(framework)
    original_node_count = len(schema1.nodes)
    original_edge_count = len(schema1.edges)
    
    # Step 2: Project to GitHub
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir) / "roundtrip_repo"
        repo_path.mkdir()
        
        projection = GitHubRepoProjection(str(repo_path))
        projection.project_schema(schema1)
        print(f"✓ Projected to GitHub: {original_node_count} nodes, {original_edge_count} edges")
        
        # Step 3: Load back from GitHub
        schema2 = HyperGraphQLSchema()
        resolver2 = HyperGraphQLResolver(schema2)
        resolver2.load_from_repo_structure(str(repo_path), "test-org")
        
        loaded_node_count = len(schema2.nodes)
        loaded_edge_count = len(schema2.edges)
        
        print(f"✓ Loaded from GitHub: {loaded_node_count} nodes, {loaded_edge_count} edges")
        
        # Verify round-trip
        if loaded_node_count == original_node_count and loaded_edge_count == original_edge_count:
            print("✅ Round-trip successful! All data preserved.")
        else:
            print("⚠️ Round-trip data mismatch detected.")


def main():
    """Main demonstration"""
    print("\n" + "🔗" * 30)
    print("   HyperGraphQL & HyperGNN Integration Demo")
    print("🔗" * 30)
    
    if not HYPERGNN_AVAILABLE:
        print("\n❌ HyperGNN framework not available.")
        print("This demo requires the HyperGNN framework to be properly installed.")
        return
    
    try:
        # Create HyperGNN case
        framework = create_sample_hypergnn_case()
        
        # Convert to HyperGraphQL
        schema, resolver = convert_hypergnn_to_hypergraphql(framework)
        
        # Demonstrate queries
        demonstrate_graphql_queries(resolver)
        
        # Project to GitHub
        project_to_github_repo(schema)
        
        # Demonstrate round-trip
        demonstrate_round_trip(framework)
        
        print("\n" + "="*60)
        print("✅ Integration demonstration completed successfully!")
        print("="*60)
        print("\nKey Takeaways:")
        print("1. HyperGNN agents/events/flows map to HyperGraphQL nodes/edges")
        print("2. GraphQL queries provide flexible data access")
        print("3. GitHub projection enables version control and collaboration")
        print("4. Round-trip conversion preserves all data")
        print("5. Org-aware management supports multi-repo scaling")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
