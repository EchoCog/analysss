#!/usr/bin/env python3
"""
OpenCog HGNNQL Case-LLM Demo
============================

Demonstration of the complete OpenCog-inspired Case-LLM system
integrating HGNNQL, Hyper-Holmes inference engine, and Super-Sleuth
introspection trainer.

This demo shows how to:
1. Initialize the OpenCog Case-LLM system
2. Load case data from HyperGNN framework
3. Query the knowledge base with HGNNQL
4. Run automated inference
5. Train introspection system
6. Generate investigation leads
7. Ask natural language questions
"""

import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from frameworks.opencog_case_llm import OpenCogCaseLLM


def print_section(title: str):
    """Print a section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_basic_usage():
    """Demonstrate basic usage of OpenCog Case-LLM"""
    print_section("OpenCog HGNNQL Case-LLM Demo")
    
    # Initialize the system
    print("\n1. Initializing OpenCog Case-LLM system...")
    system = OpenCogCaseLLM(case_id="demo_case_001", output_dir="./output/opencog_demo")
    print("   ✓ System initialized")
    
    # Add sample entities
    print("\n2. Adding entities to knowledge base...")
    system.add_entity("alice", "Alice Johnson", "person", {
        "role": "Lead Investigator",
        "department": "Fraud Detection"
    })
    system.add_entity("bob", "Bob Smith", "person", {
        "role": "Financial Analyst",
        "department": "Finance"
    })
    system.add_entity("company_a", "Company A Ltd", "organization", {
        "industry": "Technology",
        "status": "Under Investigation"
    })
    print("   ✓ Added 3 entities")
    
    # Add sample events
    print("\n3. Adding events to timeline...")
    system.add_event("event_001", "Initial meeting to discuss case", 
                    datetime(2025, 1, 15, 10, 0),
                    participants=["alice", "bob"])
    system.add_event("event_002", "Suspicious transaction detected",
                    datetime(2025, 1, 20, 14, 30),
                    participants=["company_a"])
    system.add_event("event_003", "Follow-up investigation meeting",
                    datetime(2025, 1, 25, 9, 0),
                    participants=["alice", "bob"])
    print("   ✓ Added 3 events")
    
    # Add relationships
    print("\n4. Adding relationships...")
    system.add_relationship("alice", "bob", "colleagues", strength=0.9)
    system.add_relationship("alice", "company_a", "investigates", strength=0.85)
    print("   ✓ Added 2 relationships")
    
    # Add evidence
    print("\n5. Adding evidence...")
    system.add_evidence("evidence_001", "Bank transfer records showing irregularities",
                       related_entities=["company_a"],
                       verification_status="verified")
    system.add_evidence("evidence_002", "Email communications between parties",
                       related_entities=["alice", "bob"],
                       verification_status="unverified")
    print("   ✓ Added 2 evidence items")
    
    return system


def demo_queries(system: OpenCogCaseLLM):
    """Demonstrate HGNNQL queries"""
    print_section("HGNNQL Query Demonstrations")
    
    # Query 1: Find all entities
    print("\n1. Query: FIND ENTITY")
    result = system.query_hgnnql("FIND ENTITY")
    print(f"   Found {result['count']} entities")
    for atom in result['results'][:3]:  # Show first 3
        print(f"   - {atom['name']} (type: {atom['metadata'].get('entity_type')})")
    
    # Query 2: Find all events
    print("\n2. Query: FIND EVENT")
    result = system.query_hgnnql("FIND EVENT")
    print(f"   Found {result['count']} events")
    for atom in result['results']:
        print(f"   - {atom['name']}")
    
    # Query 3: Find relationships
    print("\n3. Query: FIND RELATIONSHIP")
    result = system.query_hgnnql("FIND RELATIONSHIP")
    print(f"   Found {result['count']} relationships")
    
    # Query 4: Find evidence
    print("\n4. Query: FIND EVIDENCE")
    result = system.query_hgnnql("FIND EVIDENCE")
    print(f"   Found {result['count']} evidence items")
    for atom in result['results']:
        status = atom['metadata'].get('verification_status', 'unknown')
        print(f"   - {atom['name'][:60]}... (status: {status})")


def demo_inference(system: OpenCogCaseLLM):
    """Demonstrate Hyper-Holmes inference engine"""
    print_section("Hyper-Holmes Inference Engine")
    
    print("\n1. Running forward chaining inference...")
    inference_results = system.run_inference(method="forward", max_iterations=5)
    print(f"   ✓ Completed {inference_results['iterations']} iterations")
    print(f"   ✓ Generated {inference_results['total_inferences']} new inferences")
    
    print("\n2. Detecting patterns in case data...")
    patterns = system.detect_patterns()
    print(f"   ✓ Detected {len(patterns)} patterns:")
    for i, pattern in enumerate(patterns[:3], 1):  # Show first 3
        print(f"   {i}. {pattern.get('pattern_type', 'unknown')}: "
              f"{pattern.get('description', 'No description')}")
    
    print("\n3. Generating hypotheses from evidence...")
    evidence_ids = ["evidence_001", "evidence_002"]
    hypotheses = system.generate_hypotheses(evidence_ids)
    print(f"   ✓ Generated {len(hypotheses)} hypotheses:")
    for i, hyp in enumerate(hypotheses, 1):
        print(f"   {i}. {hyp['hypothesis_type']}: {hyp['description']}")
        print(f"      Confidence: {hyp['confidence']:.2f}")


def demo_introspection(system: OpenCogCaseLLM):
    """Demonstrate Super-Sleuth introspection trainer"""
    print_section("Super-Sleuth Introspection Trainer")
    
    print("\n1. Training introspection system on case data...")
    training_summary = system.train_introspection()
    print(f"   ✓ Training completed in {training_summary['duration_seconds']:.2f} seconds")
    print(f"   ✓ Learned {training_summary['patterns_learned']} patterns")
    print(f"   ✓ Generated {training_summary['leads_generated']} investigation leads")
    
    print("\n2. Pattern breakdown by category:")
    for category, count in training_summary['pattern_breakdown'].items():
        if count > 0:
            print(f"   - {category}: {count}")
    
    print("\n3. Running introspective analysis...")
    introspection = system.introspect()
    
    print(f"\n4. Knowledge base metrics:")
    metrics = introspection['knowledge_base_metrics']
    print(f"   - Total atoms: {metrics['total_atoms']}")
    print(f"   - Entities: {metrics['entities']}")
    print(f"   - Events: {metrics['events']}")
    print(f"   - Relationships: {metrics['relationships']}")
    print(f"   - Evidence: {metrics['evidence']}")
    print(f"   - Average confidence: {metrics['average_confidence']:.3f}")
    
    print("\n5. Investigation leads generated:")
    leads = system.get_investigation_leads()
    for i, lead in enumerate(leads, 1):
        print(f"\n   Lead {i}: [{lead['priority']}] {lead['description']}")
        print(f"   Confidence: {lead['confidence']:.2f}")
        print(f"   Recommended actions:")
        for action in lead['recommended_actions'][:2]:  # Show first 2
            print(f"     • {action}")
    
    if introspection['knowledge_gaps']:
        print("\n6. Identified knowledge gaps:")
        for gap in introspection['knowledge_gaps']:
            print(f"   - [{gap['severity']}] {gap['description']}")


def demo_llm_interaction(system: OpenCogCaseLLM):
    """Demonstrate Case-LLM natural language interaction"""
    print_section("Case-LLM Natural Language Interface")
    
    print("\n1. Asking questions about the case...")
    
    questions = [
        "What entities are involved in this case?",
        "What suspicious activities have been detected?",
        "What is the timeline of events?",
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n   Q{i}: {question}")
        response = system.ask_llm(question)
        print(f"   Model: {response['model']}")
        print(f"   Context: {response['context']}")
        print(f"   Answer: {response['answer']}")
        print(f"   Confidence: {response['confidence']:.2f}")


def demo_complete_analysis(system: OpenCogCaseLLM):
    """Demonstrate complete analysis pipeline"""
    print_section("Complete Analysis Pipeline")
    
    print("\nRunning complete OpenCog Case-LLM analysis...")
    print("This includes:")
    print("  • Forward chaining inference")
    print("  • Pattern detection")
    print("  • Introspection training")
    print("  • Lead generation")
    
    report = system.run_complete_analysis()
    
    print("\n✓ Analysis complete!")
    print(f"\nSummary:")
    summary = report['summary']
    print(f"  • Inferences: {summary['total_inferences']}")
    print(f"  • Patterns detected: {summary['patterns_detected']}")
    print(f"  • Leads generated: {summary['leads_generated']}")
    print(f"  • Knowledge base size: {summary['knowledge_base_size']} atoms")
    print(f"  • Analysis duration: {report['duration_seconds']:.2f} seconds")


def demo_export(system: OpenCogCaseLLM):
    """Demonstrate exporting results"""
    print_section("Exporting Results")
    
    print("\n1. Exporting knowledge base...")
    system.export_knowledge_base()
    print("   ✓ Knowledge base exported")
    
    print("\n2. Exporting training results...")
    system.export_training_results()
    print("   ✓ Training results exported")
    
    print("\n3. System status:")
    status = system.get_system_status()
    print(f"   Case ID: {status['case_id']}")
    print(f"   AtomSpace: {status['atomspace']['total_atoms']} atoms")
    print(f"   Inference engine: {status['inference_engine']['total_rules']} rules")
    print(f"   Trainer: {status['trainer']['patterns_learned']} patterns learned")


def main():
    """Main demo function"""
    print("\n" + "🧠" * 35)
    print("  OpenCog HGNNQL Case-LLM Demonstration")
    print("  Integrating Knowledge Graphs, Inference, and Learning")
    print("🧠" * 35)
    
    # Run demos
    system = demo_basic_usage()
    demo_queries(system)
    demo_inference(system)
    demo_introspection(system)
    demo_llm_interaction(system)
    demo_complete_analysis(system)
    demo_export(system)
    
    print("\n" + "=" * 70)
    print("  ✓ Demo completed successfully!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  1. OpenCog-inspired AtomSpace provides flexible knowledge representation")
    print("  2. HGNNQL enables intuitive querying of case knowledge")
    print("  3. Hyper-Holmes performs automated inference and pattern detection")
    print("  4. Super-Sleuth learns patterns and generates investigation leads")
    print("  5. Case-LLM enables natural language interaction with case data")
    print("  6. Complete integration provides comprehensive AI-powered case analysis")
    
    print("\n📁 Output files saved to: ./output/opencog_demo/")
    print("\n")


if __name__ == "__main__":
    main()
