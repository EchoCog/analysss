#!/usr/bin/env python3
"""
Case Hypergraph Example Usage
=============================

Demonstrates how to use the case hypergraph system for analysis.
"""

import json
from pathlib import Path

from hypergraph_visualizer import HypergraphVisualizer

from case_hypergraph_constructor import CaseHypergraph, HyperedgeType


def analyze_case_hypergraph():
    """Demonstrate hypergraph analysis capabilities"""

    print("=== CASE HYPERGRAPH ANALYSIS EXAMPLE ===\n")

    # Load existing hypergraph
    hypergraph_file = "/workspace/case_hypergraph.json"
    if not Path(hypergraph_file).exists():
        print(
            "Please run case_hypergraph_constructor.py first to build the hypergraph."
        )
        return

    print(f"Loading hypergraph from {hypergraph_file}...")
    hypergraph = CaseHypergraph.load_from_file(hypergraph_file)

    # Basic statistics
    print(f"\n=== BASIC STATISTICS ===")
    print(f"Total nodes: {len(hypergraph.nodes)}")
    print(f"Total hyperedges: {len(hypergraph.hyperedges)}")

    # Count by node type
    node_types = {}
    for node in hypergraph.nodes.values():
        node_types[node.node_type] = node_types.get(node.node_type, 0) + 1

    print(f"\nNodes by type:")
    for node_type, count in sorted(node_types.items()):
        print(f"  {node_type}: {count}")

    # Count by hyperedge type
    edge_types = {}
    for edge in hypergraph.hyperedges.values():
        edge_types[edge.edge_type.value] = edge_types.get(edge.edge_type.value, 0) + 1

    print(f"\nHyperedges by type:")
    for edge_type, count in sorted(edge_types.items()):
        print(f"  {edge_type}: {count}")

    # Find most connected nodes
    print(f"\n=== MOST CONNECTED NODES ===")
    sorted_nodes = sorted(
        hypergraph.nodes.values(), key=lambda n: n.weighted_degree, reverse=True
    )[:10]

    for node in sorted_nodes:
        print(
            f"{node.label} ({node.node_type}): {node.degree} connections, "
            f"weighted degree: {node.weighted_degree:.2f}"
        )

    # Find largest hyperedges
    print(f"\n=== LARGEST HYPEREDGES ===")
    sorted_edges = sorted(
        hypergraph.hyperedges.values(), key=lambda e: len(e.nodes), reverse=True
    )[:5]

    for edge in sorted_edges:
        print(f"{edge.edge_id} ({edge.edge_type.value}): {len(edge.nodes)} nodes")
        if edge.timestamp:
            print(f"  Date: {edge.timestamp.strftime('%Y-%m-%d')}")

    # Analyze specific entity
    print(f"\n=== ENTITY ANALYSIS: Peter Faucitt ===")
    peter_id = "peter_faucitt"
    if peter_id in hypergraph.nodes:
        peter_node = hypergraph.nodes[peter_id]
        print(f"Hyperedges involving {peter_node.label}:")

        for edge_id in list(peter_node.hyperedges)[:5]:  # Show first 5
            edge = hypergraph.hyperedges[edge_id]
            print(f"  - {edge.edge_type.value}: {len(edge.nodes)} participants")
            if edge.timestamp:
                print(f"    Date: {edge.timestamp.strftime('%Y-%m-%d')}")

    # Find related entities
    print(f"\n=== ENTITIES RELATED TO PETER FAUCITT ===")
    if peter_id in hypergraph.nodes:
        related = set()
        for edge_id in hypergraph.nodes[peter_id].hyperedges:
            edge = hypergraph.hyperedges[edge_id]
            related.update(edge.nodes)

        related.remove(peter_id)  # Remove self

        # Count co-occurrences
        co_occurrence = {}
        for other_id in related:
            count = 0
            for edge_id in hypergraph.nodes[peter_id].hyperedges:
                if other_id in hypergraph.hyperedges[edge_id].nodes:
                    count += 1
            co_occurrence[other_id] = count

        # Show top related
        top_related = sorted(co_occurrence.items(), key=lambda x: x[1], reverse=True)[
            :10
        ]
        for other_id, count in top_related:
            other_node = hypergraph.nodes[other_id]
            print(
                f"  {other_node.label} ({other_node.node_type}): {count} shared hyperedges"
            )

    # Community analysis
    print(f"\n=== COMMUNITY ANALYSIS ===")
    communities = hypergraph.detect_communities()
    community_sizes = {}
    for node_id, comm_id in communities.items():
        community_sizes[comm_id] = community_sizes.get(comm_id, 0) + 1

    print(f"Found {len(community_sizes)} communities:")
    for comm_id, size in sorted(
        community_sizes.items(), key=lambda x: x[1], reverse=True
    ):
        print(f"  Community {comm_id}: {size} nodes")

        # Show sample nodes from community
        comm_nodes = [nid for nid, cid in communities.items() if cid == comm_id][:5]
        for node_id in comm_nodes:
            node = hypergraph.nodes[node_id]
            print(f"    - {node.label} ({node.node_type})")

    # Temporal analysis
    print(f"\n=== TEMPORAL ANALYSIS ===")
    temporal_patterns = hypergraph.find_temporal_patterns(window_days=7)
    print(f"Found {len(temporal_patterns)} temporal clusters")

    if temporal_patterns:
        # Show most active period
        most_active = max(temporal_patterns, key=lambda p: p["edge_count"])
        print(f"\nMost active 7-day period:")
        print(f"  Start: {most_active['start_time'].strftime('%Y-%m-%d')}")
        print(f"  Hyperedges: {most_active['edge_count']}")
        print(f"  Participants: {most_active['unique_participants']}")
        print(f"  Activity types: {most_active['edge_types']}")

    # Search for specific patterns
    print(f"\n=== PATTERN SEARCH ===")

    # Find all communication hyperedges
    comm_edges = [
        e
        for e in hypergraph.hyperedges.values()
        if e.edge_type == HyperedgeType.COMMUNICATION
    ]
    print(f"Found {len(comm_edges)} communication hyperedges")

    # Find all financial transaction hyperedges
    trans_edges = [
        e
        for e in hypergraph.hyperedges.values()
        if e.edge_type == HyperedgeType.TRANSACTION
    ]
    print(f"Found {len(trans_edges)} transaction hyperedges")

    # Find verified evidence
    verified_edges = [
        e
        for e in hypergraph.hyperedges.values()
        if hasattr(e, "verification_status")
        and str(e.verification_status) == "InformationStatus.VERIFIED"
    ]
    print(f"Found {len(verified_edges)} verified hyperedges")

    print(f"\n=== ANALYSIS COMPLETE ===")


def export_analysis_report():
    """Export detailed analysis report"""

    print("\n=== EXPORTING ANALYSIS REPORT ===")

    # Load hypergraph
    hypergraph = CaseHypergraph.load_from_file("/workspace/case_hypergraph.json")

    # Compute all analyses
    analysis = hypergraph.export_to_dict()

    # Save detailed report
    report_file = "/workspace/case_hypergraph_analysis_report.json"
    with open(report_file, "w") as f:
        json.dump(analysis, f, indent=2, default=str)

    print(f"✅ Detailed analysis report saved to: {report_file}")

    # Create summary report
    summary = {
        "case_id": analysis["case_id"],
        "statistics": {
            "total_nodes": analysis["metadata"]["node_count"],
            "total_hyperedges": analysis["metadata"]["hyperedge_count"],
            "communities_found": len(set(analysis["analysis"]["communities"].values())),
            "temporal_patterns": len(analysis["analysis"]["temporal_patterns"]),
            "overlapping_edges": len(analysis["analysis"]["overlapping_edges"]),
        },
        "top_entities": [],
        "key_findings": [],
    }

    # Add top entities by centrality
    centrality = analysis["analysis"]["centrality"]["eigenvector"]
    top_entities = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]

    for entity_id, score in top_entities:
        if entity_id in analysis["nodes"]:
            node = analysis["nodes"][entity_id]
            summary["top_entities"].append(
                {
                    "name": node["label"],
                    "type": node["node_type"],
                    "centrality_score": score,
                    "connections": node["degree"],
                }
            )

    # Add key findings
    if analysis["analysis"]["temporal_patterns"]:
        most_active = max(
            analysis["analysis"]["temporal_patterns"], key=lambda p: p["edge_count"]
        )
        summary["key_findings"].append(
            {
                "type": "temporal_hotspot",
                "description": f"Peak activity on {most_active['start_time']} with {most_active['edge_count']} events",
            }
        )

    # Save summary
    summary_file = "/workspace/case_hypergraph_summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"✅ Summary report saved to: {summary_file}")


if __name__ == "__main__":
    # Run analysis
    analyze_case_hypergraph()

    # Export reports
    export_analysis_report()
