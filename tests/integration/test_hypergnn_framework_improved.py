#!/usr/bin/env python3
"""
Test Suite for Enhanced HyperGNN Framework
=========================================

Comprehensive unit and integration tests for the improved HyperGNN framework.
"""

import json
import os
import shutil
import tempfile
import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

# Import the enhanced framework
from hypergnn_framework_improved import (
    AnalysisConfiguration,
    AnalysisScope,
    ComplexityLevel,
    ComponentFactory,
    DataIntegrationLayer,
    HyperGNNFramework,
    RiskLevel,
    RulesEngine,
)


class TestAnalysisConfiguration(unittest.TestCase):
    """Test cases for AnalysisConfiguration class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_valid_configuration(self):
        """Test creating a valid configuration."""
        config = AnalysisConfiguration(
            case_id="test_case_001",
            scope=AnalysisScope.COMPREHENSIVE,
            complexity_level=ComplexityLevel.ADVANCED,
            output_directory=self.temp_dir,
        )

        self.assertEqual(config.case_id, "test_case_001")
        self.assertEqual(config.scope, AnalysisScope.COMPREHENSIVE)
        self.assertEqual(config.complexity_level, ComplexityLevel.ADVANCED)
        self.assertEqual(config.output_directory, self.temp_dir)
        self.assertTrue(config.professional_standards)
        self.assertTrue(config.enable_logging)
        self.assertTrue(config.backup_enabled)

    def test_empty_case_id_raises_error(self):
        """Test that empty case_id raises ValueError."""
        with self.assertRaises(ValueError) as context:
            AnalysisConfiguration(
                case_id="",
                scope=AnalysisScope.INDIVIDUAL,
                complexity_level=ComplexityLevel.BASIC,
                output_directory=self.temp_dir,
            )
        self.assertIn("case_id cannot be empty", str(context.exception))

    def test_empty_output_directory_raises_error(self):
        """Test that empty output_directory raises ValueError."""
        with self.assertRaises(ValueError) as context:
            AnalysisConfiguration(
                case_id="test_case",
                scope=AnalysisScope.INDIVIDUAL,
                complexity_level=ComplexityLevel.BASIC,
                output_directory="",
            )
        self.assertIn("output_directory is required", str(context.exception))

    def test_output_directory_creation(self):
        """Test that output directory is created if it doesn't exist."""
        non_existent_dir = os.path.join(self.temp_dir, "new_directory")
        self.assertFalse(os.path.exists(non_existent_dir))

        config = AnalysisConfiguration(
            case_id="test_case",
            scope=AnalysisScope.INDIVIDUAL,
            complexity_level=ComplexityLevel.BASIC,
            output_directory=non_existent_dir,
        )

        self.assertTrue(os.path.exists(non_existent_dir))


class TestRulesEngine(unittest.TestCase):
    """Test cases for RulesEngine class."""

    def setUp(self):
        """Set up test fixtures."""
        self.rules_engine = RulesEngine()

    def test_risk_level_assessment(self):
        """Test risk level assessment based on risk factors."""
        test_cases = [
            (0, RiskLevel.MINIMAL),
            (1, RiskLevel.MINIMAL),
            (2, RiskLevel.LOW),
            (3, RiskLevel.LOW),
            (4, RiskLevel.MODERATE),
            (5, RiskLevel.MODERATE),
            (6, RiskLevel.HIGH),
            (7, RiskLevel.HIGH),
            (8, RiskLevel.CRITICAL),
            (10, RiskLevel.CRITICAL),
        ]

        for risk_factors, expected_level in test_cases:
            with self.subTest(risk_factors=risk_factors):
                result = self.rules_engine.assess_risk_level(risk_factors)
                self.assertEqual(result, expected_level)

    def test_assessment_generation(self):
        """Test professional assessment text generation."""
        assessment = self.rules_engine.generate_assessment(RiskLevel.HIGH)
        self.assertIsInstance(assessment, str)
        self.assertIn("elevated risk factors", assessment.lower())

    def test_recommendations_generation(self):
        """Test recommendations generation."""
        recommendations = self.rules_engine.generate_recommendations(RiskLevel.MODERATE)
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)

        # Test that we get a copy, not the original list
        original_length = len(recommendations)
        recommendations.append("test")
        new_recommendations = self.rules_engine.generate_recommendations(
            RiskLevel.MODERATE
        )
        self.assertEqual(len(new_recommendations), original_length)


class TestDataIntegrationLayer(unittest.TestCase):
    """Test cases for DataIntegrationLayer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = AnalysisConfiguration(
            case_id="test_case",
            scope=AnalysisScope.INDIVIDUAL,
            complexity_level=ComplexityLevel.BASIC,
            output_directory=self.temp_dir,
        )
        self.data_integration = DataIntegrationLayer(self.config)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_successful_data_integration(self):
        """Test successful data integration."""
        test_data = {
            "entities": {
                "entity1": {"name": "Test Entity"},
                "entity2": {"name": "Another Entity"},
            },
            "events": [{"id": "event1", "description": "Test Event"}],
            "metadata": {"source": "test"},
        }

        result = self.data_integration.integrate_data(test_data)

        self.assertTrue(result["success"])
        self.assertEqual(result["entities_processed"], 2)
        self.assertEqual(result["events_processed"], 1)
        self.assertIn("integration_timestamp", result)

    def test_empty_data_integration(self):
        """Test integration with empty data."""
        test_data = {}

        result = self.data_integration.integrate_data(test_data)

        self.assertTrue(result["success"])
        self.assertEqual(result["entities_processed"], 0)
        self.assertEqual(result["events_processed"], 0)


class TestComponentFactory(unittest.TestCase):
    """Test cases for ComponentFactory class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = AnalysisConfiguration(
            case_id="test_case",
            scope=AnalysisScope.INDIVIDUAL,
            complexity_level=ComplexityLevel.BASIC,
            output_directory=self.temp_dir,
        )
        self.factory = ComponentFactory(self.config)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("hypergnn_framework_improved.EvidenceManagementSystem")
    def test_create_evidence_component(self, mock_evidence_class):
        """Test creating evidence component."""
        mock_instance = Mock()
        mock_evidence_class.return_value = mock_instance

        component = self.factory.create_component("evidence")

        self.assertIsNotNone(component)
        mock_evidence_class.assert_called_once_with(self.config.output_directory)

    def test_create_unknown_component(self):
        """Test creating unknown component type."""
        component = self.factory.create_component("unknown_type")
        self.assertIsNone(component)

    def test_get_component_creates_if_not_exists(self):
        """Test that get_component creates component if it doesn't exist."""
        with patch.object(self.factory, "create_component") as mock_create:
            mock_create.return_value = Mock()

            component = self.factory.get_component("test_type")

            mock_create.assert_called_once_with("test_type")

    def test_get_all_components(self):
        """Test getting all components returns a copy."""
        # Add a mock component
        mock_component = Mock()
        self.factory._components["test"] = mock_component

        components = self.factory.get_all_components()

        self.assertIn("test", components)
        self.assertEqual(components["test"], mock_component)

        # Modify the returned dict and ensure original is unchanged
        components["new"] = Mock()
        self.assertNotIn("new", self.factory._components)


class TestHyperGNNFramework(unittest.TestCase):
    """Test cases for HyperGNNFramework class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = AnalysisConfiguration(
            case_id="test_case_framework",
            scope=AnalysisScope.COMPREHENSIVE,
            complexity_level=ComplexityLevel.ADVANCED,
            output_directory=self.temp_dir,
        )

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("hypergnn_framework_improved.ComponentFactory")
    def test_framework_initialization(self, mock_factory_class):
        """Test framework initialization."""
        mock_factory = Mock()
        mock_factory_class.return_value = mock_factory

        framework = HyperGNNFramework(self.config)

        self.assertEqual(framework.config, self.config)
        self.assertIsNotNone(framework.component_factory)
        self.assertIsNotNone(framework.data_integration)
        self.assertIsNotNone(framework.rules_engine)

    @patch("hypergnn_framework_improved.ComponentFactory")
    def test_add_agent_success(self, mock_factory_class):
        """Test successful agent addition."""
        mock_factory = Mock()
        mock_dynamics = Mock()
        mock_evidence = Mock()

        mock_factory.get_component.side_effect = lambda comp_type: {
            "dynamics": mock_dynamics,
            "evidence": mock_evidence,
        }.get(comp_type)

        mock_factory_class.return_value = mock_factory

        framework = HyperGNNFramework(self.config)

        result = framework.add_agent(
            "agent_001", "Test Agent", "individual", {"attr": "value"}
        )

        self.assertTrue(result)
        self.assertEqual(mock_factory.get_component.call_count, 2)

    @patch("hypergnn_framework_improved.ComponentFactory")
    def test_add_agent_failure(self, mock_factory_class):
        """Test agent addition failure handling."""
        mock_factory = Mock()
        mock_factory.get_component.side_effect = Exception("Component error")
        mock_factory_class.return_value = mock_factory

        framework = HyperGNNFramework(self.config)

        result = framework.add_agent("agent_001", "Test Agent")

        self.assertFalse(result)

    @patch("hypergnn_framework_improved.ComponentFactory")
    def test_add_event_success(self, mock_factory_class):
        """Test successful event addition."""
        mock_factory = Mock()
        mock_dynamics = Mock()
        mock_evidence = Mock()

        mock_factory.get_component.side_effect = lambda comp_type: {
            "dynamics": mock_dynamics,
            "evidence": mock_evidence,
        }.get(comp_type)

        mock_factory_class.return_value = mock_factory

        framework = HyperGNNFramework(self.config)

        result = framework.add_event(
            "event_001", "Test Event", datetime.now(), ["agent1", "agent2"]
        )

        self.assertTrue(result)

    @patch("hypergnn_framework_improved.ComponentFactory")
    def test_mmo_analysis_success(self, mock_factory_class):
        """Test successful MMO analysis."""
        mock_factory = Mock()
        mock_dynamics = Mock()
        mock_verification = Mock()

        # Mock the MMO analysis result
        mock_mmo_result = Mock()
        mock_mmo_result.motive_indicators = ["indicator1", "indicator2"]
        mock_mmo_result.means_available = ["means1"]
        mock_mmo_result.opportunity_factors = ["opportunity1", "opportunity2"]
        mock_mmo_result.risk_assessment.value = "moderate"

        mock_dynamics.analyze_motive_means_opportunity.return_value = mock_mmo_result
        mock_verification.get_person_communication_timeline.return_value = [
            "comm1",
            "comm2",
        ]

        mock_factory.get_component.side_effect = lambda comp_type: {
            "dynamics": mock_dynamics,
            "verification": mock_verification,
        }.get(comp_type)

        mock_factory_class.return_value = mock_factory

        framework = HyperGNNFramework(self.config)

        result = framework.analyze_motive_means_opportunity("agent_001", "event_001")

        self.assertIn("agent_id", result)
        self.assertIn("event_id", result)
        self.assertIn("integrated_assessment", result)
        self.assertEqual(result["agent_id"], "agent_001")
        self.assertEqual(result["event_id"], "event_001")
        self.assertEqual(result["integrated_assessment"]["total_risk_factors"], 5)

    @patch("hypergnn_framework_improved.ComponentFactory")
    def test_mmo_analysis_failure(self, mock_factory_class):
        """Test MMO analysis failure handling."""
        mock_factory = Mock()
        mock_factory.get_component.return_value = None  # No dynamics component
        mock_factory_class.return_value = mock_factory

        framework = HyperGNNFramework(self.config)

        result = framework.analyze_motive_means_opportunity("agent_001", "event_001")

        self.assertIn("error", result)
        self.assertIn("agent_id", result)
        self.assertIn("event_id", result)

    @patch("hypergnn_framework_improved.ComponentFactory")
    def test_get_framework_status(self, mock_factory_class):
        """Test getting framework status."""
        mock_factory = Mock()
        mock_factory.get_all_components.return_value = {
            "evidence": Mock(),
            "dynamics": Mock(),
        }
        mock_factory_class.return_value = mock_factory

        framework = HyperGNNFramework(self.config)

        status = framework.get_framework_status()

        self.assertEqual(status["framework_status"], "operational")
        self.assertEqual(status["case_id"], self.config.case_id)
        self.assertEqual(status["components_count"], 2)
        self.assertIn("evidence", status["components_loaded"])
        self.assertIn("dynamics", status["components_loaded"])

    @patch("hypergnn_framework_improved.ComponentFactory")
    def test_export_comprehensive_analysis(self, mock_factory_class):
        """Test comprehensive analysis export."""
        mock_factory = Mock()
        mock_component1 = Mock()
        mock_component1.get_summary.return_value = {"status": "active", "items": 5}
        mock_component2 = Mock()
        mock_component2.get_summary.return_value = {"status": "ready", "count": 10}

        mock_factory.get_all_components.return_value = {
            "component1": mock_component1,
            "component2": mock_component2,
        }
        mock_factory_class.return_value = mock_factory

        framework = HyperGNNFramework(self.config)

        result = framework.export_comprehensive_analysis()

        self.assertEqual(result["case_id"], self.config.case_id)
        self.assertEqual(result["framework_version"], "2.0.0-enhanced")
        self.assertIn("component_summaries", result)
        self.assertIn("component1", result["component_summaries"])
        self.assertIn("component2", result["component_summaries"])


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete framework."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = AnalysisConfiguration(
            case_id="integration_test",
            scope=AnalysisScope.INDIVIDUAL,
            complexity_level=ComplexityLevel.BASIC,
            output_directory=self.temp_dir,
        )

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("hypergnn_framework_improved.ComponentFactory")
    def test_full_workflow(self, mock_factory_class):
        """Test a complete workflow from initialization to analysis export."""
        # Mock all components
        mock_factory = Mock()
        mock_components = {}

        for comp_type in [
            "evidence",
            "dynamics",
            "language",
            "verification",
            "knowledge",
        ]:
            mock_comp = Mock()
            mock_comp.get_summary.return_value = {f"{comp_type}_status": "operational"}
            mock_components[comp_type] = mock_comp

        mock_factory.create_component.side_effect = (
            lambda comp_type: mock_components.get(comp_type)
        )
        mock_factory.get_component.side_effect = lambda comp_type: mock_components.get(
            comp_type
        )
        mock_factory.get_all_components.return_value = mock_components
        mock_factory_class.return_value = mock_factory

        # Initialize framework
        framework = HyperGNNFramework(self.config)

        # Add agents and events
        agent_result = framework.add_agent("agent_001", "Test Agent")
        event_result = framework.add_event(
            "event_001", "Test Event", datetime.now(), ["agent_001", "agent_002"]
        )

        # Get status
        status = framework.get_framework_status()

        # Export analysis
        analysis = framework.export_comprehensive_analysis()

        # Verify results
        self.assertTrue(agent_result)
        self.assertTrue(event_result)
        self.assertEqual(status["framework_status"], "operational")
        self.assertEqual(analysis["case_id"], self.config.case_id)
        self.assertIn("component_summaries", analysis)


if __name__ == "__main__":
    # Create a test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_classes = [
        TestAnalysisConfiguration,
        TestRulesEngine,
        TestDataIntegrationLayer,
        TestComponentFactory,
        TestHyperGNNFramework,
        TestIntegration,
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(
        f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%"
    )
    print(f"{'='*50}")
