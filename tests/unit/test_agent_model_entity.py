#!/usr/bin/env python3
"""
Unit tests for Agent Model implementation for CaseEntity
"""

import unittest
from datetime import datetime

from case_data_loader import (
    AgentModelFactory,
    CaseEntity,
    InformationStatus,
)


class TestCaseEntityAgentModel(unittest.TestCase):
    """Test cases for CaseEntity agent model functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.entity = CaseEntity(
            entity_id="test_person_001",
            name="Test Person",
            entity_type="person",
            roles=["plaintiff"],
        )

    def test_initialize_agent_model(self):
        """Test initializing agent model properties"""
        self.entity.initialize_agent_model(
            legal_aggression=0.8,
            control_seeking=0.7,
            evidence_dismissal=0.6,
            vulnerability_to_pressure=0.5,
            ethical_compliance=0.4,
        )

        self.assertIsNotNone(self.entity.behavioral_properties)
        self.assertEqual(self.entity.behavioral_properties['legal_aggression'], 0.8)
        self.assertEqual(self.entity.behavioral_properties['control_seeking'], 0.7)
        self.assertEqual(self.entity.behavioral_properties['evidence_dismissal'], 0.6)
        self.assertEqual(
            self.entity.behavioral_properties['vulnerability_to_pressure'], 0.5
        )
        self.assertEqual(self.entity.behavioral_properties['ethical_compliance'], 0.4)
        self.assertIsNotNone(self.entity.current_state)

    def test_add_behavioral_rule(self):
        """Test adding behavioral rules"""
        self.entity.initialize_agent_model()
        self.entity.add_behavioral_rule("challenged", "escalate")

        self.assertEqual(len(self.entity.behavioral_rules), 1)
        self.assertIn("IF challenged THEN escalate", self.entity.behavioral_rules)

        # Test duplicate prevention
        self.entity.add_behavioral_rule("challenged", "escalate")
        self.assertEqual(len(self.entity.behavioral_rules), 1)

    def test_add_strategic_goal(self):
        """Test adding strategic goals"""
        self.entity.initialize_agent_model()
        self.entity.add_strategic_goal("Maintain control")

        self.assertEqual(len(self.entity.strategic_goals), 1)
        self.assertIn("Maintain control", self.entity.strategic_goals)

        # Test duplicate prevention
        self.entity.add_strategic_goal("Maintain control")
        self.assertEqual(len(self.entity.strategic_goals), 1)

    def test_update_state(self):
        """Test updating agent state"""
        self.entity.initialize_agent_model()
        initial_timestamp = self.entity.current_state['timestamp']

        self.entity.update_state(
            "event_001", {'new_property': 'test_value', 'events_participated': []}
        )

        self.assertEqual(self.entity.current_state['new_property'], 'test_value')
        self.assertIn("event_001", self.entity.current_state['events_participated'])
        self.assertEqual(len(self.entity.state_history), 1)
        self.assertGreater(
            self.entity.current_state['timestamp'], initial_timestamp
        )

    def test_make_decision(self):
        """Test decision making based on behavioral properties"""
        self.entity.initialize_agent_model(legal_aggression=0.9)
        self.entity.add_behavioral_rule("evidence presented", "escalate legally")

        context = {'event': 'evidence presented', 'type': 'contradictory'}
        decision = self.entity.make_decision(context)

        self.assertIsNotNone(decision)
        self.assertIn('decision', decision)
        self.assertIn('reasoning', decision)
        self.assertIsInstance(decision['reasoning'], list)

    def test_relationship_management(self):
        """Test relationship strength management"""
        self.entity.initialize_agent_model()

        # Test getting initial relationship (should default to 0.0)
        strength = self.entity.get_relationship_strength("other_entity")
        self.assertEqual(strength, 0.0)

        # Test updating relationship
        self.entity.update_relationship("other_entity", 0.3)
        strength = self.entity.get_relationship_strength("other_entity")
        self.assertEqual(strength, 0.8)  # 0.5 default + 0.3

        # Test bounds (should not exceed 1.0)
        self.entity.update_relationship("other_entity", 0.5)
        strength = self.entity.get_relationship_strength("other_entity")
        self.assertEqual(strength, 1.0)

        # Test lower bound (should not go below 0.0)
        self.entity.update_relationship("other_entity", -2.0)
        strength = self.entity.get_relationship_strength("other_entity")
        self.assertEqual(strength, 0.0)

    def test_to_agent_conversion(self):
        """Test converting CaseEntity to Agent"""
        self.entity.initialize_agent_model(legal_aggression=0.8)
        self.entity.add_behavioral_rule("challenged", "escalate")
        self.entity.add_strategic_goal("Maintain control")

        agent = self.entity.to_agent()

        self.assertEqual(agent.agent_id, self.entity.entity_id)
        self.assertEqual(agent.name, self.entity.name)
        self.assertIn('behavioral_properties', agent.attributes)
        self.assertIn('behavioral_rules', agent.attributes)
        self.assertIn('strategic_goals', agent.attributes)


class TestAgentModelFactory(unittest.TestCase):
    """Test cases for AgentModelFactory"""

    def test_create_primary_agent_peter_faucitt(self):
        """Test creating Peter Faucitt agent profile"""
        entity = CaseEntity(
            entity_id="peter_faucitt",
            name="Peter Faucitt",
            entity_type="person",
            roles=["defendant"],
        )

        enhanced_entity = AgentModelFactory.create_primary_agent(
            entity, "peter_faucitt"
        )

        self.assertIsNotNone(enhanced_entity.behavioral_properties)
        self.assertGreater(
            enhanced_entity.behavioral_properties['legal_aggression'], 0.8
        )
        self.assertGreater(
            enhanced_entity.behavioral_properties['control_seeking'], 0.9
        )
        self.assertGreater(len(enhanced_entity.behavioral_rules), 0)
        self.assertGreater(len(enhanced_entity.strategic_goals), 0)
        self.assertIn(
            "Maintain control over financial resources",
            enhanced_entity.strategic_goals,
        )

    def test_create_primary_agent_jacqueline_faucitt(self):
        """Test creating Jacqueline Faucitt agent profile"""
        entity = CaseEntity(
            entity_id="jacqueline_faucitt",
            name="Jacqueline Faucitt",
            entity_type="person",
            roles=["witness"],
        )

        enhanced_entity = AgentModelFactory.create_primary_agent(
            entity, "jacqueline_faucitt"
        )

        self.assertIsNotNone(enhanced_entity.behavioral_properties)
        self.assertGreater(
            enhanced_entity.behavioral_properties['vulnerability_to_pressure'], 0.7
        )
        self.assertGreater(
            enhanced_entity.behavioral_properties['ethical_compliance'], 0.6
        )
        self.assertIn("Protect personal interests", enhanced_entity.strategic_goals)

    def test_create_primary_agent_daniel_faucitt(self):
        """Test creating Daniel Faucitt agent profile"""
        entity = CaseEntity(
            entity_id="daniel_faucitt",
            name="Daniel Faucitt",
            entity_type="person",
            roles=["witness"],
        )

        enhanced_entity = AgentModelFactory.create_primary_agent(
            entity, "daniel_faucitt"
        )

        self.assertIsNotNone(enhanced_entity.behavioral_properties)
        self.assertGreater(
            enhanced_entity.behavioral_properties['ethical_compliance'], 0.8
        )
        self.assertIn(
            "Expose financial misconduct and serious crimes",
            enhanced_entity.strategic_goals,
        )

    def test_create_secondary_agent_elliott_attorneys(self):
        """Test creating Elliott Attorneys agent profile"""
        entity = CaseEntity(
            entity_id="elliott_attorneys",
            name="Elliott Attorneys",
            entity_type="organization",
            roles=["legal_counsel"],
        )

        enhanced_entity = AgentModelFactory.create_secondary_agent(
            entity, "elliott_attorneys"
        )

        self.assertIsNotNone(enhanced_entity.behavioral_properties)
        self.assertGreater(
            enhanced_entity.behavioral_properties['legal_aggression'], 0.7
        )
        self.assertIn(
            "Serve client interests regardless of ethics",
            enhanced_entity.strategic_goals,
        )

    def test_create_secondary_agent_ens_africa(self):
        """Test creating ENS Africa agent profile"""
        entity = CaseEntity(
            entity_id="ens_africa",
            name="ENS Africa",
            entity_type="organization",
            roles=["legal_counsel"],
        )

        enhanced_entity = AgentModelFactory.create_secondary_agent(entity, "ens_africa")

        self.assertIsNotNone(enhanced_entity.behavioral_properties)
        self.assertIn("Maintain client relationship", enhanced_entity.strategic_goals)

    def test_create_secondary_agent_medical_professionals(self):
        """Test creating Medical Professionals agent profile"""
        entity = CaseEntity(
            entity_id="medical_prof",
            name="Medical Professional",
            entity_type="person",
            roles=["medical_examiner"],
        )

        enhanced_entity = AgentModelFactory.create_secondary_agent(
            entity, "medical_professionals"
        )

        self.assertIsNotNone(enhanced_entity.behavioral_properties)
        self.assertIn("Generate professional fees", enhanced_entity.strategic_goals)

    def test_create_institutional_agent_court_system(self):
        """Test creating Court System agent profile"""
        entity = CaseEntity(
            entity_id="court",
            name="Court System",
            entity_type="system",
            roles=["judicial"],
        )

        enhanced_entity = AgentModelFactory.create_institutional_agent(
            entity, "court_system"
        )

        self.assertIsNotNone(enhanced_entity.behavioral_properties)
        self.assertGreater(
            enhanced_entity.behavioral_properties['ethical_compliance'], 0.7
        )
        self.assertIn("Uphold legal procedures", enhanced_entity.strategic_goals)

    def test_create_institutional_agent_forensic_investigators(self):
        """Test creating Forensic Investigators agent profile"""
        entity = CaseEntity(
            entity_id="forensic",
            name="Forensic Investigators",
            entity_type="organization",
            roles=["investigator"],
        )

        enhanced_entity = AgentModelFactory.create_institutional_agent(
            entity, "forensic_investigators"
        )

        self.assertIsNotNone(enhanced_entity.behavioral_properties)
        self.assertIn(
            "Complete investigation within parameters",
            enhanced_entity.strategic_goals,
        )


if __name__ == "__main__":
    unittest.main()
