#!/usr/bin/env python3
"""
Fraud Scheme Visualization Generator
Creates comprehensive visualizations of the profit extraction fraud scheme
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
import networkx as nx
import json
from datetime import datetime

def create_fraud_flow_diagram():
    """Create the main fraud flow diagram showing the 4-step scheme"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'RegimA Profit Extraction Fraud Scheme', 
            fontsize=20, fontweight='bold', ha='center')
    ax.text(5, 9.1, 'ZAR 12M+ Monthly Systematic Wealth Transfer (February 2025)', 
            fontsize=14, ha='center', color='red')
    
    # Define entity boxes with ownership indicators
    entities = {
        'SLG': {'pos': (1.5, 7), 'color': '#ff6b6b', 'owner': 'Dan Entity (Victim)', 'size': (1.8, 1.2)},
        'RST': {'pos': (5, 7), 'color': '#4ecdc4', 'owner': 'Non-Dan Entity', 'size': (1.8, 1.2)},
        'RWD': {'pos': (8.5, 7), 'color': '#ff6b6b', 'owner': 'Dan Entity (Victim)', 'size': (1.8, 1.2)},
        'VVA': {'pos': (5, 4), 'color': '#95e1d3', 'owner': 'Non-Dan Entity (Hidden)', 'size': (1.8, 1.2)}
    }
    
    # Draw entity boxes
    for entity, props in entities.items():
        x, y = props['pos']
        w, h = props['size']
        
        # Main entity box
        box = FancyBboxPatch((x-w/2, y-h/2), w, h,
                           boxstyle="round,pad=0.1",
                           facecolor=props['color'],
                           edgecolor='black',
                           linewidth=2)
        ax.add_patch(box)
        
        # Entity name
        ax.text(x, y+0.2, entity, fontsize=14, fontweight='bold', ha='center')
        
        # Full name
        full_names = {
            'SLG': 'Strategic Logistics',
            'RST': 'RegimA Skin Treatments', 
            'RWD': 'RegimA Worldwide Distribution',
            'VVA': 'Villa Via Arcadia'
        }
        ax.text(x, y, full_names[entity], fontsize=10, ha='center')
        
        # Ownership
        ax.text(x, y-0.3, props['owner'], fontsize=9, ha='center', 
                style='italic', color='darkblue')
    
    # Step 1: Asset Stripping (SLG)
    ax.text(1.5, 5.8, 'STEP 1: ASSET STRIPPING', fontsize=12, fontweight='bold', 
            ha='center', color='red')
    ax.text(1.5, 5.5, '• ZAR 5.2M Stock Disappearance', fontsize=10, ha='center')
    ax.text(1.5, 5.3, '• Forced Selling at Losses', fontsize=10, ha='center')
    ax.text(1.5, 5.1, '• Debt Injection → Insolvency', fontsize=10, ha='center')
    
    # Step 2: Profit Generation (RST)
    ax.text(5, 5.8, 'STEP 2: PROFIT GENERATION', fontsize=12, fontweight='bold', 
            ha='center', color='green')
    ax.text(5, 5.5, '• Healthy Profits from Cheap Inventory', fontsize=10, ha='center')
    ax.text(5, 5.3, '• Minimal Expenses (ZAR 16K IT)', fontsize=10, ha='center')
    ax.text(5, 5.1, '• All Employees but Low Costs', fontsize=10, ha='center')
    
    # Step 3: Expense Dumping (RWD)
    ax.text(8.5, 5.8, 'STEP 3: EXPENSE DUMPING', fontsize=12, fontweight='bold', 
            ha='center', color='red')
    ax.text(8.5, 5.5, '• All Company Expenses Dumped', fontsize=10, ha='center')
    ax.text(8.5, 5.3, '• No Employees but All Costs', fontsize=10, ha='center')
    ax.text(8.5, 5.1, '• Systematic Loss Generation', fontsize=10, ha='center')
    
    # Step 4: Final Extraction (VVA)
    ax.text(5, 2.8, 'STEP 4: PROFIT EXTRACTION', fontsize=12, fontweight='bold', 
            ha='center', color='purple')
    ax.text(5, 2.5, '• 86% Profit Margin Rent', fontsize=10, ha='center')
    ax.text(5, 2.3, '• ZAR 4M+ Pete Enrichment', fontsize=10, ha='center')
    ax.text(5, 2.1, '• Hidden Outside "Group"', fontsize=10, ha='center')
    
    # Draw flow arrows
    # SLG to RST (inventory transfer)
    arrow1 = ConnectionPatch((2.4, 7), (4.1, 7), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5,
                           mutation_scale=20, fc="red", ec="red", lw=3)
    ax.add_patch(arrow1)
    ax.text(3.25, 7.3, 'Below-Cost\nInventory', fontsize=9, ha='center', color='red')
    
    # RST to RWD (expense transfer)
    arrow2 = ConnectionPatch((5.9, 7), (7.6, 7), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5,
                           mutation_scale=20, fc="orange", ec="orange", lw=3)
    ax.add_patch(arrow2)
    ax.text(6.75, 7.3, 'Expense\nDumping', fontsize=9, ha='center', color='orange')
    
    # RST to VVA (rent extraction)
    arrow3 = ConnectionPatch((5, 6.4), (5, 5.2), "data", "data",
                           arrowstyle="->", shrinkA=5, shrinkB=5,
                           mutation_scale=20, fc="purple", ec="purple", lw=3)
    ax.add_patch(arrow3)
    ax.text(5.5, 5.8, 'Rent\nExtraction', fontsize=9, ha='center', color='purple')
    
    # Add financial impact summary
    summary_box = FancyBboxPatch((0.2, 0.2), 9.6, 1.5,
                               boxstyle="round,pad=0.1",
                               facecolor='lightyellow',
                               edgecolor='black',
                               linewidth=2)
    ax.add_patch(summary_box)
    
    ax.text(5, 1.4, 'FINANCIAL IMPACT SUMMARY', fontsize=14, fontweight='bold', ha='center')
    ax.text(2.5, 1.0, 'Dan Entity Losses:', fontsize=11, fontweight='bold', ha='left')
    ax.text(2.5, 0.8, '• SLG: ZAR 5.2M+ (stock + losses)', fontsize=10, ha='left')
    ax.text(2.5, 0.6, '• RWD: Unknown (expense dumping)', fontsize=10, ha='left')
    ax.text(2.5, 0.4, '• Total: ZAR 12M+ systematic transfer', fontsize=10, ha='left', color='red')
    
    ax.text(7.5, 1.0, 'Non-Dan Entity Gains:', fontsize=11, fontweight='bold', ha='left')
    ax.text(7.5, 0.8, '• RST: Artificial profits', fontsize=10, ha='left')
    ax.text(7.5, 0.6, '• VVA: ZAR 4M+ Pete enrichment', fontsize=10, ha='left')
    ax.text(7.5, 0.4, '• Total: ZAR 4M+ identified gains', fontsize=10, ha='left', color='green')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analysis/fraud_scheme_flow_diagram.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_ownership_intersection_fraud_map():
    """Create visualization showing how ownership intersections enable fraud"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Ownership Intersections Enable Systematic Fraud', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Shareholder positions
    shareholders = {
        'Dan': {'pos': (2, 7.5), 'color': '#ff9999', 'groups': 3, 'entities': 14},
        'Pete': {'pos': (5, 8.5), 'color': '#99ff99', 'groups': 3, 'entities': 11},
        'Jax': {'pos': (8, 7.5), 'color': '#9999ff', 'groups': 2, 'entities': 10}
    }
    
    # Draw shareholder circles
    for name, props in shareholders.items():
        x, y = props['pos']
        circle = plt.Circle((x, y), 0.8, facecolor=props['color'], 
                          edgecolor='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y+0.1, name, fontsize=12, fontweight='bold', ha='center')
        ax.text(x, y-0.1, f"{props['groups']} groups", fontsize=10, ha='center')
        ax.text(x, y-0.3, f"{props['entities']} entities", fontsize=10, ha='center')
    
    # Legal groups
    groups = {
        'J_P': {'pos': (1.5, 5), 'entities': ['RST', 'VVA'], 'color': '#e6ffe6'},
        'D_J_P': {'pos': (5, 5), 'entities': ['SLG', 'RWD'], 'color': '#ffe6e6'},
        'D_P': {'pos': (8.5, 5), 'entities': ['RegimA SA'], 'color': '#ffe6f0'},
        'D_Only': {'pos': (2, 2.5), 'entities': ['8 entities'], 'color': '#f0e6ff'}
    }
    
    # Draw group boxes
    for group, props in groups.items():
        x, y = props['pos']
        box = FancyBboxPatch((x-0.8, y-0.6), 1.6, 1.2,
                           boxstyle="round,pad=0.1",
                           facecolor=props['color'],
                           edgecolor='black',
                           linewidth=1)
        ax.add_patch(box)
        ax.text(x, y+0.2, group.replace('_', ' '), fontsize=11, fontweight='bold', ha='center')
        for i, entity in enumerate(props['entities']):
            ax.text(x, y-0.1-i*0.2, entity, fontsize=9, ha='center')
    
    # Draw intersection lines showing fraud enablement
    # Pete to J_P (benefits)
    ax.plot([5, 1.5], [7.7, 5.6], 'g-', linewidth=3, alpha=0.7)
    ax.text(3, 6.8, 'Benefits\n(RST+VVA)', fontsize=9, ha='center', color='green')
    
    # Pete to D_J_P (swing vote)
    ax.plot([5, 5], [7.7, 5.6], 'r-', linewidth=3, alpha=0.7)
    ax.text(5.5, 6.8, 'Swing Vote\n(Controls SLG+RWD)', fontsize=9, ha='center', color='red')
    
    # Dan vulnerability lines
    ax.plot([2, 5], [6.7, 5.6], 'r--', linewidth=2, alpha=0.7)
    ax.text(3.5, 6, 'Victim Entities', fontsize=9, ha='center', color='red')
    
    # Fraud mechanism explanation
    fraud_box = FancyBboxPatch((0.2, 0.2), 9.6, 1.8,
                             boxstyle="round,pad=0.1",
                             facecolor='lightcoral',
                             edgecolor='black',
                             linewidth=2)
    ax.add_patch(fraud_box)
    
    ax.text(5, 1.7, 'FRAUD ENABLEMENT MECHANISM', fontsize=14, fontweight='bold', ha='center')
    ax.text(5, 1.4, 'Pete\'s Strategic Position: Swing vote in D_J_P group + Benefits in J_P group', 
            fontsize=11, ha='center', fontweight='bold')
    ax.text(5, 1.1, '1. Uses swing vote to control SLG & RWD decisions (victim entities)', 
            fontsize=10, ha='center')
    ax.text(5, 0.9, '2. Benefits from RST profits and VVA rent extraction (beneficiary entities)', 
            fontsize=10, ha='center')
    ax.text(5, 0.7, '3. Systematic wealth transfer: Dan entities → Non-Dan entities', 
            fontsize=10, ha='center')
    ax.text(5, 0.5, '4. ZAR 4M+ personal enrichment while complaining about "group losses"', 
            fontsize=10, ha='center', color='darkred', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analysis/ownership_intersection_fraud_map.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_financial_flow_network():
    """Create network diagram showing financial flows"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    
    # Create network graph
    G = nx.DiGraph()
    
    # Add nodes with attributes
    entities = {
        'SLG': {'type': 'victim', 'owner': 'Dan', 'pos': (0, 1)},
        'RST': {'type': 'beneficiary', 'owner': 'Non-Dan', 'pos': (2, 1)},
        'RWD': {'type': 'victim', 'owner': 'Dan', 'pos': (4, 1)},
        'VVA': {'type': 'extractor', 'owner': 'Non-Dan', 'pos': (2, -1)},
        'Pete': {'type': 'person', 'owner': 'Self', 'pos': (2, -2)}
    }
    
    for entity, attrs in entities.items():
        G.add_node(entity, **attrs)
    
    # Add edges with financial flows
    flows = [
        ('SLG', 'RST', {'amount': 'ZAR 5.2M+', 'type': 'inventory_transfer', 'color': 'red'}),
        ('RST', 'RWD', {'amount': 'All Expenses', 'type': 'expense_dump', 'color': 'orange'}),
        ('RST', 'VVA', {'amount': 'Profits', 'type': 'rent_payment', 'color': 'purple'}),
        ('VVA', 'Pete', {'amount': 'ZAR 4M+', 'type': 'extraction', 'color': 'green'})
    ]
    
    for source, target, attrs in flows:
        G.add_edge(source, target, **attrs)
    
    # Set positions
    pos = {node: entities[node]['pos'] for node in G.nodes()}
    
    # Draw nodes
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if entities[node]['type'] == 'victim':
            node_colors.append('#ff6b6b')
            node_sizes.append(3000)
        elif entities[node]['type'] == 'beneficiary':
            node_colors.append('#4ecdc4')
            node_sizes.append(3000)
        elif entities[node]['type'] == 'extractor':
            node_colors.append('#95e1d3')
            node_sizes.append(3000)
        else:  # person
            node_colors.append('#ffd93d')
            node_sizes.append(2000)
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', ax=ax)
    
    # Draw edges with different colors and styles
    for edge in G.edges(data=True):
        source, target, attrs = edge
        color = attrs['color']
        nx.draw_networkx_edges(G, pos, [(source, target)], 
                             edge_color=color, width=3, 
                             arrowsize=20, arrowstyle='->', ax=ax)
        
        # Add edge labels
        edge_pos = ((pos[source][0] + pos[target][0])/2, 
                   (pos[source][1] + pos[target][1])/2)
        ax.text(edge_pos[0], edge_pos[1]+0.1, attrs['amount'], 
               fontsize=10, ha='center', fontweight='bold', 
               bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # Add title and legend
    ax.set_title('Financial Flow Network - Fraud Scheme\nZAR 12M+ Monthly Systematic Transfer', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Create legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#ff6b6b', 
                  markersize=15, label='Victim Entities (Dan)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4ecdc4', 
                  markersize=15, label='Beneficiary Entities (Non-Dan)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#95e1d3', 
                  markersize=15, label='Extraction Entities (Hidden)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#ffd93d', 
                  markersize=15, label='Individual Beneficiary')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analysis/financial_flow_network.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_concealment_mechanism_diagram():
    """Create diagram showing how the fraud is concealed"""
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
    
    # Top: False Group Framing
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 5)
    ax1.axis('off')
    ax1.text(5, 4.5, 'CONCEALMENT MECHANISM 1: False Group Framing', 
            fontsize=16, fontweight='bold', ha='center')
    
    # False group box
    false_group = FancyBboxPatch((1, 2), 6, 1.5,
                               boxstyle="round,pad=0.1",
                               facecolor='lightblue',
                               edgecolor='blue',
                               linewidth=2)
    ax1.add_patch(false_group)
    ax1.text(4, 3, 'FALSE "GROUP"', fontsize=14, fontweight='bold', ha='center')
    ax1.text(2, 2.7, 'SLG', fontsize=12, ha='center')
    ax1.text(4, 2.7, 'RST', fontsize=12, ha='center')
    ax1.text(6, 2.7, 'RWD', fontsize=12, ha='center')
    ax1.text(4, 2.3, 'Framed as single group to hide extraction', fontsize=10, ha='center', style='italic')
    
    # Hidden extractor
    hidden_box = FancyBboxPatch((8, 2.5), 1.5, 1,
                              boxstyle="round,pad=0.1",
                              facecolor='lightcoral',
                              edgecolor='red',
                              linewidth=2,
                              linestyle='--')
    ax1.add_patch(hidden_box)
    ax1.text(8.75, 3, 'VVA', fontsize=12, fontweight='bold', ha='center')
    ax1.text(8.75, 2.7, 'HIDDEN', fontsize=10, ha='center', color='red')
    
    # Arrow showing extraction
    arrow = ConnectionPatch((7, 2.75), (8, 2.75), "data", "data",
                          arrowstyle="->", shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc="red", ec="red", lw=3)
    ax1.add_patch(arrow)
    ax1.text(7.5, 3.2, 'ZAR 4M+\nExtraction', fontsize=10, ha='center', color='red')
    
    ax1.text(5, 1.5, 'Makes rent extraction appear as external transaction rather than internal theft', 
            fontsize=12, ha='center', style='italic', color='darkblue')
    
    # Bottom: Victim Blaming Narrative
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 5)
    ax2.axis('off')
    ax2.text(5, 4.5, 'CONCEALMENT MECHANISM 2: Victim Blaming Narrative', 
            fontsize=16, fontweight='bold', ha='center')
    
    # Pete's complaint
    complaint_box = FancyBboxPatch((0.5, 2.5), 4, 1.5,
                                 boxstyle="round,pad=0.1",
                                 facecolor='lightyellow',
                                 edgecolor='orange',
                                 linewidth=2)
    ax2.add_patch(complaint_box)
    ax2.text(2.5, 3.5, 'PETE\'S COMPLAINT', fontsize=12, fontweight='bold', ha='center')
    ax2.text(2.5, 3.2, '"Group made loss because of', fontsize=10, ha='center')
    ax2.text(2.5, 3.0, 'Danny\'s IT expenses"', fontsize=10, ha='center')
    ax2.text(2.5, 2.7, '(Blames victim for engineered losses)', fontsize=9, ha='center', style='italic')
    
    # Reality
    reality_box = FancyBboxPatch((5.5, 2.5), 4, 1.5,
                               boxstyle="round,pad=0.1",
                               facecolor='lightgreen',
                               edgecolor='green',
                               linewidth=2)
    ax2.add_patch(reality_box)
    ax2.text(7.5, 3.5, 'REALITY', fontsize=12, fontweight='bold', ha='center')
    ax2.text(7.5, 3.2, 'Pete extracted ZAR 4M+', fontsize=10, ha='center')
    ax2.text(7.5, 3.0, 'through VVA rent mechanism', fontsize=10, ha='center')
    ax2.text(7.5, 2.7, '(Enriched while complaining)', fontsize=9, ha='center', style='italic')
    
    # Hypocrisy arrow
    hypocrisy_arrow = ConnectionPatch((4.5, 3.25), (5.5, 3.25), "data", "data",
                                    arrowstyle="<->", shrinkA=5, shrinkB=5,
                                    mutation_scale=20, fc="red", ec="red", lw=3)
    ax2.add_patch(hypocrisy_arrow)
    ax2.text(5, 3.7, 'HYPOCRISY', fontsize=11, fontweight='bold', ha='center', color='red')
    
    # Evidence box
    evidence_box = FancyBboxPatch((2, 0.5), 6, 1.5,
                                boxstyle="round,pad=0.1",
                                facecolor='lightcoral',
                                edgecolor='red',
                                linewidth=2)
    ax2.add_patch(evidence_box)
    ax2.text(5, 1.7, 'EVIDENCE OF EXPENSE FRAUD', fontsize=12, fontweight='bold', ha='center')
    ax2.text(5, 1.4, 'RWD: No employees but carries ALL expenses', fontsize=10, ha='center')
    ax2.text(5, 1.2, 'RST: All employees but only ZAR 16K IT expenses', fontsize=10, ha='center')
    ax2.text(5, 1.0, 'Systematic expense dumping in Dan entities', fontsize=10, ha='center')
    ax2.text(5, 0.8, 'while minimizing costs in non-Dan entities', fontsize=10, ha='center')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analysis/concealment_mechanism_diagram.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_historical_impact_projection():
    """Create visualization of potential historical impact"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Left: Monthly progression
    months = ['Feb 2025', 'Mar 2025', 'Apr 2025', 'May 2025', 'Jun 2025', 'Jul 2025']
    identified = [12, 0, 0, 0, 0, 0]  # Only Feb identified
    projected = [12, 12, 12, 12, 12, 12]  # If sustained
    
    x = np.arange(len(months))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, identified, width, label='Identified Fraud', color='red', alpha=0.7)
    bars2 = ax1.bar(x + width/2, projected, width, label='Projected if Sustained', color='orange', alpha=0.7)
    
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Fraud Amount (ZAR Millions)')
    ax1.set_title('Monthly Fraud Projection\n(Based on February 2025 Evidence)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(months, rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        if height > 0:
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'ZAR {height}M', ha='center', va='bottom', fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        if height > 0:
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'ZAR {height}M', ha='center', va='bottom', fontweight='bold')
    
    # Right: Historical scenarios
    scenarios = ['Conservative\n(6 months)', 'Moderate\n(2 years)', 'Extensive\n(5 years)']
    amounts = [72, 288, 720]  # 6*12, 24*12, 60*12
    colors = ['yellow', 'orange', 'red']
    
    bars = ax2.bar(scenarios, amounts, color=colors, alpha=0.7)
    ax2.set_ylabel('Total Fraud Amount (ZAR Millions)')
    ax2.set_title('Historical Fraud Scenarios\n"Who knows how much previously?"')
    ax2.grid(True, alpha=0.3)
    
    # Add value labels
    for bar, amount in zip(bars, amounts):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 10,
                f'ZAR {amount}M', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    # Add February 2025 reference line
    ax2.axhline(y=12, color='red', linestyle='--', linewidth=2, alpha=0.8)
    ax2.text(1, 15, 'February 2025\nIdentified: ZAR 12M', ha='center', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analysis/historical_impact_projection.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_interactive_fraud_dashboard():
    """Create HTML dashboard with all visualizations"""
    
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RegimA Fraud Scheme Analysis Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            text-align: center;
            background-color: #dc3545;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        .visualization-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .full-width {
            grid-column: 1 / -1;
        }
        .visualization-card h3 {
            margin-top: 0;
            color: #333;
            border-bottom: 2px solid #dc3545;
            padding-bottom: 10px;
        }
        .visualization-card img {
            width: 100%;
            height: auto;
            border-radius: 5px;
        }
        .key-findings {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        .critical-alert {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        .financial-summary {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .metric-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚨 RegimA Profit Extraction Fraud Scheme Analysis</h1>
        <h2>ZAR 12M+ Monthly Systematic Wealth Transfer</h2>
        <p>Criminal Conspiracy Discovery - February 2025 Evidence</p>
    </div>

    <div class="financial-summary">
        <div class="metric-card">
            <div class="metric-value">ZAR 12M+</div>
            <div class="metric-label">Monthly Transfer<br>(February 2025)</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">ZAR 4M+</div>
            <div class="metric-label">Pete's Enrichment<br>(VVA Extraction)</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">ZAR 5.2M</div>
            <div class="metric-label">Stock Disappearance<br>(SLG Asset Stripping)</div>
        </div>
    </div>

    <div class="critical-alert">
        <h3>🚨 CRITICAL CRIMINAL FRAUD DISCOVERY</h3>
        <p><strong>Scheme Type:</strong> Systematic profit extraction using ownership intersections to mask criminal wealth transfer</p>
        <p><strong>Sophistication:</strong> HIGH - Multi-entity coordinated fraud exploiting complex ownership structure</p>
        <p><strong>Legal Violations:</strong> Corporate law, tax law, criminal fraud, fiduciary duty breaches</p>
        <p><strong>Historical Risk:</strong> Unknown duration - "Who knows how much this has been done previously?"</p>
    </div>

    <div class="dashboard-grid">
        <div class="visualization-card full-width">
            <h3>Fraud Scheme Flow Diagram</h3>
            <img src="fraud_scheme_flow_diagram.png" alt="Fraud Scheme Flow">
            <p>Complete 4-step fraud mechanism showing systematic wealth transfer from Dan entities to non-Dan entities through coordinated asset stripping, profit generation, expense dumping, and final extraction.</p>
        </div>

        <div class="visualization-card">
            <h3>Ownership Intersection Fraud Map</h3>
            <img src="ownership_intersection_fraud_map.png" alt="Ownership Intersection Map">
            <p>Shows how Pete's strategic position across multiple groups enables systematic fraud through swing vote control and beneficiary positioning.</p>
        </div>

        <div class="visualization-card">
            <h3>Financial Flow Network</h3>
            <img src="financial_flow_network.png" alt="Financial Flow Network">
            <p>Network diagram illustrating the systematic financial flows from victim entities (Dan) to beneficiary entities (Non-Dan) culminating in Pete's personal enrichment.</p>
        </div>

        <div class="visualization-card full-width">
            <h3>Concealment Mechanisms</h3>
            <img src="concealment_mechanism_diagram.png" alt="Concealment Mechanisms">
            <p>Detailed analysis of how the fraud is concealed through false group framing and victim blaming narratives while Pete extracts ZAR 4M+ and complains about "group losses."</p>
        </div>

        <div class="visualization-card full-width">
            <h3>Historical Impact Projection</h3>
            <img src="historical_impact_projection.png" alt="Historical Impact">
            <p>Projection of potential historical fraud scope based on February 2025 evidence. Conservative estimates suggest ZAR 72M+ over 6 months, with extensive scenarios reaching ZAR 720M+ over 5 years.</p>
        </div>
    </div>

    <div class="key-findings">
        <h3>🔍 Key Fraud Scheme Components</h3>
        <ul>
            <li><strong>Asset Stripping (SLG):</strong> ZAR 5.2M stock disappearance, forced selling at losses, debt injection causing insolvency</li>
            <li><strong>Profit Generation (RST):</strong> Healthy profits from below-cost inventory, minimal expenses despite all employees</li>
            <li><strong>Expense Dumping (RWD):</strong> All company expenses dumped despite no employees, systematic loss generation</li>
            <li><strong>Final Extraction (VVA):</strong> 86% profit margin rent extraction, ZAR 4M+ Pete enrichment, hidden outside "group"</li>
        </ul>
        
        <h3>🎭 Concealment Tactics</h3>
        <ul>
            <li><strong>False Group Framing:</strong> SLG-RST-RWD presented as "group" while VVA hidden to mask extraction</li>
            <li><strong>Victim Blaming:</strong> Pete complains about "Danny's IT expenses" while extracting ZAR 4M+</li>
            <li><strong>Expense Attribution Fraud:</strong> IT costs blamed on Dan despite RWD having no employees but all expenses</li>
            <li><strong>Ownership Complexity Exploitation:</strong> Uses intersections to confuse regulators and mask systematic theft</li>
        </ul>
    </div>

    <div class="critical-alert">
        <h3>⚖️ Legal Violations Identified</h3>
        <p><strong>Corporate Law:</strong> Director duty breaches, fraudulent trading, asset stripping, insolvent trading</p>
        <p><strong>Tax Law:</strong> Transfer pricing manipulation, artificial expense allocation, income shifting, tax avoidance</p>
        <p><strong>Criminal Law:</strong> Systematic fraud, asset misappropriation, financial statement fraud, conspiracy to defraud</p>
        <p><strong>Fiduciary Duties:</strong> Breach of fiduciary duty, conflicts of interest, duty of loyalty violations</p>
        
        <h3>🚨 IMMEDIATE ACTIONS REQUIRED</h3>
        <ol>
            <li><strong>Forensic Investigation:</strong> Full forensic accounting of all inter-entity transactions</li>
            <li><strong>Asset Tracing:</strong> Trace ZAR 5.2M stock disappearance and recovery action</li>
            <li><strong>Legal Recovery:</strong> Initiate legal action for fraudulent asset recovery</li>
            <li><strong>Regulatory Reporting:</strong> Report to SARS, CIPC, and law enforcement</li>
            <li><strong>Injunctive Relief:</strong> Prevent further asset stripping and fraud continuation</li>
        </ol>
    </div>

    <div style="text-align: center; margin-top: 30px; padding: 20px; background-color: #e9ecef; border-radius: 10px;">
        <p><strong>Analysis Date:</strong> October 11, 2025</p>
        <p><strong>Discovery Method:</strong> Trial balance analysis + ownership intersection modeling</p>
        <p><strong>Evidence Source:</strong> February 2025 financial data revealing systematic fraud patterns</p>
        <p><strong>Criminal Liability:</strong> Multiple parties involved in coordinated conspiracy to defraud</p>
    </div>
</body>
</html>
"""
    
    with open('/home/ubuntu/analysis/fraud_scheme_dashboard.html', 'w') as f:
        f.write(html_content)

def main():
    """Generate all fraud scheme visualizations"""
    
    print("🎨 Generating Fraud Scheme Visualizations...")
    print("=" * 60)
    
    # Create all visualizations
    create_fraud_flow_diagram()
    print("✅ Fraud flow diagram created")
    
    create_ownership_intersection_fraud_map()
    print("✅ Ownership intersection fraud map created")
    
    create_financial_flow_network()
    print("✅ Financial flow network created")
    
    create_concealment_mechanism_diagram()
    print("✅ Concealment mechanism diagram created")
    
    create_historical_impact_projection()
    print("✅ Historical impact projection created")
    
    create_interactive_fraud_dashboard()
    print("✅ Interactive fraud dashboard created")
    
    # Create summary of visualizations
    summary = {
        'visualizations_created': [
            'fraud_scheme_flow_diagram.png',
            'ownership_intersection_fraud_map.png', 
            'financial_flow_network.png',
            'concealment_mechanism_diagram.png',
            'historical_impact_projection.png',
            'fraud_scheme_dashboard.html'
        ],
        'key_insights_visualized': [
            'ZAR 12M+ monthly systematic transfer mechanism',
            'Pete\'s swing vote position enabling fraud',
            'Asset stripping and profit extraction flows',
            'Concealment through false group framing',
            'Potential ZAR 720M+ historical fraud scope'
        ],
        'fraud_components_mapped': [
            'SLG asset stripping (ZAR 5.2M stock disappearance)',
            'RST profit generation (artificial profits)',
            'RWD expense dumping (no employees, all costs)',
            'VVA final extraction (ZAR 4M+ Pete enrichment)'
        ]
    }
    
    with open('/home/ubuntu/analysis/fraud_visualizations_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n🎯 Visualization Summary:")
    print(f"   Total visualizations: {len(summary['visualizations_created'])}")
    print(f"   Fraud value mapped: ZAR 12M+ monthly")
    print(f"   Historical projection: Up to ZAR 720M+")
    print(f"   Interactive dashboard: fraud_scheme_dashboard.html")
    
    return summary

if __name__ == "__main__":
    main()
