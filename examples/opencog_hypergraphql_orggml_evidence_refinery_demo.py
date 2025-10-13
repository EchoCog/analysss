#!/usr/bin/env python3
"""
OpenCog HyperGraphQL ORGGML Evidence Refinery Demo
=================================================

Comprehensive demonstration of the integrated evidence refinery system combining:
- OpenCog-style knowledge representation
- HyperGraphQL API integration  
- GGML-optimized inference engine
- Evidence quality assessment and refinement

This demo shows:
1. Setting up the integrated refinery system
2. Adding raw evidence from various sources
3. Processing evidence through the pipeline
4. Quality assessment and refinement
5. Creating evidence relationships
6. Querying via HyperGraphQL resolvers
7. Exporting refined evidence
"""

import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.opencog_hypergraphql_orggml_evidence_refinery import (
    OpenCogHyperGraphQLORGGMLEvidenceRefinery,
    EvidenceQualityScore,
    EvidenceProcessingStatus
)
from src.api.hypergraphql_resolvers import HyperGraphQLResolver


def print_section(title: str):
    """Print a section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_evidence_summary(evidence):
    """Print formatted evidence summary"""
    print(f"  Evidence ID: {evidence.evidence_id}")
    print(f"  Quality: {evidence.quality_score.value.upper()}")
    print(f"  Confidence: {evidence.confidence:.3f}")
    print(f"  Status: {evidence.processing_status.value}")
    print(f"  Original length: {len(evidence.original_content)} chars")
    print(f"  Refined: {'Yes' if evidence.refined_content else 'No'}")
    if evidence.ggml_analysis:
        relevance = evidence.ggml_analysis.get("relevance_score", 0)
        print(f"  GGML Relevance: {relevance:.3f}")


def demo_setup():
    """Initialize the evidence refinery system"""
    print_section("Setting up OpenCog HyperGraphQL ORGGML Evidence Refinery")
    
    # Initialize the refinery
    case_id = "demo_case_evidence_refinery_001"
    refinery = OpenCogHyperGraphQLORGGMLEvidenceRefinery(
        case_id=case_id,
        output_dir="./evidence_refinery_demo_output"
    )
    
    # Initialize GraphQL resolver and connect to refinery
    resolver = HyperGraphQLResolver(refinery.hypergraphql_schema)
    resolver.set_evidence_refinery(refinery)
    
    print(f"✓ Evidence refinery initialized for case: {case_id}")
    print(f"✓ OpenCog AtomSpace ready")
    print(f"✓ GGML legal engine configured")  
    print(f"✓ HyperGraphQL schema and resolvers connected")
    
    return refinery, resolver


def demo_add_raw_evidence(refinery):
    """Add sample raw evidence to the refinery"""
    print_section("Adding Raw Evidence")
    
    # Sample evidence from different sources
    evidence_samples = [
        {
            "id": "email_001",
            "content": "Email from Rynette Farrar dated 2025-06-15 discussing unauthorized transfer of £50,000 from RegimA Distribution company account to personal account. Email indicates fiduciary duty breach and potential fraud.",
            "source": "email_archive",
            "metadata": {"sender": "rynette@example.com", "date": "2025-06-15"}
        },
        {
            "id": "bank_statement_001", 
            "content": "Bank statement showing transaction ID TX789456 for £50,000 transferred from RegimA Distribution Ltd (Account: 12345678) to personal account (Account: 87654321) on 2025-06-16. Transaction approved by unauthorized card.",
            "source": "bank_records",
            "metadata": {"account": "12345678", "transaction_id": "TX789456"}
        },
        {
            "id": "witness_statement_001",
            "content": "Witness testimony from Daniel Faucitt stating that he observed Rynette Farrar accessing company financial systems without authorization on multiple occasions during June 2025. Witness confirms breach of fiduciary duty.",
            "source": "witness_testimony", 
            "metadata": {"witness": "Daniel Faucitt", "date_observed": "2025-06-01 to 2025-06-30"}
        },
        {
            "id": "contract_breach_001",
            "content": "Legal analysis showing breach of directorship contract clauses 3.2 and 4.1 relating to fiduciary responsibility and unauthorized financial transactions. Contract explicitly prohibits personal use of company funds.",
            "source": "legal_documents",
            "metadata": {"contract_id": "DIR_2023_001", "clauses": ["3.2", "4.1"]}
        },
        {
            "id": "speculation_001",
            "content": "Unverified claim that there might have been additional unreported transactions. This is speculative and lacks supporting documentation.",
            "source": "unverified_sources",
            "metadata": {"reliability": "low"}
        }
    ]
    
    added_evidence = []
    for sample in evidence_samples:
        print(f"\nAdding evidence: {sample['id']}")
        evidence = refinery.add_raw_evidence(
            evidence_id=sample["id"],
            content=sample["content"], 
            source=sample["source"],
            metadata=sample["metadata"]
        )
        added_evidence.append(evidence)
        print(f"  ✓ Added to AtomSpace: {evidence.atom_id}")
        print(f"  ✓ Added to HyperGraphQL: {evidence.graphql_node_id}")
    
    print(f"\n✓ Total evidence added: {len(added_evidence)}")
    return added_evidence


def demo_process_evidence(refinery, evidence_list):
    """Process evidence through the refinery pipeline"""
    print_section("Processing Evidence Through Refinery Pipeline")
    
    processed_evidence = []
    
    for evidence in evidence_list:
        print(f"\nProcessing evidence: {evidence.evidence_id}")
        processed = refinery.process_evidence(evidence.evidence_id)
        processed_evidence.append(processed)
        
        print_evidence_summary(processed)
        
        # Show GGML analysis if available
        if processed.ggml_analysis:
            analysis = processed.ggml_analysis
            print(f"  GGML Legal Significance: {analysis.get('legal_significance', 0):.3f}")
            print(f"  GGML Optimized: {analysis.get('ggml_optimized', False)}")
    
    print(f"\n✓ Processed {len(processed_evidence)} evidence items")
    return processed_evidence


def demo_evidence_relationships(refinery, evidence_list):
    """Create relationships between evidence items"""
    print_section("Creating Evidence Relationships")
    
    # Create relationships between related evidence
    relationships = [
        ("email_001", "bank_statement_001", "corroborates"),
        ("bank_statement_001", "witness_statement_001", "supports"), 
        ("witness_statement_001", "contract_breach_001", "evidences"),
        ("email_001", "contract_breach_001", "demonstrates")
    ]
    
    created_relationships = 0
    for source_id, target_id, rel_type in relationships:
        success = refinery.create_evidence_relationship(
            source_id=source_id,
            target_id=target_id,
            relationship_type=rel_type,
            strength=0.8
        )
        
        if success:
            print(f"  ✓ {source_id} --[{rel_type}]--> {target_id}")
            created_relationships += 1
        else:
            print(f"  ✗ Failed to create: {source_id} -> {target_id}")
    
    print(f"\n✓ Created {created_relationships} evidence relationships")
    
    # Show related evidence for key items
    print("\nFinding related evidence:")
    for evidence_id in ["email_001", "bank_statement_001"]:
        related = refinery.find_related_evidence(evidence_id)
        print(f"  {evidence_id} relates to: {related}")


def demo_graphql_queries(resolver, refinery):
    """Demonstrate GraphQL resolver queries"""
    print_section("HyperGraphQL Resolver Queries")
    
    case_id = refinery.case_id
    
    # Query 1: Get evidence summary
    print("\n1. Evidence Summary Query:")
    summary = resolver.resolve_evidence_summary("email_001")
    if "error" not in summary:
        print(f"  Quality: {summary['qualityScore']}")
        print(f"  Confidence: {summary['confidence']:.3f}")
        print(f"  Related evidence: {summary['relatedEvidenceCount']}")
        print(f"  Processing steps: {summary['processingSteps']}")
    else:
        print(f"  Error: {summary['error']}")
    
    # Query 2: Quality report
    print("\n2. Evidence Quality Report:")
    quality_report = resolver.resolve_evidence_quality_report(case_id)
    if "error" not in quality_report:
        print(f"  Total evidence: {quality_report['totalEvidence']}")
        print(f"  Average confidence: {quality_report['averageConfidence']:.3f}")
        print(f"  Quality distribution: {quality_report['qualityDistribution']}")
    else:
        print(f"  Error: {quality_report['error']}")
    
    # Query 3: Processing status
    print("\n3. Processing Status Report:")
    status_report = resolver.resolve_processing_status(case_id)
    if "error" not in status_report:
        print(f"  AtomSpace size: {status_report['atomSpaceSize']}")
        print(f"  HyperGraphQL nodes: {status_report['hyperGraphQLNodes']}")
        print(f"  HyperGraphQL edges: {status_report['hyperGraphQLEdges']}")
    else:
        print(f"  Error: {status_report['error']}")
    
    # Query 4: Related evidence
    print("\n4. Related Evidence Query:")
    related = resolver.resolve_related_evidence("email_001", threshold=0.5)
    print(f"  Evidence related to 'email_001': {related}")


def demo_quality_assessment(refinery):
    """Demonstrate evidence quality assessment"""
    print_section("Evidence Quality Assessment Analysis")
    
    print("\nQuality Score Distribution:")
    summary = refinery.get_processing_summary()
    quality_dist = summary.get("quality_distribution", {})
    
    for quality, count in quality_dist.items():
        print(f"  {quality.upper()}: {count} items")
    
    print(f"\nOverall Statistics:")
    print(f"  Average confidence: {summary.get('average_confidence', 0):.3f}")
    print(f"  Total relationships: {summary.get('total_relationships', 0)}")
    
    # Show individual quality assessments
    print("\nIndividual Evidence Assessments:")
    for evidence_id, evidence in refinery.refined_evidence.items():
        print(f"\n  {evidence_id}:")
        print(f"    Quality: {evidence.quality_score.value}")
        print(f"    Confidence: {evidence.confidence:.3f}")
        print(f"    Source reliability: {evidence.source_reliability:.3f}")
        if evidence.ggml_analysis:
            relevance = evidence.ggml_analysis.get("relevance_score", 0)
            print(f"    GGML relevance: {relevance:.3f}")


def demo_opencog_integration(refinery):
    """Demonstrate OpenCog AtomSpace integration"""
    print_section("OpenCog AtomSpace Integration")
    
    # Show AtomSpace contents
    print("\nAtomSpace Contents:")
    print(f"  Total atoms: {len(refinery.atomspace.atoms)}")
    
    # Query evidence atoms using HGNNQL
    print("\nHGNNQL Queries:")
    
    # Find all evidence atoms
    result = refinery.query_engine.execute_hgnnql("FIND EVIDENCE")
    print(f"  Evidence atoms found: {result.get('count', 0)}")
    
    # Find all relationship atoms
    result = refinery.query_engine.execute_hgnnql("FIND RELATIONSHIP") 
    print(f"  Relationship atoms found: {result.get('count', 0)}")
    
    # Show connections for specific evidence
    if refinery.refined_evidence:
        first_evidence = list(refinery.refined_evidence.values())[0]
        if first_evidence.atom_id:
            query = f"QUERY CONNECTED TO {first_evidence.atom_id}"
            result = refinery.query_engine.execute_hgnnql(query)
            connected_count = result.get("connected_count", 0)
            print(f"  Atoms connected to {first_evidence.evidence_id}: {connected_count}")


def demo_ggml_optimization(refinery):
    """Demonstrate GGML optimization features"""
    print_section("GGML Legal Engine Optimization")
    
    # Show GGML performance statistics
    performance = refinery.ggml_engine.get_performance_stats()
    print(f"\nGGML Performance Metrics:")
    print(f"  Total tensors: {performance['total_tensors']}")
    print(f"  Quantized tensors: {performance['quantized_tensors']}")
    print(f"  Quantization ratio: {performance['quantization_ratio']:.2f}")
    print(f"  Memory usage: {performance['memory_mb']:.2f} MB")
    print(f"  Available operators: {performance['operators_available']}")
    
    # Show evidence analysis results
    print(f"\nEvidence Analysis Results:")
    for evidence_id, evidence in refinery.refined_evidence.items():
        if evidence.ggml_analysis:
            analysis = evidence.ggml_analysis
            print(f"\n  {evidence_id}:")
            print(f"    Relevance score: {analysis.get('relevance_score', 0):.3f}")
            print(f"    Legal significance: {analysis.get('legal_significance', 0):.3f}")
            print(f"    GGML optimized: {analysis.get('ggml_optimized', False)}")


def demo_export_results(resolver, refinery):
    """Demonstrate exporting refined evidence"""
    print_section("Exporting Refined Evidence")
    
    # Export via GraphQL resolver
    print("\nExporting via HyperGraphQL resolver:")
    export_result = resolver.resolve_export_refined_evidence(refinery.case_id, "json")
    
    if export_result["success"]:
        print(f"  ✓ Export successful!")
        print(f"  ✓ File: {export_result['filepath']}")
        print(f"  ✓ Records: {export_result['recordCount']}")
        print(f"  ✓ Message: {export_result['message']}")
    else:
        print(f"  ✗ Export failed: {export_result['message']}")
    
    # Also export directly from refinery
    print(f"\nDirect export from refinery:")
    try:
        filepath = refinery.export_refined_evidence("json")
        print(f"  ✓ Exported to: {filepath}")
        
        # Show file size
        file_path = Path(filepath)
        if file_path.exists():
            size_kb = file_path.stat().st_size / 1024
            print(f"  ✓ File size: {size_kb:.1f} KB")
    except Exception as e:
        print(f"  ✗ Export error: {str(e)}")


def demo_complete_pipeline():
    """Run the complete evidence refinery demonstration"""
    print("\n" + "🧠" * 40)
    print("  OpenCog HyperGraphQL ORGGML Evidence Refinery")
    print("  Comprehensive AI-Powered Evidence Processing")
    print("🧠" * 40)
    
    # Setup
    refinery, resolver = demo_setup()
    
    # Add evidence
    evidence_list = demo_add_raw_evidence(refinery)
    
    # Process evidence
    processed_evidence = demo_process_evidence(refinery, evidence_list)
    
    # Create relationships
    demo_evidence_relationships(refinery, processed_evidence)
    
    # GraphQL queries
    demo_graphql_queries(resolver, refinery)
    
    # Quality assessment
    demo_quality_assessment(refinery)
    
    # OpenCog integration
    demo_opencog_integration(refinery)
    
    # GGML optimization
    demo_ggml_optimization(refinery)
    
    # Export results
    demo_export_results(resolver, refinery)
    
    # Final summary
    print_section("Demo Completion Summary")
    
    summary = refinery.get_processing_summary()
    print(f"\n✓ Successfully demonstrated evidence refinery integration!")
    print(f"\nFinal Statistics:")
    print(f"  • Evidence processed: {summary['total_evidence']}")
    print(f"  • Average quality confidence: {summary['average_confidence']:.3f}")
    print(f"  • Evidence relationships: {summary['total_relationships']}")
    print(f"  • OpenCog atoms: {summary['atomspace_size']}")
    print(f"  • HyperGraphQL nodes: {summary['hypergraphql_nodes']}")
    print(f"  • HyperGraphQL edges: {summary['hypergraphql_edges']}")
    
    print(f"\nKey Features Demonstrated:")
    print(f"  ✓ OpenCog AtomSpace knowledge representation")
    print(f"  ✓ GGML-optimized neural inference for legal analysis")
    print(f"  ✓ HyperGraphQL API integration with evidence operations")
    print(f"  ✓ Automated evidence quality assessment and refinement")
    print(f"  ✓ Evidence relationship detection and mapping")
    print(f"  ✓ Multi-framework integration and optimization")
    
    print(f"\n📁 Output files saved to: {refinery.output_dir}/")
    print(f"\n" + "=" * 80)


if __name__ == "__main__":
    demo_complete_pipeline()