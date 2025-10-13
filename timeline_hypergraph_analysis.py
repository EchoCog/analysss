#!/usr/bin/env python3
"""
Timeline Hypergraph Analysis
Generates comprehensive hypergraph analysis and visualization of timeline data
"""

import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Timeline data from Neon query
TIMELINE_DATA = [
    {"id": 8, "event_date": "2017-06-30", "phase": "Business Relationship Development", "phase_number": 2, "is_critical": False, "entity_count": 2, "transaction_count": 1, "total_amount": 501.60},
    {"id": 9, "event_date": "2017-09-30", "phase": "Business Relationship Development", "phase_number": 2, "is_critical": False, "entity_count": 2, "transaction_count": 1, "total_amount": 200000.00},
    {"id": 2, "event_date": "2019-03-01", "phase": "Financial Structure Establishment", "phase_number": 1, "is_critical": False, "entity_count": 2, "transaction_count": 0, "total_amount": 0},
    {"id": 3, "event_date": "2019-05-01", "phase": "Financial Structure Establishment", "phase_number": 1, "is_critical": False, "entity_count": 1, "transaction_count": 0, "total_amount": 0},
    {"id": 4, "event_date": "2020-02-20", "phase": "Financial Structure Establishment", "phase_number": 1, "is_critical": True, "entity_count": 3, "transaction_count": 4, "total_amount": 4926000.00},
    {"id": 5, "event_date": "2020-02-28", "phase": "Financial Structure Establishment", "phase_number": 1, "is_critical": True, "entity_count": 3, "transaction_count": 3, "total_amount": 5845002.27},
    {"id": 6, "event_date": "2020-04-30", "phase": "Financial Structure Establishment", "phase_number": 1, "is_critical": True, "entity_count": 1, "transaction_count": 3, "total_amount": 30900000.00},
    {"id": 7, "event_date": "2020-08-13", "phase": "Financial Structure Establishment", "phase_number": 1, "is_critical": False, "entity_count": 6, "transaction_count": 0, "total_amount": 0},
    {"id": 10, "event_date": "2022-03-01", "phase": "Debt Accumulation and Manipulation", "phase_number": 3, "is_critical": True, "entity_count": 2, "transaction_count": 1, "total_amount": 1943175.86},
    {"id": 11, "event_date": "2022-07-11", "phase": "Debt Accumulation and Manipulation", "phase_number": 3, "is_critical": False, "entity_count": 2, "transaction_count": 1, "total_amount": 80000.00},
    {"id": 12, "event_date": "2023-02-28", "phase": "Debt Accumulation and Manipulation", "phase_number": 3, "is_critical": True, "entity_count": 2, "transaction_count": 1, "total_amount": 2070722.68},
    {"id": 13, "event_date": "2023-03-15", "phase": "Debt Accumulation and Manipulation", "phase_number": 3, "is_critical": True, "entity_count": 2, "transaction_count": 1, "total_amount": 940000.00},
    {"id": 14, "event_date": "2023-09-20", "phase": "Debt Accumulation and Manipulation", "phase_number": 3, "is_critical": True, "entity_count": 2, "transaction_count": 1, "total_amount": 1530722.68},
    {"id": 15, "event_date": "2025-04-15", "phase": "Fraud Discovery and Cover-up", "phase_number": 4, "is_critical": True, "entity_count": 1, "transaction_count": 0, "total_amount": 0},
    {"id": 16, "event_date": "2025-05-15", "phase": "Fraud Discovery and Cover-up", "phase_number": 4, "is_critical": True, "entity_count": 4, "transaction_count": 0, "total_amount": 0},
    {"id": 17, "event_date": "2025-05-22", "phase": "Fraud Discovery and Cover-up", "phase_number": 4, "is_critical": True, "entity_count": 1, "transaction_count": 0, "total_amount": 0},
    {"id": 18, "event_date": "2025-05-29", "phase": "Fraud Discovery and Cover-up", "phase_number": 4, "is_critical": True, "entity_count": 3, "transaction_count": 0, "total_amount": 0},
    {"id": 19, "event_date": "2025-06-07", "phase": "Fraud Discovery and Cover-up", "phase_number": 4, "is_critical": True, "entity_count": 1, "transaction_count": 0, "total_amount": 0},
    {"id": 20, "event_date": "2025-07-02", "phase": "Fraud Discovery and Cover-up", "phase_number": 4, "is_critical": False, "entity_count": 2, "transaction_count": 0, "total_amount": 0},
    {"id": 21, "event_date": "2025-07-07", "phase": "Fraud Discovery and Cover-up", "phase_number": 4, "is_critical": False, "entity_count": 1, "transaction_count": 0, "total_amount": 0},
    {"id": 22, "event_date": "2025-10-09", "phase": "Fraud Discovery and Cover-up", "phase_number": 4, "is_critical": True, "entity_count": 2, "transaction_count": 1, "total_amount": 2470722.68},
    {"id": 23, "event_date": "2025-10-12", "phase": "Fraud Discovery and Cover-up", "phase_number": 4, "is_critical": True, "entity_count": 3, "transaction_count": 1, "total_amount": 35700000.00},
]

ENTITY_DATA = [
    {"entity_name": "RegimA Group", "entity_type": "Group", "event_count": 11, "roles": "Client, Control consolidator, Debtor, Evidence destroyer, False claimant, Payer, Perpetrator, Target"},
    {"entity_name": "ReZonance", "entity_type": "Company", "event_count": 9, "roles": "Creditor, Payee, Service provider, Victim"},
    {"entity_name": "RegimA Skin Treatments", "entity_type": "Company", "event_count": 4, "roles": "Client, Cost recipient, Financial year start, Interest receiver"},
    {"entity_name": "Rynette Farrar", "entity_type": "Person", "event_count": 3, "roles": "Beneficiary, CC recipient, Confronted party"},
    {"entity_name": "Daniel Faucitt", "entity_type": "Person", "event_count": 3, "roles": "Beneficiary, CC recipient, CIO (RWW)"},
    {"entity_name": "Strategic Logistics", "entity_type": "Company", "event_count": 3, "roles": "Cost reallocation, Financial year start, Interest payer"},
    {"entity_name": "Villa Via", "entity_type": "Company", "event_count": 2, "roles": "Financial year start, Rental income vehicle"},
    {"entity_name": "Jacqui Faucitt", "entity_type": "Person", "event_count": 2, "roles": "CC recipient, Fraud detector (RST CEO)"},
    {"entity_name": "RegimA Worldwide", "entity_type": "Company", "event_count": 2, "roles": "Cost dumping ground, Loan recipient"},
    {"entity_name": "Peter Faucitt", "entity_type": "Person", "event_count": 1, "roles": "Beneficiary"},
    {"entity_name": "RegimA UK", "entity_type": "Company", "event_count": 1, "roles": "Extraction vehicle"},
    {"entity_name": "Adderory", "entity_type": "Person", "event_count": 1, "roles": "Domain purchaser (Rynette's son)"},
]

TRANSACTION_DATA = [
    {"from_entity": "Villa Via", "to_entity": None, "transaction_type": "Capital Extraction", "total_amount": 22800000.00},
    {"from_entity": "RegimA SA", "to_entity": "RegimA UK", "transaction_type": "International Transfer", "total_amount": 11900000.00},
    {"from_entity": None, "to_entity": "Villa Via", "transaction_type": "Revenue", "total_amount": 4400000.00},
    {"from_entity": None, "to_entity": "Villa Via", "transaction_type": "Profit", "total_amount": 3700000.00},
    {"from_entity": "RegimA Group", "to_entity": "ReZonance", "transaction_type": "Debt", "total_amount": 2006949.27},
    {"from_entity": "RegimA Group", "to_entity": "ReZonance", "transaction_type": "Fraud", "total_amount": 1235361.34},
    {"from_entity": "RegimA Group", "to_entity": "ReZonance", "transaction_type": "Fraudulent Claim", "total_amount": 1235361.34},
    {"from_entity": "RWW", "to_entity": None, "transaction_type": "Reallocation", "total_amount": 810000.00},
    {"from_entity": "RST", "to_entity": None, "transaction_type": "Adjustment", "total_amount": 784000.00},
    {"from_entity": "RST", "to_entity": "RWW", "transaction_type": "Loan", "total_amount": 750000.00},
    {"from_entity": "SLG", "to_entity": "RST", "transaction_type": "Interest", "total_amount": 414334.09},
]

def create_timeline_visualization():
    """Create timeline visualization showing events, phases, and criticality"""
    fig, ax = plt.subplots(figsize=(20, 12))
    
    # Parse dates and prepare data
    dates = [datetime.strptime(event['event_date'], '%Y-%m-%d') for event in TIMELINE_DATA]
    phases = [event['phase_number'] for event in TIMELINE_DATA]
    critical = [event['is_critical'] for event in TIMELINE_DATA]
    amounts = [event['total_amount'] for event in TIMELINE_DATA]
    
    # Normalize amounts for bubble size
    max_amount = max(amounts) if max(amounts) > 0 else 1
    sizes = [max(50, (amount / max_amount) * 1000) if amount > 0 else 50 for amount in amounts]
    
    # Color mapping for phases
    phase_colors = {
        1: '#3498db',  # Blue - Financial Structure
        2: '#2ecc71',  # Green - Business Development
        3: '#f39c12',  # Orange - Debt Accumulation
        4: '#e74c3c'   # Red - Fraud Discovery
    }
    
    colors = [phase_colors.get(phase, '#95a5a6') for phase in phases]
    
    # Plot events
    for i, (date, phase, is_crit, size, color, event) in enumerate(zip(dates, phases, critical, sizes, colors, TIMELINE_DATA)):
        # Use phase number as y-coordinate
        y = phase
        
        # Draw event bubble
        if is_crit:
            ax.scatter(date, y, s=size, c=color, alpha=0.7, edgecolors='red', linewidths=3, zorder=3)
        else:
            ax.scatter(date, y, s=size, c=color, alpha=0.5, edgecolors='black', linewidths=1, zorder=2)
    
    # Add phase labels and backgrounds
    phase_labels = {
        1: 'Phase 1: Financial Structure\nEstablishment (2019-2020)',
        2: 'Phase 2: Business Relationship\nDevelopment (2017-2021)',
        3: 'Phase 3: Debt Accumulation\n& Manipulation (2022-2023)',
        4: 'Phase 4: Fraud Discovery\n& Cover-up (2025)'
    }
    
    for phase_num, label in phase_labels.items():
        ax.axhspan(phase_num - 0.4, phase_num + 0.4, alpha=0.1, color=phase_colors[phase_num])
        ax.text(datetime(2016, 1, 1), phase_num, label, 
                fontsize=10, fontweight='bold', va='center', ha='left',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=phase_colors[phase_num], alpha=0.3))
    
    # Formatting
    ax.set_xlabel('Timeline', fontsize=14, fontweight='bold')
    ax.set_ylabel('Phase', fontsize=14, fontweight='bold')
    ax.set_title('Timeline Hypergraph: Fraud Scheme Evolution (2017-2025)\nBubble Size = Transaction Amount | Red Border = Critical Event', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0.5, 4.5)
    ax.set_yticks([1, 2, 3, 4])
    ax.set_yticklabels(['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'])
    ax.grid(True, alpha=0.3, axis='x')
    
    # Legend
    legend_elements = [
        mpatches.Patch(color='#3498db', label='Phase 1: Financial Structure', alpha=0.7),
        mpatches.Patch(color='#2ecc71', label='Phase 2: Business Development', alpha=0.7),
        mpatches.Patch(color='#f39c12', label='Phase 3: Debt Accumulation', alpha=0.7),
        mpatches.Patch(color='#e74c3c', label='Phase 4: Fraud & Cover-up', alpha=0.7),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
                   markersize=10, markeredgecolor='red', markeredgewidth=3, label='Critical Event')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analysis/timeline_hypergraph_visualization.png', dpi=300, bbox_inches='tight')
    print("✓ Timeline visualization saved")
    return fig

def create_entity_network_visualization():
    """Create entity relationship network visualization"""
    fig, ax = plt.subplots(figsize=(18, 14))
    
    # Entity positioning (manual layout for clarity)
    entity_positions = {
        # Central fraud actors
        "RegimA Group": (0, 0),
        "ReZonance": (5, 0),
        
        # RegimA entities
        "RegimA Skin Treatments": (-2, 2),
        "Strategic Logistics": (-2, -2),
        "RegimA Worldwide": (0, -3),
        "Villa Via": (-4, 0),
        "RegimA UK": (-4, -2),
        
        # Key people
        "Jacqui Faucitt": (3, 3),
        "Rynette Farrar": (-1, 3),
        "Daniel Faucitt": (1, -4),
        "Peter Faucitt": (-3, -4),
        "Adderory": (-2, 4),
    }
    
    # Entity type colors
    type_colors = {
        "Group": "#e74c3c",
        "Company": "#3498db",
        "Person": "#2ecc71",
        "Estate": "#9b59b6"
    }
    
    # Draw entities
    for entity in ENTITY_DATA:
        name = entity['entity_name']
        if name in entity_positions:
            x, y = entity_positions[name]
            entity_type = entity['entity_type']
            event_count = entity['event_count']
            
            # Size based on event count
            size = 500 + (event_count * 200)
            
            # Draw node
            color = type_colors.get(entity_type, '#95a5a6')
            ax.scatter(x, y, s=size, c=color, alpha=0.7, edgecolors='black', linewidths=2, zorder=3)
            
            # Add label
            ax.text(x, y, name.replace(' ', '\n'), ha='center', va='center', 
                   fontsize=8, fontweight='bold', zorder=4)
            
            # Add event count
            ax.text(x, y - 0.7, f"({event_count} events)", ha='center', va='top', 
                   fontsize=6, style='italic', zorder=4)
    
    # Draw transaction flows
    for tx in TRANSACTION_DATA[:8]:  # Top 8 transactions
        from_e = tx['from_entity']
        to_e = tx['to_entity']
        
        if from_e and to_e and from_e in entity_positions and to_e in entity_positions:
            x1, y1 = entity_positions[from_e]
            x2, y2 = entity_positions[to_e]
            
            # Determine arrow style based on transaction type
            tx_type = tx['transaction_type']
            if 'Fraud' in tx_type:
                color = '#e74c3c'
                style = 'dashed'
                width = 3
            elif 'Debt' in tx_type:
                color = '#f39c12'
                style = 'solid'
                width = 2
            else:
                color = '#95a5a6'
                style = 'solid'
                width = 1.5
            
            # Draw arrow
            arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                   arrowstyle='->', mutation_scale=20,
                                   color=color, linestyle=style, linewidth=width,
                                   alpha=0.6, zorder=1)
            ax.add_patch(arrow)
            
            # Add amount label
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            amount_m = tx['total_amount'] / 1000000
            ax.text(mid_x, mid_y, f"R{amount_m:.1f}M", 
                   fontsize=7, ha='center', va='bottom',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8),
                   zorder=2)
    
    # Formatting
    ax.set_xlim(-6, 7)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Entity Relationship Hypergraph\nNode Size = Event Involvement | Arrows = Transaction Flows', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Legend
    legend_elements = [
        mpatches.Patch(color='#e74c3c', label='Group Entity', alpha=0.7),
        mpatches.Patch(color='#3498db', label='Company Entity', alpha=0.7),
        mpatches.Patch(color='#2ecc71', label='Person Entity', alpha=0.7),
        plt.Line2D([0], [0], color='#e74c3c', linewidth=3, linestyle='dashed', label='Fraudulent Flow'),
        plt.Line2D([0], [0], color='#f39c12', linewidth=2, label='Debt Flow'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analysis/entity_network_hypergraph.png', dpi=300, bbox_inches='tight')
    print("✓ Entity network visualization saved")
    return fig

def create_transaction_flow_sankey():
    """Create transaction flow analysis visualization"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # Left plot: Transaction types by amount
    tx_types = {}
    for tx in TRANSACTION_DATA:
        tx_type = tx['transaction_type']
        amount = tx['total_amount']
        tx_types[tx_type] = tx_types.get(tx_type, 0) + amount
    
    sorted_types = sorted(tx_types.items(), key=lambda x: x[1], reverse=True)
    types = [t[0] for t in sorted_types]
    amounts = [t[1] / 1000000 for t in sorted_types]  # Convert to millions
    
    colors_tx = ['#e74c3c' if 'Fraud' in t else '#f39c12' if 'Debt' in t else '#3498db' for t in types]
    
    ax1.barh(types, amounts, color=colors_tx, alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Amount (R Millions)', fontsize=12, fontweight='bold')
    ax1.set_title('Transaction Types by Total Amount', fontsize=14, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (t, a) in enumerate(zip(types, amounts)):
        ax1.text(a, i, f' R{a:.1f}M', va='center', fontsize=9, fontweight='bold')
    
    # Right plot: Entity involvement by role
    entity_roles = {}
    for entity in ENTITY_DATA[:6]:  # Top 6 entities
        name = entity['entity_name']
        roles = entity['roles'].split(', ')
        entity_roles[name] = len(roles)
    
    sorted_entities = sorted(entity_roles.items(), key=lambda x: x[1], reverse=True)
    entities = [e[0] for e in sorted_entities]
    role_counts = [e[1] for e in sorted_entities]
    
    colors_ent = ['#e74c3c' if 'RegimA' in e else '#2ecc71' if 'ReZonance' in e else '#3498db' for e in entities]
    
    ax2.barh(entities, role_counts, color=colors_ent, alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Number of Different Roles', fontsize=12, fontweight='bold')
    ax2.set_title('Entity Role Complexity', fontsize=14, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (e, r) in enumerate(zip(entities, role_counts)):
        ax2.text(r, i, f' {r} roles', va='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analysis/transaction_flow_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Transaction flow analysis saved")
    return fig

def generate_hypergraph_metrics():
    """Generate hypergraph metrics and statistics"""
    metrics = {
        "timeline_metrics": {
            "total_events": len(TIMELINE_DATA),
            "critical_events": sum(1 for e in TIMELINE_DATA if e['is_critical']),
            "total_transaction_value": sum(e['total_amount'] for e in TIMELINE_DATA),
            "average_entities_per_event": sum(e['entity_count'] for e in TIMELINE_DATA) / len(TIMELINE_DATA),
            "phases": {
                "phase_1": len([e for e in TIMELINE_DATA if e['phase_number'] == 1]),
                "phase_2": len([e for e in TIMELINE_DATA if e['phase_number'] == 2]),
                "phase_3": len([e for e in TIMELINE_DATA if e['phase_number'] == 3]),
                "phase_4": len([e for e in TIMELINE_DATA if e['phase_number'] == 4]),
            }
        },
        "entity_metrics": {
            "total_entities": len(ENTITY_DATA),
            "most_involved": ENTITY_DATA[0]['entity_name'],
            "most_involved_count": ENTITY_DATA[0]['event_count'],
            "entity_types": {
                "companies": len([e for e in ENTITY_DATA if e['entity_type'] == 'Company']),
                "persons": len([e for e in ENTITY_DATA if e['entity_type'] == 'Person']),
                "groups": len([e for e in ENTITY_DATA if e['entity_type'] == 'Group']),
            }
        },
        "transaction_metrics": {
            "total_transactions": len(TRANSACTION_DATA),
            "total_value": sum(t['total_amount'] for t in TRANSACTION_DATA),
            "largest_transaction": max(TRANSACTION_DATA, key=lambda x: x['total_amount']),
            "fraud_total": sum(t['total_amount'] for t in TRANSACTION_DATA if 'Fraud' in t['transaction_type']),
            "debt_total": sum(t['total_amount'] for t in TRANSACTION_DATA if 'Debt' in t['transaction_type']),
        },
        "hypergraph_properties": {
            "average_hyperedge_size": sum(e['entity_count'] for e in TIMELINE_DATA) / len(TIMELINE_DATA),
            "max_hyperedge_size": max(e['entity_count'] for e in TIMELINE_DATA),
            "temporal_span_days": (datetime.strptime(TIMELINE_DATA[-1]['event_date'], '%Y-%m-%d') - 
                                  datetime.strptime(TIMELINE_DATA[0]['event_date'], '%Y-%m-%d')).days,
            "critical_event_ratio": sum(1 for e in TIMELINE_DATA if e['is_critical']) / len(TIMELINE_DATA),
        }
    }
    
    # Save metrics
    with open('/home/ubuntu/analysis/hypergraph_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print("✓ Hypergraph metrics generated")
    return metrics

def main():
    """Main execution"""
    print("\n" + "="*60)
    print("Timeline Hypergraph Analysis")
    print("="*60 + "\n")
    
    # Generate visualizations
    print("Generating visualizations...")
    create_timeline_visualization()
    create_entity_network_visualization()
    create_transaction_flow_sankey()
    
    # Generate metrics
    print("\nGenerating hypergraph metrics...")
    metrics = generate_hypergraph_metrics()
    
    print("\n" + "="*60)
    print("Hypergraph Analysis Summary")
    print("="*60)
    print(f"Total Events: {metrics['timeline_metrics']['total_events']}")
    print(f"Critical Events: {metrics['timeline_metrics']['critical_events']}")
    print(f"Total Transaction Value: R{metrics['transaction_metrics']['total_value']/1000000:.1f}M")
    print(f"Fraud Amount: R{metrics['transaction_metrics']['fraud_total']/1000000:.1f}M")
    print(f"Total Entities: {metrics['entity_metrics']['total_entities']}")
    print(f"Most Involved Entity: {metrics['entity_metrics']['most_involved']} ({metrics['entity_metrics']['most_involved_count']} events)")
    print(f"Temporal Span: {metrics['hypergraph_properties']['temporal_span_days']} days")
    print("="*60 + "\n")
    
    print("✅ Hypergraph analysis completed!\n")
    print("Generated files:")
    print("  - timeline_hypergraph_visualization.png")
    print("  - entity_network_hypergraph.png")
    print("  - transaction_flow_analysis.png")
    print("  - hypergraph_metrics.json\n")

if __name__ == "__main__":
    main()

