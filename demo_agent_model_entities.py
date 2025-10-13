#!/usr/bin/env python3
"""
Demonstration of Agent Model Implementation for Entities
=========================================================

This script demonstrates the newly implemented agent-based modeling 
capabilities for CaseEntity objects, showing how entities can be enhanced
with behavioral properties, decision-making rules, and strategic goals.
"""

import json
from datetime import datetime

from case_data_loader import AgentModelFactory, CaseEntity, InformationStatus


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def demonstrate_basic_agent_model():
    """Demonstrate basic agent model functionality"""
    print_section("1. Basic Agent Model Initialization")

    # Create a simple entity
    entity = CaseEntity(
        entity_id="demo_entity_001",
        name="Demo Person",
        entity_type="person",
        roles=["participant"],
    )

    print(f"Created entity: {entity.name}")
    print(f"Entity ID: {entity.entity_id}")
    print(f"Entity Type: {entity.entity_type}")

    # Initialize agent model
    entity.initialize_agent_model(
        legal_aggression=0.7,
        control_seeking=0.6,
        evidence_dismissal=0.4,
        vulnerability_to_pressure=0.5,
        ethical_compliance=0.8,
    )

    print("\nAgent Model Properties:")
    for prop, value in entity.behavioral_properties.items():
        print(f"  {prop}: {value:.2f}")

    return entity


def demonstrate_behavioral_rules(entity: CaseEntity):
    """Demonstrate adding and using behavioral rules"""
    print_section("2. Behavioral Rules")

    # Add behavioral rules
    entity.add_behavioral_rule("evidence presented", "analyze and respond")
    entity.add_behavioral_rule("challenged", "provide supporting documentation")
    entity.add_behavioral_rule("legal threat", "seek legal counsel")

    print("Added Behavioral Rules:")
    for i, rule in enumerate(entity.behavioral_rules, 1):
        print(f"  {i}. {rule}")


def demonstrate_strategic_goals(entity: CaseEntity):
    """Demonstrate adding strategic goals"""
    print_section("3. Strategic Goals")

    # Add strategic goals
    entity.add_strategic_goal("Maintain credibility")
    entity.add_strategic_goal("Protect personal interests")
    entity.add_strategic_goal("Support legal process")

    print("Strategic Goals:")
    for i, goal in enumerate(entity.strategic_goals, 1):
        print(f"  {i}. {goal}")


def demonstrate_state_management(entity: CaseEntity):
    """Demonstrate state management"""
    print_section("4. State Management")

    # Update state based on events
    print("Initial state:")
    print(f"  Active: {entity.current_state['active']}")
    print(f"  Events participated: {len(entity.current_state['events_participated'])}")

    # Simulate event participation
    entity.update_state(
        "event_001", {'status': 'provided_evidence', 'cooperation_level': 'high'}
    )

    entity.update_state(
        "event_002", {'status': 'attended_meeting', 'cooperation_level': 'high'}
    )

    print("\nAfter event participation:")
    print(f"  Events participated: {len(entity.current_state['events_participated'])}")
    print(
        f"  Events: {', '.join(entity.current_state['events_participated'])}"
    )
    print(f"  Status: {entity.current_state.get('status', 'N/A')}")
    print(
        f"  Cooperation level: {entity.current_state.get('cooperation_level', 'N/A')}"
    )
    print(f"  State history entries: {len(entity.state_history)}")


def demonstrate_decision_making(entity: CaseEntity):
    """Demonstrate decision-making capabilities"""
    print_section("5. Decision Making")

    # Make decisions based on different contexts
    contexts = [
        {'event': 'evidence presented', 'type': 'supporting'},
        {'event': 'legal threat', 'severity': 'high'},
        {'event': 'routine inquiry', 'priority': 'low'},
    ]

    print("Decision making for different contexts:\n")
    for i, context in enumerate(contexts, 1):
        decision = entity.make_decision(context)
        print(f"Context {i}: {context}")
        print(f"  Decision: {decision['decision']}")
        print(f"  Reasoning: {', '.join(decision['reasoning'])}")
        print()


def demonstrate_relationship_management(entity: CaseEntity):
    """Demonstrate relationship management"""
    print_section("6. Relationship Management")

    # Manage relationships with other entities
    other_entities = [
        ("entity_002", "colleague"),
        ("entity_003", "opponent"),
        ("entity_004", "neutral party"),
    ]

    print("Establishing relationships:\n")
    entity.update_relationship("entity_002", 0.3)  # Positive relationship
    entity.update_relationship("entity_003", -0.4)  # Negative relationship
    entity.update_relationship("entity_004", 0.0)  # Neutral relationship

    for entity_id, description in other_entities:
        strength = entity.get_relationship_strength(entity_id)
        print(f"  {description} ({entity_id}): {strength:.2f}")


def demonstrate_predefined_profiles():
    """Demonstrate creating entities with predefined agent profiles"""
    print_section("7. Predefined Agent Profiles")

    # Create entities with specific profiles
    profiles = [
        ("peter_faucitt", "Peter Faucitt", "person", "primary"),
        ("elliott_attorneys", "Elliott Attorneys", "organization", "secondary"),
        ("court_system", "Court System", "system", "institutional"),
    ]

    for profile_id, name, entity_type, category in profiles:
        entity = CaseEntity(
            entity_id=profile_id, name=name, entity_type=entity_type, roles=[]
        )

        if category == "primary":
            entity = AgentModelFactory.create_primary_agent(entity, profile_id)
        elif category == "secondary":
            entity = AgentModelFactory.create_secondary_agent(entity, profile_id)
        elif category == "institutional":
            entity = AgentModelFactory.create_institutional_agent(entity, profile_id)

        print(f"\n{name} ({entity_type}):")
        print(f"  Behavioral Properties:")
        for prop, value in list(entity.behavioral_properties.items())[:3]:
            print(f"    {prop}: {value:.2f}")
        print(f"  Behavioral Rules: {len(entity.behavioral_rules)}")
        print(f"  Strategic Goals: {len(entity.strategic_goals)}")
        if entity.strategic_goals:
            print(f"    Primary Goal: {entity.strategic_goals[0]}")


def demonstrate_agent_conversion(entity: CaseEntity):
    """Demonstrate converting CaseEntity to Agent for HyperGNN framework"""
    print_section("8. Converting to HyperGNN Agent")

    print(f"Converting {entity.name} to Agent object...")
    agent = entity.to_agent()

    print(f"\nAgent created:")
    print(f"  Agent ID: {agent.agent_id}")
    print(f"  Agent Type: {agent.agent_type.value}")
    print(f"  Name: {agent.name}")
    print(f"  Attributes keys: {list(agent.attributes.keys())}")
    print(f"\n  Agent can now be used in HyperGNN Framework for:")
    print(f"    - Timeline tensor generation")
    print(f"    - Multi-agent interaction modeling")
    print(f"    - System dynamics analysis")
    print(f"    - Network analysis and visualization")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 70)
    print("  AGENT MODEL IMPLEMENTATION FOR ENTITIES - DEMONSTRATION")
    print("=" * 70)

    # Run demonstrations
    entity = demonstrate_basic_agent_model()
    demonstrate_behavioral_rules(entity)
    demonstrate_strategic_goals(entity)
    demonstrate_state_management(entity)
    demonstrate_decision_making(entity)
    demonstrate_relationship_management(entity)
    demonstrate_predefined_profiles()
    demonstrate_agent_conversion(entity)

    print_section("Summary")
    print("The agent model implementation provides:")
    print("  ✓ Behavioral property modeling")
    print("  ✓ Rule-based decision making")
    print("  ✓ Strategic goal tracking")
    print("  ✓ State management with history")
    print("  ✓ Relationship strength tracking")
    print("  ✓ Predefined agent profiles based on case analysis")
    print("  ✓ Seamless conversion to HyperGNN Agent objects")
    print("\nThis enables comprehensive agent-based modeling for case analysis.")
    print()


if __name__ == "__main__":
    main()
