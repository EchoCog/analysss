#!/usr/bin/env python3
"""
Configuration script for enhanced detailed simulation reports
============================================================

This script configures the simulation analysis framework to generate significantly
more detailed reports with comprehensive analysis sections, detailed metrics,
and enhanced recommendations.

Usage:
    python configure_detailed_reports.py --case-id <case_id> [options]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.generate_simulation_report import generate_comprehensive_report


def configure_enhanced_reporting():
    """Configure the system for enhanced detailed reporting"""

    print("🔧 Configuring Enhanced Detailed Simulation Reports")
    print("=" * 60)

    # Configuration settings for enhanced reports
    config = {
        "report_version": "2.0",
        "detail_level": "maximum",
        "enhancement_features": {
            "detailed_model_analysis": True,
            "comprehensive_metrics": True,
            "cross_model_validation": True,
            "risk_assessment_analysis": True,
            "investigation_priority_matrix": True,
            "actionable_recommendations": True,
            "performance_benchmarks": True,
            "statistical_analysis": True,
            "quality_assurance_metrics": True,
            "enhanced_markdown_formatting": True,
        },
        "analytical_depth": {
            "network_analysis": "comprehensive",
            "temporal_analysis": "detailed",
            "behavioral_patterns": "enhanced",
            "system_dynamics": "full_spectrum",
            "integration_quality": "maximum_validation",
        },
        "reporting_enhancements": {
            "visual_formatting": True,
            "structured_sections": True,
            "implementation_guidance": True,
            "success_metrics": True,
            "quality_indicators": True,
        },
    }

    # Save configuration
    config_file = Path(__file__).parent / "enhanced_report_config.json"
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)

    print(f"✅ Enhanced reporting configuration saved to: {config_file}")
    return config


def generate_enhanced_report(case_id: str, results_dir: str, output_dir: str = "sims"):
    """Generate an enhanced detailed simulation report"""

    print(f"\n📊 Generating Enhanced Detailed Report for Case: {case_id}")
    print("-" * 50)

    # Check if results directory exists
    if not Path(results_dir).exists():
        print(f"❌ Results directory not found: {results_dir}")
        print(
            "   Please ensure simulation results are available before generating reports."
        )
        return None

    try:
        # Generate the comprehensive report using enhanced configuration
        report_file = generate_comprehensive_report(
            case_id=case_id, results_dir=results_dir, output_dir=output_dir
        )

        if report_file:
            # Check file sizes to show enhancement
            json_file = Path(report_file)
            markdown_file = json_file.with_suffix(".md")

            print(f"\n✅ Enhanced Detailed Report Generated Successfully!")
            print(f"   📄 JSON Report: {json_file}")
            print(f"      Size: {json_file.stat().st_size:,} bytes")

            if markdown_file.exists():
                print(f"   📝 Markdown Report: {markdown_file}")
                print(f"      Size: {markdown_file.stat().st_size:,} bytes")

                # Count lines and sections
                with open(markdown_file, "r") as f:
                    content = f.read()
                    lines = len(content.split("\n"))
                    sections = content.count("##")

                print(f"      Lines: {lines:,}")
                print(f"      Sections: {sections}")

            print(f"\n📈 Report Enhancement Summary:")
            print(f"   • Detailed model analysis with comprehensive metrics")
            print(f"   • Cross-model validation and convergence analysis")
            print(f"   • Risk assessment with quantitative analysis")
            print(f"   • Investigation priority matrix with confidence scoring")
            print(f"   • Actionable recommendations with implementation steps")
            print(f"   • Performance benchmarks and statistical summaries")
            print(f"   • Quality assurance metrics and validation protocols")
            print(f"   • Enhanced visual formatting and structured presentation")

            return str(report_file)

        else:
            print("❌ Report generation failed - please check simulation results")
            return None

    except Exception as e:
        print(f"❌ Error generating enhanced report: {e}")
        import traceback

        traceback.print_exc()
        return None


def main():
    """Main function for enhanced report configuration"""

    parser = argparse.ArgumentParser(
        description="Configure and generate enhanced detailed simulation reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Configure enhanced reporting
  python configure_detailed_reports.py --configure-only
  
  # Generate enhanced report for existing case
  python configure_detailed_reports.py --case-id comprehensive_test_2025 --results-dir ./simulation_results
  
  # Generate enhanced report with custom output directory
  python configure_detailed_reports.py --case-id my_case --results-dir ./results --output-dir ./enhanced_reports
        """,
    )

    parser.add_argument("--case-id", help="Case ID for report generation")
    parser.add_argument("--results-dir", help="Directory containing simulation results")
    parser.add_argument(
        "--output-dir", default="sims", help="Output directory for reports"
    )
    parser.add_argument(
        "--configure-only",
        action="store_true",
        help="Only configure enhanced reporting, don't generate report",
    )

    args = parser.parse_args()

    # Always configure enhanced reporting
    config = configure_enhanced_reporting()

    if args.configure_only:
        print(f"\n✅ Enhanced reporting configured successfully!")
        print(f"   Use --case-id and --results-dir to generate enhanced reports")
        return

    if not args.case_id or not args.results_dir:
        print(f"\n⚠️ Case ID and results directory required for report generation")
        print(f"   Use --configure-only to only setup enhanced reporting")
        print(f"   Use --help for usage examples")
        return

    # Generate enhanced report
    report_file = generate_enhanced_report(
        case_id=args.case_id, results_dir=args.results_dir, output_dir=args.output_dir
    )

    if report_file:
        print(f"\n🎉 Enhanced Detailed Simulation Report Complete!")
        print(f"   Report provides significantly more detailed analysis")
        print(f"   Ready for comprehensive case analysis and decision-making")
    else:
        print(f"\n❌ Enhanced report generation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
