#!/usr/bin/env python3
"""
Test Enhanced HGNNQL Implementation
==================================

Demonstrates the enhanced HGNNQL query language with:
- FIND queries with filtering
- LINK operations for creating relationships
- INFER operations for reasoning
- QUERY operations for graph traversal
- COUNT operations with conditions
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from frameworks.opencog_hgnnql import (
    Atom, AtomSpace, AtomType, HGNNQLQueryEngine, TruthValue
)

def create_sample_case_knowledge():
    """Create a sample knowledge base for case analysis"""
    atomspace = AtomSpace("test_case_001")
    
    # Add entities
    alice = Atom(
        atom_id="alice_johnson",
        atom_type=AtomType.ENTITY,
        name="Alice Johnson",
        truth_value=TruthValue(0.9, 0.8),
        metadata={"role": "suspect", "age": 35}
    )
    
    bob = Atom(
        atom_id="bob_smith", 
        atom_type=AtomType.ENTITY,
        name="Bob Smith",
        truth_value=TruthValue(0.8, 0.9),
        metadata={"role": "victim", "age": 42}
    )
    
    company = Atom(
        atom_id="company_a",
        atom_type=AtomType.ENTITY,
        name="Company A Ltd",
        truth_value=TruthValue(0.7, 0.6),
        metadata={"type": "organization"}
    )
    
    # Add events
    meeting = Atom(
        atom_id="meeting_001",
        atom_type=AtomType.EVENT,
        name="Suspicious Meeting",
        truth_value=TruthValue(0.6, 0.8),
        metadata={"date": "2024-01-15", "location": "Downtown Office"}
    )
    
    transfer = Atom(
        atom_id="transfer_001",
        atom_type=AtomType.EVENT,
        name="Financial Transfer",
        truth_value=TruthValue(0.8, 0.9),
        metadata={"amount": 50000, "date": "2024-01-16"}
    )
    
    # Add evidence
    email_evidence = Atom(
        atom_id="email_001",
        atom_type=AtomType.EVIDENCE,
        name="Incriminating Email",
        truth_value=TruthValue(0.9, 0.95),
        metadata={"type": "digital", "verified": True}
    )
    
    bank_records = Atom(
        atom_id="bank_001",
        atom_type=AtomType.EVIDENCE,
        name="Bank Transaction Records",
        truth_value=TruthValue(0.95, 0.99),
        metadata={"type": "financial", "verified": True}
    )
    
    # Add atoms to atomspace
    for atom in [alice, bob, company, meeting, transfer, email_evidence, bank_records]:
        atomspace.add_atom(atom)
    
    return atomspace

def demonstrate_hgnnql_queries():
    """Demonstrate enhanced HGNNQL query capabilities"""
    print("🔍 Enhanced HGNNQL Query Demonstration")
    print("=" * 50)
    
    # Create knowledge base
    atomspace = create_sample_case_knowledge()
    query_engine = HGNNQLQueryEngine(atomspace)
    
    # 1. Basic FIND queries
    print("\n1. Basic FIND Queries:")
    print("-" * 25)
    
    result = query_engine.execute_hgnnql("FIND ENTITY")
    print(f"   Entities found: {result['count']}")
    for entity in result['results'][:3]:  # Show first 3
        print(f"   - {entity['name']} (confidence: {entity['truth_value']['confidence']:.2f})")
    
    result = query_engine.execute_hgnnql("FIND EVIDENCE")
    print(f"   Evidence found: {result['count']}")
    for evidence in result['results']:
        print(f"   - {evidence['name']} (strength: {evidence['truth_value']['strength']:.2f})")
    
    # 2. COUNT queries
    print("\n2. COUNT Queries:")
    print("-" * 18)
    
    result = query_engine.execute_hgnnql("COUNT ENTITY")
    print(f"   Total entities: {result['count']}")
    
    result = query_engine.execute_hgnnql("COUNT EVENT")
    print(f"   Total events: {result['count']}")
    
    # 3. LINK operations
    print("\n3. LINK Operations:")
    print("-" * 20)
    
    # Link entities
    result = query_engine.execute_hgnnql("LINK alice_johnson TO company_a AS employed_by")
    print(f"   Link result: {result}")
    if 'source' in result:
        print(f"   Link created: {result['source']} -> {result['target']} ({result['relationship']})")
    else:
        print(f"   Link error: {result.get('error', 'Unknown error')}")
    
    result = query_engine.execute_hgnnql("LINK meeting_001 TO alice_johnson AS attended_by")
    print(f"   Link created: {result['source']} -> {result['target']} ({result['relationship']})")
    
    result = query_engine.execute_hgnnql("LINK transfer_001 TO bob_smith AS beneficiary")
    print(f"   Link created: {result['source']} -> {result['target']} ({result['relationship']})")
    
    # 4. QUERY connected entities
    print("\n4. QUERY Connected Entities:")
    print("-" * 30)
    
    result = query_engine.execute_hgnnql("QUERY CONNECTED TO alice_johnson")
    print(f"   Entities connected to Alice: {result['connected_count']}")
    for connected in result['connected_atoms']:
        print(f"   - {connected['name']}")
    
    # 5. INFER operations
    print("\n5. INFER Operations:")
    print("-" * 21)
    
    result = query_engine.execute_hgnnql("INFER suspicious_activity FROM email_001 bank_001")
    print(f"   Inference: {result['pattern']}")
    print(f"   Confidence: {result['confidence']:.2f}")
    print(f"   Strength: {result['strength']:.2f}")
    print(f"   Based on {result['evidence_count']} pieces of evidence")
    
    result = query_engine.execute_hgnnql("INFER financial_fraud FROM transfer_001 meeting_001")
    print(f"   Inference: {result['pattern']}")
    print(f"   Confidence: {result['confidence']:.2f}")
    
    # 6. Complex queries after inference
    print("\n6. Post-Inference Analysis:")
    print("-" * 28)
    
    result = query_engine.execute_hgnnql("FIND INFERENCE")
    print(f"   Inferences generated: {result['count']}")
    for inference in result['results']:
        print(f"   - {inference['name']} (confidence: {inference['truth_value']['confidence']:.2f})")
    
    print(f"\n📊 Total atoms in knowledge base: {len(atomspace.atoms)}")
    
    # Count links (which are stored as atoms with RELATIONSHIP type)
    from frameworks.opencog_hgnnql import Link
    link_count = len([atom for atom in atomspace.atoms.values() if isinstance(atom, Link)])
    print(f"📊 Total links in knowledge base: {link_count}")
    
    return atomspace, query_engine

def demonstrate_hypergraphql_integration():
    """Demonstrate integration with HyperGraphQL"""
    print("\n\n🔗 HyperGraphQL Integration")
    print("=" * 30)
    
    try:
        from src.api.hypergraphql_schema import HyperGraphQLSchema, HyperGraphQLNode, EntityTypeQL, OrgLevel
        from src.api.hypergraphql_resolvers import HyperGraphQLResolver
        
        # Create HyperGraphQL schema
        schema = HyperGraphQLSchema()
        resolver = HyperGraphQLResolver(schema)
        
        # Create sample atomspace
        atomspace, query_engine = demonstrate_hgnnql_queries()
        
        # Convert HGNNQL atoms to HyperGraphQL nodes
        converted_count = 0
        for atom in atomspace.atoms.values():
            if atom.atom_type == AtomType.ENTITY:
                node_type = EntityTypeQL.PERSON if "person" in atom.name.lower() else EntityTypeQL.ORGANIZATION
            elif atom.atom_type == AtomType.EVENT:
                node_type = EntityTypeQL.EVENT
            elif atom.atom_type == AtomType.EVIDENCE:
                node_type = EntityTypeQL.DOCUMENT
            elif atom.atom_type == AtomType.INFERENCE:
                node_type = EntityTypeQL.DOCUMENT  # Treat inferences as documents
            else:
                node_type = EntityTypeQL.AGENT  # Default to agent for other types
            
            node = HyperGraphQLNode(
                id=atom.atom_id,
                node_type=node_type,
                name=atom.name,
                properties={
                    "truth_strength": atom.truth_value.strength,
                    "truth_confidence": atom.truth_value.confidence,
                    **atom.metadata
                },
                org_level=OrgLevel.REPO,
                metadata={"source": "hgnnql", "atom_type": atom.atom_type.value}
            )
            schema.add_node(node)
            converted_count += 1
        
        print(f"✅ Converted {converted_count} HGNNQL atoms to HyperGraphQL nodes")
        print(f"📊 Total HyperGraphQL nodes: {len(schema.nodes)}")
        
        # Demonstrate GraphQL-style queries
        nodes = resolver.resolve_nodes(node_type=None, org_level="REPO")
        print(f"📊 GraphQL query result: {len(nodes)} nodes")
        
    except ImportError as e:
        print(f"⚠️ HyperGraphQL integration skipped: {e}")

if __name__ == "__main__":
    print("🚀 Enhanced HGNNQL Implementation Test")
    print("=" * 45)
    
    try:
        # Main demonstration
        demonstrate_hgnnql_queries()
        
        # Integration demonstration
        demonstrate_hypergraphql_integration()
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()