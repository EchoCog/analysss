#!/usr/bin/env python3
"""
Test script for enhanced simulation report generation
"""

import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.generate_simulation_report import generate_comprehensive_report


def create_mock_simulation_results():
    """Create mock simulation results for testing"""

    # Create temporary directory structure
    temp_dir = tempfile.mkdtemp()
    results_dir = Path(temp_dir) / "simulation_results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # Create mock agent-based results
    agent_dir = results_dir / "agent_simulation" / "run_001"
    agent_dir.mkdir(parents=True, exist_ok=True)

    agent_results = {
        "hypergnn_simulation": {
            "agent_dynamics": {
                "agent_001": {
                    "role": "suspect",
                    "interactions": ["event_1", "event_2"],
                },
                "agent_002": {"role": "witness", "interactions": ["event_1"]},
                "agent_003": {
                    "role": "investigator",
                    "interactions": ["event_2", "event_3"],
                },
            },
            "network_topology": {
                "clustering_coefficient": 0.75,
                "centrality_analysis": {"betweenness": {}, "eigenvector": {}},
                "community_detection": {"communities": 2},
                "network_robustness": {"robustness_score": 0.82},
            },
            "influence_propagation": {
                "cascade_analysis": {"max_depth": 3},
                "reach_metrics": {"average_reach": 2.5},
                "speed_analysis": {"propagation_speed": 1.2},
            },
            "stability_metrics": {"convergence_rate": 0.89},
            "performance_stats": {"execution_time": 45.2},
        }
    }

    agent_summary = {
        "simulation_type": "agent-based",
        "summary_stats": {
            "total_agents": 3,
            "network_density": 0.75,
            "simulation_duration": 60,
        },
    }

    # Create discrete event results
    discrete_dir = results_dir / "discrete_simulation" / "run_001"
    discrete_dir.mkdir(parents=True, exist_ok=True)

    discrete_results = {
        "discrete_event_simulation": {
            "total_events": 15,
            "cascade_analysis": {
                "max_cascade_depth": 4,
                "depth_distribution": {"1": 5, "2": 4, "3": 3, "4": 3},
                "branching_analysis": {"average_branching": 1.8},
            },
            "temporal_patterns": {
                "frequency_analysis": {"peak_frequency": 0.3},
                "clustering_metrics": {"temporal_clusters": 3},
                "periodicity_analysis": {"period_detected": True},
            },
            "causal_analysis": {"causal_chains": 4},
            "warning_indicators": {"risk_level": "medium"},
        }
    }

    discrete_summary = {
        "simulation_type": "discrete-event",
        "summary_stats": {
            "total_events": 15,
            "cascade_depth": 4,
            "temporal_clusters": 3,
        },
    }

    # Create system dynamics results
    system_dir = results_dir / "system_simulation" / "run_001"
    system_dir.mkdir(parents=True, exist_ok=True)

    system_results = {
        "system_dynamics_simulation": {
            "optimization_metrics": {
                "total_system_efficiency": 0.82,
                "stability_index": 0.76,
            },
            "flow_dynamics": {"flow_rate": 2.4},
            "stock_analysis": {"resource_levels": {"high": 2, "medium": 3}},
            "bottleneck_analysis": {"bottlenecks_identified": 2},
        },
        "equilibrium_analysis": {
            "equilibrium_states": {"stable_points": 2},
            "stability_analysis": {"stability_region": "large"},
        },
    }

    system_summary = {
        "simulation_type": "system-dynamics",
        "summary_stats": {
            "system_efficiency": 0.82,
            "stability_index": 0.76,
            "equilibrium_points": 2,
        },
    }

    # Create integrated multi-model results
    integrated_dir = results_dir / "integrated_simulation" / "run_001"
    integrated_dir.mkdir(parents=True, exist_ok=True)

    integrated_results = {
        "integration_metrics": {
            "overall_score": 0.85,
            "alignment_matrix": {"agent_discrete": 0.78, "system_agent": 0.82},
            "alignments": [{"coherence_metrics": {"attention_patterns": {}}}],
        },
        "integrated_insights": {
            "cross_model_insights": [
                {"insight": "temporal coherence", "confidence": 0.89},
                {"insight": "network stability", "confidence": 0.76},
            ]
        },
    }

    integrated_summary = {
        "simulation_type": "integrated",
        "summary_stats": {
            "integration_score": 0.85,
            "cross_model_insights": 2,
            "alignment_quality": "high",
        },
    }

    # Write all results to files
    with open(agent_dir / "simulation_results.json", "w") as f:
        json.dump(agent_results, f, indent=2)
    with open(agent_dir / "simulation_summary.json", "w") as f:
        json.dump(agent_summary, f, indent=2)

    with open(discrete_dir / "simulation_results.json", "w") as f:
        json.dump(discrete_results, f, indent=2)
    with open(discrete_dir / "simulation_summary.json", "w") as f:
        json.dump(discrete_summary, f, indent=2)

    with open(system_dir / "simulation_results.json", "w") as f:
        json.dump(system_results, f, indent=2)
    with open(system_dir / "simulation_summary.json", "w") as f:
        json.dump(system_summary, f, indent=2)

    with open(integrated_dir / "simulation_results.json", "w") as f:
        json.dump(integrated_results, f, indent=2)
    with open(integrated_dir / "simulation_summary.json", "w") as f:
        json.dump(integrated_summary, f, indent=2)

    return str(results_dir)


def main():
    """Test the enhanced simulation report generation"""
    print("🧪 Testing Enhanced Simulation Report Generation")
    print("=" * 60)

    # Create mock data
    print("📁 Creating mock simulation results...")
    mock_results_dir = create_mock_simulation_results()
    print(f"   Mock data created in: {mock_results_dir}")

    # Generate enhanced report
    print("\n📊 Generating enhanced comprehensive report...")
    output_dir = "/home/runner/work/analysis/analysis/sims"

    try:
        report_file = generate_comprehensive_report(
            case_id="enhanced_test_case_2025",
            results_dir=mock_results_dir,
            output_dir=output_dir,
        )

        if report_file:
            print(f"✅ Enhanced report generated successfully!")
            print(f"   Report location: {report_file}")

            # Check if markdown file was also created
            markdown_file = report_file.replace(".json", ".md")
            if Path(markdown_file).exists():
                print(f"   Markdown report: {markdown_file}")

                # Show a preview of the enhanced markdown content
                print("\n📄 Enhanced Report Preview:")
                print("-" * 40)
                with open(markdown_file, "r") as f:
                    content = f.read()
                    lines = content.split("\n")
                    # Show first 30 lines
                    for i, line in enumerate(lines[:30]):
                        print(f"{i+1:2d}: {line}")
                    if len(lines) > 30:
                        print(f"... ({len(lines) - 30} more lines)")
                        print(f"Total content length: {len(content)} characters")

        else:
            print("❌ Report generation failed!")

    except Exception as e:
        print(f"❌ Error during report generation: {e}")
        import traceback

        traceback.print_exc()

    print(f"\n🗑️ Cleaning up mock data: {mock_results_dir}")
    import shutil

    shutil.rmtree(Path(mock_results_dir).parent)


if __name__ == "__main__":
    main()
