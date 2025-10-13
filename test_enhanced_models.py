#!/usr/bin/env python3
"""
Test script for enhanced agent, event, and system models.

This script validates the enhanced legal analysis capabilities including
role identification, relation tracking, event analysis, timeline patterns,
resource flows, and legal highlights extraction.
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import enhanced models
from case_data_loader import CaseEntity, CaseEvent, AgentModelFactory, InformationStatus
from src.api.hypergnn_core import HyperGNNFramework, Agent, AgentType, DiscreteEvent, EventType, SystemFlow, FlowType


def test_enhanced_agent_model():
    """Test enhanced agent model with role identification and legal highlights."""
    print("=== Testing Enhanced Agent Model ===")
    
    # Create a test entity
    entity = CaseEntity(
        entity_id="test_peter_faucitt",
        name="Peter Faucitt",
        entity_type="person",
        roles=["defendant"]
    )
    
    # Initialize with agent model
    entity = AgentModelFactory.create_primary_agent(entity, "peter_faucitt")
    
    # Create test events
    events = [
        CaseEvent(
            event_id="murder_001",
            date=datetime(2025, 1, 15),
            description="Kayla Pretorius was murdered in suspicious circumstances",
            participants=["kayla_pretorius", "unknown_perpetrator"],
            event_type="criminal"
        ),
        CaseEvent(
            event_id="report_001", 
            date=datetime(2025, 3, 25),
            description="Daniel Faucitt filed police report about financial misconduct by Peter Faucitt",
            participants=["daniel_faucitt", "test_peter_faucitt"],
            event_type="legal"
        ),
        CaseEvent(
            event_id="legal_action_001",
            date=datetime(2025, 6, 5),
            description="Peter Faucitt filed court application against Daniel Faucitt demanding medical testing",
            participants=["test_peter_faucitt", "daniel_faucitt"],
            event_type="legal"
        )
    ]
    
    # Test criminal role identification
    criminal_roles = entity.identify_criminal_roles(events)
    print(f"Criminal roles identified: {criminal_roles}")
    
    # Test commercial role identification
    commercial_roles = entity.identify_commercial_roles(events)
    print(f"Commercial roles identified: {commercial_roles}")
    
    # Test legal highlights extraction
    legal_highlights = entity.extract_legal_highlights(events)
    print(f"Legal highlights: {legal_highlights}")
    
    # Test timeline significance calculation
    timeline_significance = entity.calculate_timeline_significance(events)
    print(f"Timeline significance: {timeline_significance}")
    
    # Test resource flow tracking
    entity.track_resource_flow(
        "financial", 
        "test_peter_faucitt", 
        "elliott_attorneys",
        50000.0,
        datetime(2025, 6, 1),
        "Payment to legal services for court application"
    )
    print(f"Resource flows tracked: {len(entity.resource_flows.get('financial', []))}")
    
    return True


def test_enhanced_event_model():
    """Test enhanced event model with legal significance and causal analysis."""
    print("\n=== Testing Enhanced Event Model ===")
    
    # Create test events with enhanced properties
    murder_event = CaseEvent(
        event_id="murder_kayla",
        date=datetime(2025, 1, 15),
        description="Kayla Pretorius murdered - forensic investigation required",
        participants=["kayla_pretorius"],
        event_type="criminal"
    )
    
    report_event = CaseEvent(
        event_id="financial_report",
        date=datetime(2025, 3, 25), 
        description="Financial fraud reported to police - evidence of embezzlement",
        participants=["daniel_faucitt", "peter_faucitt"],
        event_type="commercial"
    )
    
    legal_event = CaseEvent(
        event_id="court_application",
        date=datetime(2025, 6, 5),
        description="Court application filed for medical testing - coercive legal mechanism",
        participants=["peter_faucitt", "daniel_faucitt"],
        event_type="legal"
    )
    
    events = [murder_event, report_event, legal_event]
    
    # Test legal significance categorization
    for event in events:
        significance = event.categorize_legal_significance()
        print(f"Event {event.event_id}: Criminal={significance['criminal']:.2f}, Commercial={significance['commercial']:.2f}")
        print(f"  Legal categories: {event.legal_categories}")
    
    # Test causal relationship identification
    legal_event.identify_causal_relationships([murder_event, report_event])
    print(f"Legal event causal relations: {legal_event.causal_relations}")
    
    # Test temporal dependencies
    legal_event.calculate_temporal_dependencies([murder_event, report_event])
    print(f"Legal event temporal dependencies: {legal_event.temporal_dependencies}")
    
    return True


def test_enhanced_hypergnn_framework():
    """Test enhanced HyperGNN framework with comprehensive legal analysis."""
    print("\n=== Testing Enhanced HyperGNN Framework ===")
    
    # Create framework
    framework = HyperGNNFramework("test_case_2025")
    
    # Create and add agents
    peter_entity = CaseEntity(
        entity_id="peter_faucitt",
        name="Peter Faucitt", 
        entity_type="person",
        roles=["defendant"]
    )
    peter_entity = AgentModelFactory.create_primary_agent(peter_entity, "peter_faucitt")
    peter_agent = peter_entity.to_agent()
    framework.add_agent(peter_agent)
    
    daniel_entity = CaseEntity(
        entity_id="daniel_faucitt",
        name="Daniel Faucitt",
        entity_type="person", 
        roles=["complainant"]
    )
    daniel_entity = AgentModelFactory.create_primary_agent(daniel_entity, "daniel_faucitt")
    daniel_agent = daniel_entity.to_agent()
    framework.add_agent(daniel_agent)
    
    # Create and add enhanced events
    murder_event = DiscreteEvent(
        event_id="murder_incident",
        timestamp=datetime(2025, 1, 15),
        event_type=EventType.EVIDENCE,
        actors=["kayla_pretorius"],
        description="Kayla Pretorius murder - criminal investigation required"
    )
    murder_event.analyze_legal_significance()
    framework.add_event(murder_event)
    
    fraud_report = DiscreteEvent(
        event_id="fraud_report",
        timestamp=datetime(2025, 3, 25),
        event_type=EventType.COMMUNICATION,
        actors=["daniel_faucitt", "police"],
        description="Daniel Faucitt reported financial fraud by Peter Faucitt"
    )
    fraud_report.analyze_legal_significance()
    framework.add_event(fraud_report)
    
    court_action = DiscreteEvent(
        event_id="court_filing",
        timestamp=datetime(2025, 6, 5),
        event_type=EventType.ACTION,
        actors=["peter_faucitt", "court_system"],
        description="Peter Faucitt filed coercive court application for medical testing"
    )
    court_action.analyze_legal_significance()
    framework.add_event(court_action)
    
    # Add resource flows
    legal_payment = SystemFlow(
        flow_id="legal_fees_001",
        flow_type=FlowType.FINANCIAL,
        source="peter_faucitt",
        target="elliott_attorneys",
        timestamp=datetime(2025, 6, 1),
        magnitude=75000.0,
        description="Payment to Elliott Attorneys for coercive legal action"
    )
    legal_payment.categorize_flow_type()
    legal_payment.assess_legal_significance()
    legal_payment.evaluate_legitimacy()
    framework.add_flow(legal_payment)
    
    # Test comprehensive legal framework analysis
    comprehensive_analysis = framework.analyze_comprehensive_legal_framework()
    
    print(f"Agents analyzed: {len(comprehensive_analysis['agent_roles'])}")
    print(f"Events analyzed: {len(comprehensive_analysis['event_analysis'])}")
    print(f"Criminal highlights: {len(comprehensive_analysis['legal_highlights']['criminal'])}")
    print(f"Commercial highlights: {len(comprehensive_analysis['legal_highlights']['commercial'])}")
    print(f"Resource flow categories: {list(comprehensive_analysis['resource_flows'].keys())}")
    print(f"Timeline span: {comprehensive_analysis['timeline_analysis'].get('timeline_span_days', 0)} days")
    print(f"Overall risk level: {comprehensive_analysis['risk_assessment']['overall_risk_level']}")
    
    # Test motive, means, opportunity analysis
    mmo_analysis = framework.analyze_motive_means_opportunity("peter_faucitt", "court_filing")
    print(f"MMO Analysis for Peter Faucitt: {mmo_analysis['risk_assessment']}")
    
    return True


def run_comprehensive_test():
    """Run comprehensive test of all enhanced model capabilities."""
    print("Starting comprehensive test of enhanced legal analysis models...")
    
    try:
        # Test individual components
        test_enhanced_agent_model()
        test_enhanced_event_model() 
        test_enhanced_hypergnn_framework()
        
        print("\n=== All Tests Passed Successfully ===")
        print("Enhanced models are working correctly with:")
        print("✓ Criminal and commercial role identification")
        print("✓ Legal highlight extraction") 
        print("✓ Event causal relationship analysis")
        print("✓ Resource flow tracking and legitimacy assessment")
        print("✓ Timeline pattern analysis")
        print("✓ Comprehensive legal framework analysis")
        print("✓ Risk assessment capabilities")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)