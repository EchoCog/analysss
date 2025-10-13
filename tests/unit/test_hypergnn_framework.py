import unittest
from analysis.hypergnn_framework import (
    HyperGNNFramework,
    AnalysisConfiguration,
    AnalysisScope,
    ComplexityLevel,
)


class TestHyperGNNFramework(unittest.TestCase):

    def test_framework_initialization(self):
        config = AnalysisConfiguration(
            case_id="test_case",
            scope=AnalysisScope.COMPREHENSIVE,
            complexity_level=ComplexityLevel.ADVANCED,
        )
        framework = HyperGNNFramework(config)
        self.assertIsNotNone(framework)
        self.assertEqual(framework.config.case_id, "test_case")


if __name__ == "__main__":
    unittest.main()
