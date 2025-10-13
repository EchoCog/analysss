import argparse
from analysis.hypergnn_framework import (
    HyperGNNFramework,
    AnalysisConfiguration,
    AnalysisScope,
    ComplexityLevel,
)


def main():
    parser = argparse.ArgumentParser(description="HyperGNN Analysis Framework CLI")
    parser.add_argument(
        "--case-id", type=str, required=True, help="Case ID for the analysis"
    )
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to the data loader configuration file",
    )

    args = parser.parse_args()

    # Load the data loader configuration
    with open(args.config, "r") as f:
        data_loader_config = json.load(f)

    # Initialize the framework
    config = AnalysisConfiguration(
        case_id=args.case_id,
        scope=AnalysisScope.COMPREHENSIVE,
        complexity_level=ComplexityLevel.ADVANCED,
    )
    framework = HyperGNNFramework(config)

    # Load data
    framework.load_data_from_source(data_loader_config)

    # Export analysis
    analysis = framework.export_comprehensive_analysis()

    # Print analysis summary
    print(json.dumps(analysis, indent=4))


if __name__ == "__main__":
    main()
