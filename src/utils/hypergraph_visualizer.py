#!/usr/bin/env python3
"""
Hypergraph Visualizer
====================

Provides visualization capabilities for case hypergraphs including:
- Interactive network visualizations
- Incidence matrix heatmaps
- Temporal evolution animations
- Community structure displays
- Centrality visualizations
"""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns
from matplotlib.animation import FuncAnimation

# Import hypergraph structures
from case_hypergraph_constructor import CaseHypergraph, HyperedgeType, InformationStatus


class HypergraphVisualizer:
    """Visualizer for case hypergraphs"""

    def __init__(self, hypergraph: CaseHypergraph):
        self.hypergraph = hypergraph
        self.color_schemes = {
            "node_types": {
                "person": "#FF6B6B",
                "organization": "#4ECDC4",
                "email_address": "#45B7D1",
                "system": "#96CEB4",
                "default": "#95A5A6",
            },
            "edge_types": {
                HyperedgeType.COMMUNICATION: "#3498DB",
                HyperedgeType.TRANSACTION: "#E74C3C",
                HyperedgeType.LEGAL_PROCEEDING: "#9B59B6",
                HyperedgeType.ORGANIZATIONAL: "#F39C12",
                HyperedgeType.TEMPORAL_CLUSTER: "#16A085",
                HyperedgeType.EVIDENCE_LINK: "#2ECC71",
                HyperedgeType.CONTROL_STRUCTURE: "#E67E22",
                HyperedgeType.KNOWLEDGE_SHARING: "#1ABC9C",
            },
            "verification_status": {
                InformationStatus.VERIFIED: "#27AE60",
                InformationStatus.SAVED: "#3498DB",
                InformationStatus.PARTIAL: "#F39C12",
                InformationStatus.CIRCUMSTANTIAL: "#E67E22",
                InformationStatus.SPECULATIVE: "#E74C3C",
                InformationStatus.MISSING: "#95A5A6",
            },
        }

    def plot_hypergraph_projection(
        self,
        figsize: Tuple[int, int] = (15, 10),
        node_size_factor: float = 1000,
        edge_width_factor: float = 2.0,
        show_labels: bool = True,
        layout: str = "spring",
    ) -> plt.Figure:
        """Plot hypergraph as projected graph"""
        fig, ax = plt.subplots(figsize=figsize)

        # Project hypergraph to regular graph
        G = self.hypergraph._project_to_graph()

        # Calculate layout
        if layout == "spring":
            pos = nx.spring_layout(G, k=2, iterations=50)
        elif layout == "circular":
            pos = nx.circular_layout(G)
        elif layout == "kamada_kawai":
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.random_layout(G)

        # Prepare node colors and sizes
        node_colors = []
        node_sizes = []

        for node_id in G.nodes():
            node = self.hypergraph.nodes[node_id]
            color = self.color_schemes["node_types"].get(
                node.node_type, self.color_schemes["node_types"]["default"]
            )
            node_colors.append(color)
            node_sizes.append(node.weighted_degree * node_size_factor / 10)

        # Draw edges
        edge_weights = [G[u][v]["weight"] for u, v in G.edges()]
        max_weight = max(edge_weights) if edge_weights else 1
        edge_widths = [w * edge_width_factor / max_weight for w in edge_weights]

        nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5, edge_color="gray")

        # Draw nodes
        nx.draw_networkx_nodes(
            G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8
        )

        # Draw labels
        if show_labels:
            labels = {
                node_id: self.hypergraph.nodes[node_id].label.split()[-1]
                for node_id in G.nodes()
            }
            nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight="bold")

        # Add legend
        self._add_node_type_legend(ax)

        ax.set_title(
            f"Case Hypergraph Projection\n{len(self.hypergraph.nodes)} nodes, "
            f"{len(self.hypergraph.hyperedges)} hyperedges",
            fontsize=16,
            pad=20,
        )
        ax.axis("off")

        plt.tight_layout()
        return fig

    def plot_incidence_matrix(
        self, figsize: Tuple[int, int] = (12, 8), show_labels: bool = True
    ) -> plt.Figure:
        """Plot incidence matrix as heatmap"""
        fig, ax = plt.subplots(figsize=figsize)

        # Build incidence matrix
        H = self.hypergraph.build_incidence_matrix()

        # Create heatmap
        im = ax.imshow(H, cmap="YlOrRd", aspect="auto", interpolation="nearest")

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label("Edge Weight", rotation=270, labelpad=20)

        # Add labels if requested and not too many
        if show_labels and H.shape[0] < 50 and H.shape[1] < 50:
            # Node labels (y-axis)
            node_ids = sorted(self.hypergraph.nodes.keys())
            node_labels = [self.hypergraph.nodes[nid].label[:15] for nid in node_ids]
            ax.set_yticks(range(len(node_labels)))
            ax.set_yticklabels(node_labels, fontsize=8)

            # Edge labels (x-axis)
            edge_ids = sorted(self.hypergraph.hyperedges.keys())
            edge_labels = [eid[:10] for eid in edge_ids]
            ax.set_xticks(range(len(edge_labels)))
            ax.set_xticklabels(edge_labels, rotation=90, fontsize=8)

        ax.set_xlabel("Hyperedges", fontsize=12)
        ax.set_ylabel("Nodes", fontsize=12)
        ax.set_title("Hypergraph Incidence Matrix", fontsize=16, pad=20)

        plt.tight_layout()
        return fig

    def plot_node_similarity_matrix(
        self, figsize: Tuple[int, int] = (10, 10), show_labels: bool = True
    ) -> plt.Figure:
        """Plot node similarity matrix"""
        fig, ax = plt.subplots(figsize=figsize)

        # Get similarity matrix
        similarity = self.hypergraph.get_node_similarity_matrix()

        # Create heatmap
        mask = np.triu(np.ones_like(similarity, dtype=bool), k=1)
        sns.heatmap(
            similarity,
            mask=mask,
            cmap="coolwarm",
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
            ax=ax,
        )

        # Add labels if requested
        if show_labels and similarity.shape[0] < 30:
            node_ids = sorted(self.hypergraph.nodes.keys())
            node_labels = [self.hypergraph.nodes[nid].label[:15] for nid in node_ids]
            ax.set_xticklabels(node_labels, rotation=45, ha="right", fontsize=8)
            ax.set_yticklabels(node_labels, rotation=0, fontsize=8)

        ax.set_title(
            "Node Similarity Matrix\n(Based on shared hyperedges)", fontsize=16, pad=20
        )

        plt.tight_layout()
        return fig

    def plot_community_structure(
        self, figsize: Tuple[int, int] = (15, 10), resolution: float = 1.0
    ) -> plt.Figure:
        """Plot community structure of hypergraph"""
        fig, ax = plt.subplots(figsize=figsize)

        # Detect communities
        communities = self.hypergraph.detect_communities(resolution=resolution)

        # Project to graph
        G = self.hypergraph._project_to_graph()

        # Create layout
        pos = nx.spring_layout(G, k=2, iterations=50)

        # Prepare colors
        community_colors = {}
        unique_communities = set(communities.values())
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_communities)))

        for i, comm in enumerate(unique_communities):
            community_colors[comm] = colors[i]

        # Draw nodes by community
        for comm in unique_communities:
            nodes_in_comm = [n for n, c in communities.items() if c == comm]
            if nodes_in_comm:
                node_sizes = [
                    self.hypergraph.nodes[n].weighted_degree * 100
                    for n in nodes_in_comm
                ]
                nx.draw_networkx_nodes(
                    G,
                    pos,
                    nodelist=nodes_in_comm,
                    node_color=[community_colors[comm]] * len(nodes_in_comm),
                    node_size=node_sizes,
                    alpha=0.8,
                    label=f"Community {comm}",
                )

        # Draw edges
        nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color="gray")

        # Add labels for important nodes
        centrality = self.hypergraph.compute_centrality_measures()
        top_nodes = sorted(
            centrality["eigenvector"].items(), key=lambda x: x[1], reverse=True
        )[:10]

        labels = {
            node_id: self.hypergraph.nodes[node_id].label.split()[-1]
            for node_id, _ in top_nodes
        }
        nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight="bold")

        ax.set_title(
            f"Community Structure\n{len(unique_communities)} communities detected",
            fontsize=16,
            pad=20,
        )
        ax.legend(loc="best", fontsize=10)
        ax.axis("off")

        plt.tight_layout()
        return fig

    def plot_temporal_evolution(
        self, figsize: Tuple[int, int] = (15, 8), window_days: int = 7
    ) -> plt.Figure:
        """Plot temporal evolution of hypergraph"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, height_ratios=[2, 1])

        # Get temporal data
        temporal_data = defaultdict(lambda: {"edges": 0, "nodes": set()})

        for edge_id, edge in self.hypergraph.hyperedges.items():
            if edge.timestamp:
                date_key = edge.timestamp.date()
                temporal_data[date_key]["edges"] += 1
                temporal_data[date_key]["nodes"].update(edge.nodes)

        if not temporal_data:
            ax1.text(
                0.5,
                0.5,
                "No temporal data available",
                ha="center",
                va="center",
                fontsize=14,
            )
            return fig

        # Sort by date
        sorted_dates = sorted(temporal_data.keys())

        # Prepare data for plotting
        dates = []
        edge_counts = []
        node_counts = []
        cumulative_nodes = set()

        for date in sorted_dates:
            dates.append(date)
            edge_counts.append(temporal_data[date]["edges"])
            cumulative_nodes.update(temporal_data[date]["nodes"])
            node_counts.append(len(cumulative_nodes))

        # Plot edge activity
        ax1.bar(
            dates, edge_counts, alpha=0.7, color="steelblue", label="New hyperedges"
        )
        ax1.set_ylabel("Number of hyperedges", fontsize=12)
        ax1.set_title("Temporal Evolution of Case Hypergraph", fontsize=16, pad=20)
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot cumulative nodes
        ax2.plot(dates, node_counts, marker="o", color="darkgreen", linewidth=2)
        ax2.fill_between(dates, node_counts, alpha=0.3, color="darkgreen")
        ax2.set_xlabel("Date", fontsize=12)
        ax2.set_ylabel("Cumulative nodes", fontsize=12)
        ax2.grid(True, alpha=0.3)

        # Format x-axis
        for ax in [ax1, ax2]:
            ax.tick_params(axis="x", rotation=45)

        plt.tight_layout()
        return fig

    def plot_centrality_analysis(
        self, figsize: Tuple[int, int] = (15, 10), top_n: int = 15
    ) -> plt.Figure:
        """Plot centrality analysis results"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)

        # Compute centrality measures
        centrality = self.hypergraph.compute_centrality_measures()

        # Helper function to plot centrality
        def plot_centrality_bar(ax, measure_name, measure_data, color):
            top_nodes = sorted(measure_data.items(), key=lambda x: x[1], reverse=True)[
                :top_n
            ]

            node_labels = [
                self.hypergraph.nodes[nid].label[:20] for nid, _ in top_nodes
            ]
            values = [val for _, val in top_nodes]

            bars = ax.barh(range(len(node_labels)), values, color=color, alpha=0.7)
            ax.set_yticks(range(len(node_labels)))
            ax.set_yticklabels(node_labels, fontsize=10)
            ax.set_xlabel(measure_name, fontsize=12)
            ax.set_title(f"Top {top_n} Nodes by {measure_name}", fontsize=14)
            ax.grid(True, axis="x", alpha=0.3)

            # Add value labels
            for i, (bar, val) in enumerate(zip(bars, values)):
                ax.text(
                    bar.get_width(),
                    bar.get_y() + bar.get_height() / 2,
                    f"{val:.2f}" if val < 10 else f"{int(val)}",
                    ha="left",
                    va="center",
                    fontsize=8,
                )

        # Plot different centrality measures
        plot_centrality_bar(ax1, "Degree Centrality", centrality["degree"], "steelblue")
        plot_centrality_bar(
            ax2, "Weighted Degree", centrality["weighted_degree"], "darkgreen"
        )
        plot_centrality_bar(
            ax3, "Eigenvector Centrality", centrality["eigenvector"], "darkred"
        )
        plot_centrality_bar(
            ax4, "Betweenness Centrality", centrality["betweenness"], "darkorange"
        )

        plt.suptitle("Centrality Analysis of Case Hypergraph", fontsize=16)
        plt.tight_layout()
        return fig

    def plot_hyperedge_distribution(
        self, figsize: Tuple[int, int] = (12, 8)
    ) -> plt.Figure:
        """Plot distribution of hyperedge types and sizes"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        # Hyperedge type distribution
        edge_types = defaultdict(int)
        for edge in self.hypergraph.hyperedges.values():
            edge_types[edge.edge_type.value] += 1

        types = list(edge_types.keys())
        counts = list(edge_types.values())
        colors = [
            self.color_schemes["edge_types"].get(HyperedgeType(t), "gray")
            for t in types
        ]

        wedges, texts, autotexts = ax1.pie(
            counts, labels=types, colors=colors, autopct="%1.1f%%", startangle=90
        )
        ax1.set_title("Hyperedge Type Distribution", fontsize=14)

        # Hyperedge size distribution
        edge_sizes = [len(edge.nodes) for edge in self.hypergraph.hyperedges.values()]

        unique_sizes, size_counts = np.unique(edge_sizes, return_counts=True)

        ax2.bar(unique_sizes, size_counts, color="steelblue", alpha=0.7)
        ax2.set_xlabel("Number of nodes in hyperedge", fontsize=12)
        ax2.set_ylabel("Count", fontsize=12)
        ax2.set_title("Hyperedge Size Distribution", fontsize=14)
        ax2.grid(True, axis="y", alpha=0.3)

        # Add statistics
        ax2.text(
            0.95,
            0.95,
            f"Mean: {np.mean(edge_sizes):.2f}\nMax: {np.max(edge_sizes)}",
            transform=ax2.transAxes,
            ha="right",
            va="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )

        plt.tight_layout()
        return fig

    def _add_node_type_legend(self, ax):
        """Add legend for node types"""
        legend_elements = []
        for node_type, color in self.color_schemes["node_types"].items():
            if node_type != "default":
                legend_elements.append(
                    plt.Line2D(
                        [0],
                        [0],
                        marker="o",
                        color="w",
                        markerfacecolor=color,
                        markersize=10,
                        label=node_type.replace("_", " ").title(),
                    )
                )

        ax.legend(handles=legend_elements, loc="best", fontsize=10)

    def save_all_visualizations(self, output_dir: str):
        """Save all visualization types to files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Define all visualizations
        visualizations = [
            ("projection", self.plot_hypergraph_projection),
            ("incidence_matrix", self.plot_incidence_matrix),
            ("similarity_matrix", self.plot_node_similarity_matrix),
            ("communities", self.plot_community_structure),
            ("temporal", self.plot_temporal_evolution),
            ("centrality", self.plot_centrality_analysis),
            ("distributions", self.plot_hyperedge_distribution),
        ]

        for name, plot_func in visualizations:
            try:
                fig = plot_func()
                fig.savefig(output_path / f"{name}.png", dpi=300, bbox_inches="tight")
                plt.close(fig)
                print(f"✅ Saved {name}.png")
            except Exception as e:
                print(f"❌ Failed to save {name}: {str(e)}")


def main():
    """Demonstrate hypergraph visualization"""
    print("=== HYPERGRAPH VISUALIZATION ===\n")

    # Load hypergraph from file if exists
    hypergraph_file = "/workspace/case_hypergraph.json"

    if Path(hypergraph_file).exists():
        print(f"Loading hypergraph from {hypergraph_file}")
        hypergraph = CaseHypergraph.load_from_file(hypergraph_file)
    else:
        print(
            "No saved hypergraph found. Please run case_hypergraph_constructor.py first."
        )
        return

    # Create visualizer
    visualizer = HypergraphVisualizer(hypergraph)

    # Create output directory
    output_dir = "/workspace/hypergraph_visualizations"
    Path(output_dir).mkdir(exist_ok=True)

    # Generate all visualizations
    print(f"\nGenerating visualizations in {output_dir}...")
    visualizer.save_all_visualizations(output_dir)

    print("\n✅ All visualizations complete!")


if __name__ == "__main__":
    main()
