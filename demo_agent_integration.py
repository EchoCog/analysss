#!/usr/bin/env python3
"""
Demonstration of Agent Model Integration with Discrete Event Model
===================================================================

This script demonstrates how CaseEntity objects with agent models can be
integrated with the discrete event model for comprehensive case analysis.
"""

import sys
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, '/home/runner/work/analysis/analysis')

from case_data_loader import AgentModelFactory, CaseEntity, InformationStatus


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def create_case_entities_with_agent_models():
    """Create case entities with initialized agent models"""
    print_section("Creating Case Entities with Agent Models")
    
    entities = {}
    
    # Create Peter Faucitt entity with agent model
    peter = CaseEntity(
        entity_id="peter_faucitt",
        name="Peter Faucitt",
        entity_type="person",
        roles=["defendant", "business_owner"],
        verification_status=InformationStatus.VERIFIED
    )
    peter = AgentModelFactory.create_primary_agent(peter, "peter_faucitt")
    entities["peter_faucitt"] = peter
    
    print(f"Created: {peter.name}")
    print(f"  - Behavioral Properties: Legal Aggression={peter.behavioral_properties['legal_aggression']:.2f}")
    print(f"  - Behavioral Rules: {len(peter.behavioral_rules)}")
    print(f"  - Strategic Goals: {len(peter.strategic_goals)}")
    
    # Create Daniel Faucitt entity with agent model
    daniel = CaseEntity(
        entity_id="daniel_faucitt",
        name="Daniel Faucitt",
        entity_type="person",
        roles=["witness", "victim"],
        verification_status=InformationStatus.VERIFIED
    )
    daniel = AgentModelFactory.create_primary_agent(daniel, "daniel_faucitt")
    entities["daniel_faucitt"] = daniel
    
    print(f"\nCreated: {daniel.name}")
    print(f"  - Behavioral Properties: Ethical Compliance={daniel.behavioral_properties['ethical_compliance']:.2f}")
    print(f"  - Behavioral Rules: {len(daniel.behavioral_rules)}")
    print(f"  - Strategic Goals: {len(daniel.strategic_goals)}")
    
    # Create Elliott Attorneys entity with agent model
    elliott = CaseEntity(
        entity_id="elliott_attorneys",
        name="Elliott Attorneys",
        entity_type="organization",
        roles=["legal_counsel"],
        verification_status=InformationStatus.VERIFIED
    )
    elliott = AgentModelFactory.create_secondary_agent(elliott, "elliott_attorneys")
    entities["elliott_attorneys"] = elliott
    
    print(f"\nCreated: {elliott.name}")
    print(f"  - Behavioral Properties: Ethical Compliance={elliott.behavioral_properties['ethical_compliance']:.2f}")
    print(f"  - Behavioral Rules: {len(elliott.behavioral_rules)}")
    print(f"  - Strategic Goals: {len(elliott.strategic_goals)}")
    
    return entities


def demonstrate_agent_decision_simulation(entities):
    """Demonstrate simulating agent decisions"""
    print_section("Agent Decision Simulation")
    
    # Simulate different scenarios
    scenarios = [
        {
            "name": "Evidence Presented",
            "context": {"event": "evidence presented", "type": "contradictory"},
            "actors": ["peter_faucitt", "daniel_faucitt"]
        },
        {
            "name": "Legal Challenge",
            "context": {"event": "challenged", "severity": "high"},
            "actors": ["peter_faucitt", "elliott_attorneys"]
        },
        {
            "name": "Request for Documentation",
            "context": {"event": "attacked", "requirement": "comprehensive_evidence"},
            "actors": ["daniel_faucitt"]
        }
    ]
    
    for scenario in scenarios:
        print(f"\nScenario: {scenario['name']}")
        print(f"Context: {scenario['context']}")
        print("\nAgent Decisions:")
        
        for actor_id in scenario["actors"]:
            if actor_id in entities:
                entity = entities[actor_id]
                decision = entity.make_decision(scenario["context"])
                
                print(f"\n  {entity.name}:")
                print(f"    Decision: {decision['decision']}")
                print(f"    Reasoning: {', '.join(decision['reasoning'])}")


def demonstrate_state_tracking(entities):
    """Demonstrate tracking agent state through events"""
    print_section("Agent State Tracking Through Events")
    
    # Simulate a sequence of events
    events = [
        {
            "event_id": "event_001",
            "description": "First interdict filed",
            "actors": ["peter_faucitt", "daniel_faucitt"],
            "timestamp": datetime(2023, 1, 15)
        },
        {
            "event_id": "event_002",
            "description": "Evidence submitted by Daniel",
            "actors": ["daniel_faucitt", "elliott_attorneys"],
            "timestamp": datetime(2023, 2, 1)
        },
        {
            "event_id": "event_003",
            "description": "Second interdict filed",
            "actors": ["peter_faucitt", "daniel_faucitt"],
            "timestamp": datetime(2023, 3, 10)
        }
    ]
    
    print("Simulating event sequence:\n")
    
    for event in events:
        print(f"Event: {event['description']}")
        print(f"  Date: {event['timestamp'].strftime('%Y-%m-%d')}")
        print(f"  Actors: {', '.join(event['actors'])}")
        
        # Update state for each actor
        for actor_id in event["actors"]:
            if actor_id in entities:
                entity = entities[actor_id]
                entity.update_state(event["event_id"], {
                    "event_description": event["description"],
                    "timestamp": event["timestamp"]
                })
        print()
    
    # Show final states
    print("\nFinal Agent States:")
    for entity_id, entity in entities.items():
        if entity.current_state.get('events_participated'):
            print(f"\n{entity.name}:")
            print(f"  Events participated: {len(entity.current_state['events_participated'])}")
            print(f"  State history entries: {len(entity.state_history)}")
            if entity.state_history:
                last_event = entity.state_history[-1]
                print(f"  Last event: {last_event.get('event_id', 'N/A')}")


def demonstrate_relationship_dynamics(entities):
    """Demonstrate relationship dynamics between agents"""
    print_section("Agent Relationship Dynamics")
    
    # Initialize relationships based on case dynamics
    print("Initializing relationships based on case dynamics:\n")
    
    # Peter vs Daniel (adversarial)
    entities["peter_faucitt"].update_relationship("daniel_faucitt", -0.6)
    entities["daniel_faucitt"].update_relationship("peter_faucitt", -0.6)
    
    # Peter and Elliott (collaborative)
    entities["peter_faucitt"].update_relationship("elliott_attorneys", 0.4)
    entities["elliott_attorneys"].update_relationship("peter_faucitt", 0.4)
    
    # Daniel and Elliott (neutral to negative)
    entities["daniel_faucitt"].update_relationship("elliott_attorneys", -0.2)
    entities["elliott_attorneys"].update_relationship("daniel_faucitt", -0.2)
    
    # Display relationship matrix
    print("Relationship Strengths (0.0 = adversarial, 1.0 = collaborative):\n")
    
    entity_list = ["peter_faucitt", "daniel_faucitt", "elliott_attorneys"]
    for entity_id in entity_list:
        if entity_id in entities:
            entity = entities[entity_id]
            print(f"{entity.name}:")
            for other_id in entity_list:
                if other_id != entity_id:
                    strength = entity.get_relationship_strength(other_id)
                    other_name = entities[other_id].name
                    print(f"  → {other_name}: {strength:.2f}")


def demonstrate_strategic_goal_alignment(entities):
    """Demonstrate strategic goal alignment analysis"""
    print_section("Strategic Goal Alignment Analysis")
    
    print("Analyzing strategic goals for each agent:\n")
    
    for entity_id, entity in entities.items():
        if entity.strategic_goals:
            print(f"{entity.name}:")
            for i, goal in enumerate(entity.strategic_goals, 1):
                print(f"  {i}. {goal}")
            print()
    
    # Identify conflicting goals
    print("Goal Conflicts Identified:")
    print("  - Peter's goal to 'Neutralize witnesses' conflicts with")
    print("    Daniel's goal to 'Maintain credibility as witness'")
    print("  - Peter's goal to 'Maintain control over financial resources' conflicts with")
    print("    Daniel's goal to 'Expose financial misconduct'")


def demonstrate_behavioral_comparison(entities):
    """Demonstrate behavioral property comparison"""
    print_section("Behavioral Property Comparison")
    
    properties = [
        'legal_aggression',
        'control_seeking',
        'evidence_dismissal',
        'vulnerability_to_pressure',
        'ethical_compliance'
    ]
    
    print(f"{'Property':<30} {'Peter':<10} {'Daniel':<10} {'Elliott':<10}")
    print("-" * 70)
    
    for prop in properties:
        peter_val = entities["peter_faucitt"].behavioral_properties.get(prop, 0)
        daniel_val = entities["daniel_faucitt"].behavioral_properties.get(prop, 0)
        elliott_val = entities["elliott_attorneys"].behavioral_properties.get(prop, 0)
        
        print(f"{prop.replace('_', ' ').title():<30} {peter_val:<10.2f} {daniel_val:<10.2f} {elliott_val:<10.2f}")
    
    print("\nKey Observations:")
    print("  - Peter has significantly higher legal aggression and control seeking")
    print("  - Daniel has the highest ethical compliance")
    print("  - Elliott shows low ethical compliance despite professional role")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 70)
    print("  AGENT MODEL INTEGRATION DEMONSTRATION")
    print("=" * 70)
    
    # Create entities with agent models
    entities = create_case_entities_with_agent_models()
    
    # Run demonstrations
    demonstrate_agent_decision_simulation(entities)
    demonstrate_state_tracking(entities)
    demonstrate_relationship_dynamics(entities)
    demonstrate_strategic_goal_alignment(entities)
    demonstrate_behavioral_comparison(entities)
    
    print_section("Summary")
    print("This demonstration showed:")
    print("  ✓ Creating entities with predefined agent profiles")
    print("  ✓ Simulating agent decisions based on behavioral models")
    print("  ✓ Tracking agent state through event sequences")
    print("  ✓ Managing relationship dynamics between agents")
    print("  ✓ Analyzing strategic goal alignment and conflicts")
    print("  ✓ Comparing behavioral properties across agents")
    print("\nThese capabilities enable comprehensive agent-based modeling")
    print("for legal case analysis and simulation.")
    print()


if __name__ == "__main__":
    main()
