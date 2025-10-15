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

    # AD Hypergraph Repository Mapping commands
    ad_parser = subparsers.add_parser(
        "ad-hypergraph", help="AD hypergraph repository mapping operations"
    )
    ad_subparsers = ad_parser.add_subparsers(dest="ad_command", help="AD hypergraph commands")
    
    # Scan repositories
    scan_parser = ad_subparsers.add_parser("scan", help="Scan repositories for AD hypergraph mapping")
    scan_parser.add_argument("--repo", help="Specific repository to scan (default: all)")
    scan_parser.add_argument("--output", "-o", help="Output file for scan results")
    
    # Load repositories into unified schema
    load_parser = ad_subparsers.add_parser("load", help="Load repositories into unified hypergraph schema")
    load_parser.add_argument("--repo", help="Specific repository to load (default: all)")
    
    # Generate cross-repository links
    link_parser = ad_subparsers.add_parser("link", help="Generate cross-repository entity links")
    
    # Export unified hypergraph
    export_parser = ad_subparsers.add_parser("export", help="Export unified AD hypergraph")
    export_parser.add_argument("--output", "-o", required=True, help="Output file path")
    
    # Repository summary
    summary_parser = ad_subparsers.add_parser("summary", help="Show repository mapping summary")

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


def run_ad_hypergraph_command(args) -> Dict[str, Any]:
    """
    Run AD hypergraph repository mapping commands.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Dictionary containing command results
    """
    import sys
    from pathlib import Path
    
    # Ensure current directory is in path for module imports
    current_dir = str(Path(__file__).parent.parent)
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    from src.api.ad_hypergraph_repository_mapper import ADHypergraphRepositoryMapper
    
    mapper = ADHypergraphRepositoryMapper()
    
    if args.ad_command == "scan":
        if args.repo:
            if args.repo not in mapper.repositories:
                result = {"error": f"Repository {args.repo} not found"}
                print(json.dumps(result, indent=2))
                return result
            scan_results = mapper.scan_local_repository(args.repo)
        else:
            # Scan all available local repositories
            scan_results = {}
            for repo_name, repo_config in mapper.repositories.items():
                if repo_config.local_path:
                    try:
                        scan_results[repo_name] = mapper.scan_local_repository(repo_name)
                    except Exception as e:
                        scan_results[repo_name] = {"error": str(e)}
        
        if args.output:
            output_file = Path(args.output)
            with open(output_file, 'w') as f:
                json.dump(scan_results, f, indent=2)
            logger.info(f"Scan results saved to {output_file}")
        else:
            print(json.dumps(scan_results, indent=2))
        
        return scan_results
        
    elif args.ad_command == "load":
        total_loaded = 0
        load_results = {}
        
        if args.repo:
            if args.repo not in mapper.repositories:
                result = {"error": f"Repository {args.repo} not found"}
                print(json.dumps(result, indent=2))
                return result
            loaded = mapper.load_repository_into_schema(args.repo)
            load_results[args.repo] = loaded
            total_loaded = loaded
        else:
            # Load all available local repositories
            for repo_name, repo_config in mapper.repositories.items():
                if repo_config.local_path:
                    try:
                        loaded = mapper.load_repository_into_schema(repo_name)
                        load_results[repo_name] = loaded
                        total_loaded += loaded
                    except Exception as e:
                        load_results[repo_name] = {"error": str(e)}
        
        result = {
            "total_loaded": total_loaded,
            "repositories": load_results,
            "schema_stats": {
                "entities": len(mapper.schema.nodes),
                "relations": len(mapper.schema.edges)
            }
        }
        print(json.dumps(result, indent=2))
        return result
        
    elif args.ad_command == "link":
        cross_links = mapper.generate_cross_repository_links()
        result = {
            "cross_links_generated": len(cross_links),
            "total_entities": len(mapper.schema.nodes),
            "total_relations": len(mapper.schema.edges)
        }
        print(json.dumps(result, indent=2))
        return result
        
    elif args.ad_command == "export":
        export_data = mapper.export_unified_hypergraph(args.output)
        result = {
            "exported_to": args.output,
            "entities": len(export_data.get("nodes", [])),
            "relations": len(export_data.get("edges", [])),
            "repositories": len(export_data["metadata"]["ad_hypergraph"]["repositories"])
        }
        print(json.dumps(result, indent=2))
        return result
        
    elif args.ad_command == "summary":
        summary = mapper.get_repository_summary()
        print(json.dumps(summary, indent=2))
        return summary
        
    else:
        result = {"error": "Invalid AD hypergraph command"}
        print(json.dumps(result, indent=2))
        return result


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
    elif args.command == "ad-hypergraph":
        run_ad_hypergraph_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
