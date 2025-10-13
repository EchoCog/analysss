#!/usr/bin/env python3
"""
Demonstration of Enhanced Legal Analysis Capabilities

This script demonstrates the refined agent, event, and system models optimized 
for identification of roles, relations, events, timelines, resource stocks & flows,
and criminal & commercial legal highlights.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from case_data_loader import CaseEntity, CaseEvent, AgentModelFactory, InformationStatus
from src.api.hypergnn_core import HyperGNNFramework, Agent, AgentType, DiscreteEvent, EventType, SystemFlow, FlowType


def create_comprehensive_case_scenario():
    """Create a comprehensive case scenario demonstrating enhanced capabilities."""
    
    print("🏛️  Creating Comprehensive Legal Analysis Framework")
    print("="*60)
    
    # Initialize the framework
    framework = HyperGNNFramework("case_2025_137857_enhanced")
    
    # ===== AGENT CREATION AND ROLE IDENTIFICATION =====
    print("\n📋 1. AGENT CREATION AND ROLE IDENTIFICATION")
    print("-" * 50)
    
    # Create primary agents with enhanced behavioral modeling
    agents_to_create = [
        ("peter_faucitt", "Peter Faucitt", "person", "peter_faucitt"),
        ("jacqueline_faucitt", "Jacqueline Faucitt", "person", "jacqueline_faucitt"), 
        ("daniel_faucitt", "Daniel Faucitt", "person", "daniel_faucitt"),
    ]
    
    enhanced_entities = {}
    
    for entity_id, name, entity_type, profile in agents_to_create:
        entity = CaseEntity(
            entity_id=entity_id,
            name=name,
            entity_type=entity_type,
            roles=[]
        )
        
        # Apply agent behavioral model
        entity = AgentModelFactory.create_primary_agent(entity, profile)
        enhanced_entities[entity_id] = entity
        
        # Add to framework
        agent = entity.to_agent()
        framework.add_agent(agent)
        
        print(f"✅ Agent created: {name}")
        print(f"   Behavioral Profile: Aggression={entity.behavioral_properties.get('legal_aggression', 0):.1f}, "
              f"Ethics={entity.behavioral_properties.get('ethical_compliance', 0):.1f}")
    
    # ===== EVENT CREATION AND ANALYSIS =====
    print("\n📅 2. EVENT CREATION AND TIMELINE ANALYSIS") 
    print("-" * 50)
    
    # Create comprehensive event timeline
    timeline_events = [
        {
            "event_id": "kayla_murder",
            "timestamp": datetime(2025, 1, 15),
            "event_type": EventType.EVIDENCE,
            "actors": ["kayla_pretorius"],
            "description": "Kayla Pretorius murdered in suspicious circumstances - forensic investigation required, potential evidence tampering"
        },
        {
            "event_id": "financial_discovery", 
            "timestamp": datetime(2025, 2, 28),
            "event_type": EventType.EVIDENCE,
            "actors": ["daniel_faucitt"],
            "description": "Daniel Faucitt discovered financial fraud and embezzlement by Peter Faucitt - documentary evidence collected"
        },
        {
            "event_id": "police_report",
            "timestamp": datetime(2025, 3, 25), 
            "event_type": EventType.COMMUNICATION,
            "actors": ["daniel_faucitt", "police"],
            "description": "Daniel Faucitt filed police report about Peter Faucitt's financial misconduct and potential connection to murder"
        },
        {
            "event_id": "email_hijacking",
            "timestamp": datetime(2025, 4, 10),
            "event_type": EventType.EVIDENCE,
            "actors": ["rynette_farrar", "peter_faucitt"],
            "description": "Rynette Farrar hijacked Peter Faucitt's emails enabling evidence interception and information control"
        },
        {
            "event_id": "legal_counter_attack",
            "timestamp": datetime(2025, 6, 5),
            "event_type": EventType.ACTION, 
            "actors": ["peter_faucitt", "court_system"],
            "description": "Peter Faucitt filed coercive court application against Daniel demanding medical testing - weaponized legal system"
        },
        {
            "event_id": "settlement_coercion",
            "timestamp": datetime(2025, 7, 15),
            "event_type": EventType.TRANSACTION,
            "actors": ["peter_faucitt", "jacqueline_faucitt", "elliott_attorneys"],
            "description": "Coercive settlement agreement drafted with hidden medical testing obligations - legal manipulation"
        }
    ]
    
    # Create and analyze events
    case_events = []
    for event_data in timeline_events:
        # Create DiscreteEvent for framework
        discrete_event = DiscreteEvent(**event_data)
        discrete_event.analyze_legal_significance()
        discrete_event.calculate_timeline_criticality(timeline_events)
        framework.add_event(discrete_event)
        
        # Create CaseEvent for entity analysis
        case_event = CaseEvent(
            event_id=event_data["event_id"],
            date=event_data["timestamp"],
            description=event_data["description"],
            participants=event_data["actors"],
            event_type="legal"
        )
        case_event.categorize_legal_significance()
        case_events.append(case_event)
        
        print(f"📝 Event: {event_data['event_id']}")
        print(f"   Criminal Significance: {discrete_event.criminal_significance:.2f}")
        print(f"   Commercial Significance: {discrete_event.commercial_significance:.2f}")
        print(f"   Timeline Criticality: {discrete_event.timeline_criticality:.2f}")
    
    # ===== ROLE IDENTIFICATION =====
    print("\n🎭 3. COMPREHENSIVE ROLE IDENTIFICATION")
    print("-" * 50)
    
    for entity_id, entity in enhanced_entities.items():
        print(f"\nAgent: {entity.name}")
        
        # Identify criminal roles
        criminal_roles = entity.identify_criminal_roles(case_events)
        significant_criminal_roles = {k: v for k, v in criminal_roles.items() if v > 0.2}
        if significant_criminal_roles:
            print(f"  🔴 Criminal Roles: {significant_criminal_roles}")
        
        # Identify commercial roles
        commercial_roles = entity.identify_commercial_roles(case_events)
        significant_commercial_roles = {k: v for k, v in commercial_roles.items() if v > 0.2}
        if significant_commercial_roles:
            print(f"  💼 Commercial Roles: {significant_commercial_roles}")
        
        # Extract legal highlights
        legal_highlights = entity.extract_legal_highlights(case_events)
        if legal_highlights['criminal']:
            print(f"  ⚖️  Criminal Highlights: {len(legal_highlights['criminal'])} items")
        if legal_highlights['commercial']:
            print(f"  💰 Commercial Highlights: {len(legal_highlights['commercial'])} items")
    
    # ===== RESOURCE FLOWS AND STOCKS =====
    print("\n💸 4. RESOURCE STOCKS AND FLOWS ANALYSIS")
    print("-" * 50)
    
    # Create comprehensive resource flows
    resource_flows = [
        {
            "flow_id": "legal_fees_payment",
            "flow_type": FlowType.FINANCIAL,
            "source": "peter_faucitt",
            "target": "elliott_attorneys", 
            "timestamp": datetime(2025, 6, 1),
            "magnitude": 125000.0,
            "description": "Payment to Elliott Attorneys for coercive legal mechanisms and court applications"
        },
        {
            "flow_id": "medical_testing_funds",
            "flow_type": FlowType.FINANCIAL,
            "source": "peter_faucitt",
            "target": "medical_professionals",
            "timestamp": datetime(2025, 7, 20),
            "magnitude": 35000.0,
            "description": "Payment for weaponized medical testing with predetermined outcomes"
        },
        {
            "flow_id": "evidence_interception",
            "flow_type": FlowType.INFORMATION,
            "source": "daniel_faucitt",
            "target": "rynette_farrar",
            "timestamp": datetime(2025, 4, 10),
            "magnitude": 100.0,  # Information flow magnitude
            "description": "Unauthorized interception of evidence communications through email hijacking"
        },
        {
            "flow_id": "coercive_control",
            "flow_type": FlowType.INFLUENCE,
            "source": "peter_faucitt", 
            "target": "jacqueline_faucitt",
            "timestamp": datetime(2025, 7, 15),
            "magnitude": 80.0,
            "description": "Coercive control through legal mechanisms and settlement obligations"
        }
    ]
    
    # Analyze resource flows
    for flow_data in resource_flows:
        system_flow = SystemFlow(**flow_data)
        
        # Enhanced analysis
        category = system_flow.categorize_flow_type()
        legitimacy = system_flow.evaluate_legitimacy()
        legal_significance = system_flow.assess_legal_significance()
        impact = system_flow.calculate_impact_assessment()
        
        framework.add_flow(system_flow)
        
        print(f"💰 Flow: {flow_data['flow_id']}")
        print(f"   Category: {category}")
        print(f"   Legitimacy: {legitimacy:.2f}")
        print(f"   Legal Significance: {legal_significance:.2f}")
        print(f"   Impact Assessment: {impact}")
    
    # ===== COMPREHENSIVE LEGAL ANALYSIS =====
    print("\n⚖️  5. COMPREHENSIVE LEGAL FRAMEWORK ANALYSIS")
    print("-" * 50)
    
    comprehensive_analysis = framework.analyze_comprehensive_legal_framework()
    
    # Display key insights
    print(f"📊 Analysis Summary:")
    print(f"   Total Agents: {len(comprehensive_analysis['agent_roles'])}")
    print(f"   Total Events: {len(comprehensive_analysis['event_analysis'])}")
    print(f"   Timeline Span: {comprehensive_analysis['timeline_analysis']['timeline_span_days']} days")
    print(f"   Criminal Highlights: {len(comprehensive_analysis['legal_highlights']['criminal'])}")
    print(f"   Commercial Highlights: {len(comprehensive_analysis['legal_highlights']['commercial'])}")
    print(f"   Causal Chains: {len(comprehensive_analysis['causal_chains'])}")
    print(f"   Overall Risk Level: {comprehensive_analysis['risk_assessment']['overall_risk_level'].upper()}")
    
    # ===== DETAILED INSIGHTS =====
    print(f"\n🔍 6. DETAILED LEGAL INSIGHTS")
    print("-" * 50)
    
    # Criminal insights
    criminal_highlights = comprehensive_analysis['legal_highlights']['criminal']
    if criminal_highlights:
        print("🔴 CRIMINAL LAW HIGHLIGHTS:")
        for highlight in criminal_highlights[:3]:  # Show top 3
            print(f"   • {highlight['description']}")
            print(f"     Significance: {highlight['significance']:.2f}, Date: {highlight['timestamp'][:10]}")
    
    # Commercial insights
    commercial_highlights = comprehensive_analysis['legal_highlights']['commercial']
    if commercial_highlights:
        print("\n💼 COMMERCIAL LAW HIGHLIGHTS:")
        for highlight in commercial_highlights[:3]:  # Show top 3
            print(f"   • {highlight['description']}")
            print(f"     Significance: {highlight['significance']:.2f}, Date: {highlight['timestamp'][:10]}")
    
    # Risk assessment details
    risks = comprehensive_analysis['risk_assessment']
    print(f"\n⚠️  RISK ASSESSMENT:")
    for risk_category in ['criminal_risks', 'commercial_risks', 'procedural_risks']:
        if risks.get(risk_category):
            print(f"   {risk_category.replace('_', ' ').title()}:")
            for risk in risks[risk_category]:
                print(f"     • {risk['description']} (Severity: {risk['severity']})")
    
    # ===== EXPORT RESULTS =====
    print(f"\n📄 7. EXPORTING ANALYSIS RESULTS")
    print("-" * 50)
    
    # Export comprehensive analysis
    output_file = "enhanced_legal_analysis_report.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        # Convert datetime objects to strings for JSON serialization
        def datetime_converter(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object {obj} is not JSON serializable")
        
        json.dump(comprehensive_analysis, f, indent=2, default=datetime_converter, ensure_ascii=False)
    
    print(f"✅ Analysis exported to: {output_file}")
    print(f"📊 Report contains {len(comprehensive_analysis)} main analysis sections")
    
    return comprehensive_analysis


def demonstrate_motive_means_opportunity():
    """Demonstrate enhanced MMO analysis capabilities."""
    print(f"\n🔎 MOTIVE, MEANS, OPPORTUNITY ANALYSIS")
    print("-" * 50)
    
    framework = HyperGNNFramework("mmo_demo")
    
    # Create agent with enhanced behavioral profile
    peter_entity = CaseEntity(
        entity_id="peter_faucitt",
        name="Peter Faucitt",
        entity_type="person",
        roles=["defendant"]
    )
    peter_entity = AgentModelFactory.create_primary_agent(peter_entity, "peter_faucitt")
    peter_agent = peter_entity.to_agent()
    framework.add_agent(peter_agent)
    
    # Create high-significance event
    coercive_action = DiscreteEvent(
        event_id="coercive_legal_action",
        timestamp=datetime(2025, 6, 5),
        event_type=EventType.ACTION,
        actors=["peter_faucitt", "court_system"],
        description="Filed coercive court application to weaponize medical testing against complainant"
    )
    framework.add_event(coercive_action)
    
    # Perform MMO analysis
    mmo_analysis = framework.analyze_motive_means_opportunity("peter_faucitt", "coercive_legal_action")
    
    print("🎯 MMO Analysis Results:")
    print(f"   Agent: {mmo_analysis['agent']}")
    print(f"   Risk Assessment: {mmo_analysis['risk_assessment'].upper()}")
    print(f"   Motive Indicators ({len(mmo_analysis['motive_indicators'])}):")
    for motive in mmo_analysis['motive_indicators']:
        print(f"     • {motive}")
    print(f"   Means Available ({len(mmo_analysis['means_available'])}):")
    for means in mmo_analysis['means_available']:
        print(f"     • {means}")
    print(f"   Opportunity Factors ({len(mmo_analysis['opportunity_factors'])}):")
    for opportunity in mmo_analysis['opportunity_factors']:
        print(f"     • {opportunity}")


def main():
    """Main demonstration function."""
    print("🚀 ENHANCED LEGAL ANALYSIS FRAMEWORK DEMONSTRATION")
    print("=" * 70)
    print("Demonstrating refined agent, event, and system models optimized for:")
    print("• Role identification (criminal & commercial)")
    print("• Relation tracking and causal analysis") 
    print("• Event timeline and significance analysis")
    print("• Resource stocks and flows monitoring")
    print("• Legal highlights extraction")
    print("• Comprehensive risk assessment")
    
    try:
        # Run comprehensive scenario
        analysis_results = create_comprehensive_case_scenario()
        
        # Demonstrate MMO analysis
        demonstrate_motive_means_opportunity()
        
        print(f"\n🎉 DEMONSTRATION COMPLETED SUCCESSFULLY")
        print("-" * 50)
        print("✅ All enhanced capabilities demonstrated:")
        print("   • Agent behavioral modeling with role identification")
        print("   • Event legal significance categorization") 
        print("   • Resource flow legitimacy assessment")
        print("   • Timeline pattern analysis")
        print("   • Comprehensive legal framework analysis")
        print("   • Enhanced MMO analysis")
        print("   • Risk assessment and reporting")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)