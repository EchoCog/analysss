#!/usr/bin/env python3
"""
Main Entry Point for Analysis Framework

This module serves as the main entry point for the analysis framework,
providing a unified interface for running various analysis modules and cases.
"""

import argparse
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("analysis.log")],
)

logger = logging.getLogger(__name__)


def setup_argparse() -> argparse.ArgumentParser:
    """Set up command line argument parser."""
    parser = argparse.ArgumentParser(description="Analysis Framework")

    # Main command subparsers
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Case analysis command
    case_parser = subparsers.add_parser("case", help="Run case analysis")
    case_parser.add_argument("case_id", help="ID of the case to analyze")
    case_parser.add_argument("--output", "-o", help="Output file path")
    case_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    # Fraud analysis command
    fraud_parser = subparsers.add_parser("fraud", help="Run fraud analysis")
    fraud_parser.add_argument(
        "--case-id", required=True, help="ID of the case to analyze"
    )
    fraud_parser.add_argument("--suspect", help="Name of the primary suspect")
    fraud_parser.add_argument("--output", "-o", help="Output file path")

    # Hypergraph analysis command
    hypergraph_parser = subparsers.add_parser(
        "hypergraph", help="Generate hypergraph analysis"
    )
    hypergraph_parser.add_argument(
        "--case-id", required=True, help="ID of the case to analyze"
    )
    hypergraph_parser.add_argument("--output", "-o", help="Output file path")

    # Run all simulations command
    sim_parser = subparsers.add_parser(
        "run-all-simulations", help="Run all simulations"
    )
    sim_parser.add_argument(
        "--case-id", required=True, help="ID of the case to analyze"
    )
    sim_parser.add_argument("--output-dir", help="Output directory for simulations")

    return parser


def run_case_analysis(
    case_id: str, output_path: Optional[str] = None, verbose: bool = False
) -> Dict[str, Any]:
    """
    Run analysis for a specific case.

    Args:
        case_id: ID of the case to analyze
        output_path: Optional path to save the analysis results
        verbose: Whether to enable verbose output

    Returns:
        Dictionary containing the analysis results
    """
    logger.info(f"Running analysis for case: {case_id}")

    if case_id == "rezonance":
        from cases.rezonance_case import ReZonanceCaseAnalyzer

        analyzer = ReZonanceCaseAnalyzer()
        analyzer.load_entities()
        analyzer.load_timeline_events()
        analyzer.analyze_financial_patterns()
        analyzer.analyze_payment_fraud()

        if output_path:
            result_path = analyzer.export_to_json(output_path)
            logger.info(f"Analysis results saved to: {result_path}")
        else:
            result_path = analyzer.export_to_json()
            logger.info(f"Analysis results saved to: {result_path}")

        if verbose:
            logger.info(f"Loaded {len(analyzer.entities)} entities")
            logger.info(f"Loaded {len(analyzer.timeline_events)} timeline events")
            logger.info(
                f"Generated {len(analyzer.generate_hypergraph_nodes())} hypergraph nodes"
            )
            logger.info(
                f"Generated {len(analyzer.generate_hypergraph_edges())} hypergraph edges"
            )

        # Load the results to return
        with open(result_path, "r", encoding="utf-8") as f:
            results = json.load(f)

        return results
    else:
        logger.error(f"Unknown case ID: {case_id}")
        return {"error": f"Unknown case ID: {case_id}"}


def run_fraud_analysis(
    case_id: str, suspect: Optional[str] = None, output_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run fraud analysis for a specific case.

    Args:
        case_id: ID of the case to analyze
        suspect: Optional name of the primary suspect
        output_path: Optional path to save the analysis results

    Returns:
        Dictionary containing the fraud analysis results
    """
    logger.info(f"Running fraud analysis for case: {case_id}")

    if case_id == "rezonance":
        from fraud_analysis import create_rezonance_fraud_analyzer

        analyzer = create_rezonance_fraud_analyzer()

        if suspect:
            analyzer.generate_criminal_profile(suspect)
            logger.info(f"Generated criminal profile for: {suspect}")

        analyzer.calculate_damages()
        analyzer.generate_investigation_roadmap()

        if output_path:
            results = analyzer.export_fraud_analysis(output_path)
            logger.info(f"Fraud analysis results saved to: {output_path}")
        else:
            output_file = f"{case_id}_fraud_analysis.json"
            results = analyzer.export_fraud_analysis(output_file)
            logger.info(f"Fraud analysis results saved to: {output_file}")

        return results
    else:
        logger.error(f"Unknown case ID: {case_id}")
        return {"error": f"Unknown case ID: {case_id}"}


def run_hypergraph_analysis(
    case_id: str, output_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate hypergraph analysis for a specific case.

    Args:
        case_id: ID of the case to analyze
        output_path: Optional path to save the analysis results

    Returns:
        Dictionary containing the hypergraph analysis results
    """
    logger.info(f"Generating hypergraph analysis for case: {case_id}")

    if case_id == "rezonance":
        from cases.rezonance_case import ReZonanceCaseAnalyzer

        analyzer = ReZonanceCaseAnalyzer()
        analyzer.load_entities()
        analyzer.load_timeline_events()
        analyzer.analyze_payment_fraud()

        nodes = analyzer.generate_hypergraph_nodes()
        edges = analyzer.generate_hypergraph_edges()

        hypergraph = {
            "case_id": case_id,
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "node_count": len(nodes),
                "edge_count": len(edges),
                "entity_count": len([n for n in nodes if n["type"] == "entity"]),
                "event_count": len([n for n in nodes if n["type"] == "event"]),
                "fraud_pattern_count": len(
                    [n for n in nodes if n["type"] == "fraud_pattern"]
                ),
            },
        }

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(hypergraph, f, indent=2, ensure_ascii=False)
            logger.info(f"Hypergraph analysis results saved to: {output_path}")
        else:
            output_file = f"{case_id}_hypergraph.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(hypergraph, f, indent=2, ensure_ascii=False)
            logger.info(f"Hypergraph analysis results saved to: {output_file}")

        return hypergraph
    else:
        logger.error(f"Unknown case ID: {case_id}")
        return {"error": f"Unknown case ID: {case_id}"}


def run_all_simulations(
    case_id: str, output_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run all simulations for a specific case.

    Args:
        case_id: ID of the case to analyze
        output_dir: Optional directory to save the simulation results

    Returns:
        Dictionary containing the simulation results
    """
    logger.info(f"Running all simulations for case: {case_id}")

    # Create output directory if specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Run case analysis
    case_output = (
        os.path.join(output_dir, f"{case_id}_analysis.json") if output_dir else None
    )
    case_results = run_case_analysis(case_id, case_output, verbose=True)

    # Run fraud analysis
    fraud_output = (
        os.path.join(output_dir, f"{case_id}_fraud_analysis.json")
        if output_dir
        else None
    )
    fraud_results = run_fraud_analysis(case_id, output_path=fraud_output)

    # Run hypergraph analysis
    hypergraph_output = (
        os.path.join(output_dir, f"{case_id}_hypergraph.json") if output_dir else None
    )
    hypergraph_results = run_hypergraph_analysis(case_id, hypergraph_output)

    # Combine results
    simulation_results = {
        "case_id": case_id,
        "case_analysis": case_results,
        "fraud_analysis": fraud_results,
        "hypergraph_analysis": hypergraph_results,
    }

    # Save combined results
    if output_dir:
        combined_output = os.path.join(output_dir, f"{case_id}_combined_results.json")
        with open(combined_output, "w", encoding="utf-8") as f:
            json.dump(simulation_results, f, indent=2, ensure_ascii=False)
        logger.info(f"Combined simulation results saved to: {combined_output}")

    return simulation_results


def main():
    """Main entry point for the application."""
    parser = setup_argparse()
    args = parser.parse_args()

    if args.command == "case":
        run_case_analysis(args.case_id, args.output, args.verbose)
    elif args.command == "fraud":
        run_fraud_analysis(args.case_id, args.suspect, args.output)
    elif args.command == "hypergraph":
        run_hypergraph_analysis(args.case_id, args.output)
    elif args.command == "run-all-simulations":
        run_all_simulations(args.case_id, args.output_dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
