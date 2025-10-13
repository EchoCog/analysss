#!/usr/bin/env python3
"""
Critical Nodes and Edges Analysis
Identifies the most critical entities and relationships in the fraud hypergraph
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

# Entity data with event counts and roles
ENTITY_DATA = [
    {"entity_name": "RegimA Group", "entity_type": "Group", "event_count": 11, "roles": ["Client", "Control consolidator", "Debtor", "Evidence destroyer", "False claimant", "Payer", "Perpetrator", "Target"]},
    {"entity_name": "ReZonance", "entity_type": "Company", "event_count": 9, "roles": ["Creditor", "Payee", "Service provider", "Victim"]},
    {"entity_name": "RegimA Skin Treatments", "entity_type": "Company", "event_count": 4, "roles": ["Client", "Cost recipient", "Financial year start", "Interest receiver"]},
    {"entity_name": "Rynette Farrar", "entity_type": "Person", "event_count": 3, "roles": ["Beneficiary", "CC recipient", "Confronted party"]},
    {"entity_name": "Daniel Faucitt", "entity_type": "Person", "event_count": 3, "roles": ["Beneficiary", "CC recipient", "CIO (RWW)"]},
    {"entity_name": "Strategic Logistics", "entity_type": "Company", "event_count": 3, "roles": ["Cost reallocation", "Financial year start", "Interest payer"]},
    {"entity_name": "Villa Via", "entity_type": "Company", "event_count": 2, "roles": ["Financial year start", "Rental income vehicle"]},
    {"entity_name": "Jacqui Faucitt", "entity_type": "Person", "event_count": 2, "roles": ["CC recipient", "Fraud detector (RST CEO)"]},
    {"entity_name": "RegimA Worldwide", "entity_type": "Company", "event_count": 2, "roles": ["Cost dumping ground", "Loan recipient"]},
    {"entity_name": "Peter Faucitt", "entity_type": "Person", "event_count": 1, "roles": ["Beneficiary"]},
    {"entity_name": "RegimA UK", "entity_type": "Company", "event_count": 1, "roles": ["Extraction vehicle"]},
    {"entity_name": "Adderory", "entity_type": "Person", "event_count": 1, "roles": ["Domain purchaser (Rynette's son)"]},
]

# Transaction data
TRANSACTION_DATA = [
    {"from_entity": "Villa Via", "to_entity": None, "transaction_type": "Capital Extraction", "total_amount": 22800000.00, "criticality": "CRITICAL"},
    {"from_entity": "RegimA SA", "to_entity": "RegimA UK", "transaction_type": "International Transfer", "total_amount": 11900000.00, "criticality": "CRITICAL"},
    {"from_entity": None, "to_entity": "Villa Via", "transaction_type": "Revenue", "total_amount": 4400000.00, "criticality": "HIGH"},
    {"from_entity": None, "to_entity": "Villa Via", "transaction_type": "Profit", "total_amount": 3700000.00, "criticality": "HIGH"},
    {"from_entity": "RegimA Group", "to_entity": "ReZonance", "transaction_type": "Debt", "total_amount": 2006949.27, "criticality": "CRITICAL"},
    {"from_entity": "RegimA Group", "to_entity": "ReZonance", "transaction_type": "Fraud", "total_amount": 1235361.34, "criticality": "CRITICAL"},
    {"from_entity": "RegimA Group", "to_entity": "ReZonance", "transaction_type": "Fraudulent Claim", "total_amount": 1235361.34, "criticality": "CRITICAL"},
    {"from_entity": "RWW", "to_entity": None, "transaction_type": "Reallocation", "total_amount": 810000.00, "criticality": "HIGH"},
    {"from_entity": "RST", "to_entity": None, "transaction_type": "Adjustment", "total_amount": 784000.00, "criticality": "MEDIUM"},
    {"from_entity": "RST", "to_entity": "RWW", "transaction_type": "Loan", "total_amount": 750000.00, "criticality": "HIGH"},
    {"from_entity": "SLG", "to_entity": "RST", "transaction_type": "Interest", "total_amount": 414334.09, "criticality": "CRITICAL"},
]

# Critical events
CRITICAL_EVENTS = [
    {"date": "2020-02-20", "title": "Multiple adjusting journal entries", "impact": "HIGH", "phase": 1},
    {"date": "2020-02-28", "title": "Inter-company interest payment", "impact": "CRITICAL", "phase": 1},
    {"date": "2020-04-30", "title": "Villa Via year-end (R22.8M extraction)", "impact": "CRITICAL", "phase": 1},
    {"date": "2022-03-01", "title": "R971K accumulated debt", "impact": "HIGH", "phase": 3},
    {"date": "2023-02-28", "title": "Debt grows to R1.03M", "impact": "CRITICAL", "phase": 3},
    {"date": "2023-03-15", "title": "First false payment claim (R470K)", "impact": "CRITICAL", "phase": 3},
    {"date": "2023-09-20", "title": "Additional false claims (R765K)", "impact": "CRITICAL", "phase": 3},
    {"date": "2025-04-15", "title": "Bank accounts redirected", "impact": "CRITICAL", "phase": 4},
    {"date": "2025-05-15", "title": "Jax confronts Rynette", "impact": "CRITICAL", "phase": 4},
    {"date": "2025-05-22", "title": "Shopify evidence destroyed", "impact": "CRITICAL", "phase": 4},
    {"date": "2025-05-29", "title": "Domain hijacked", "impact": "CRITICAL", "phase": 4},
    {"date": "2025-06-07", "title": "Cards cancelled", "impact": "CRITICAL", "phase": 4},
    {"date": "2025-10-09", "title": "Full fraud discovered (R1.23M)", "impact": "CRITICAL", "phase": 4},
    {"date": "2025-10-12", "title": "UK extraction revealed (R11.9M)", "impact": "CRITICAL", "phase": 4},
]

def calculate_node_centrality():
    """Calculate centrality metrics for each node"""
    nodes = []
    
    for entity in ENTITY_DATA:
        # Calculate metrics
        event_centrality = entity['event_count']
        role_diversity = len(entity['roles'])
        
        # Determine criticality based on roles
        critical_roles = ['Perpetrator', 'Evidence destroyer', 'False claimant', 'Victim', 'Fraud detector (RST CEO)', 'Extraction vehicle']
        has_critical_role = any(role in critical_roles for role in entity['roles'])
        
        # Calculate overall criticality score
        criticality_score = (event_centrality * 2) + (role_diversity * 3)
        if has_critical_role:
            criticality_score *= 1.5
        
        nodes.append({
            'name': entity['entity_name'],
            'type': entity['entity_type'],
            'event_centrality': event_centrality,
            'role_diversity': role_diversity,
            'roles': entity['roles'],
            'has_critical_role': has_critical_role,
            'criticality_score': criticality_score
        })
    
    # Sort by criticality score
    nodes.sort(key=lambda x: x['criticality_score'], reverse=True)
    
    return nodes

def calculate_edge_criticality():
    """Calculate criticality for each edge (transaction)"""
    edges = []
    
    for tx in TRANSACTION_DATA:
        # Financial impact (normalized to millions)
        financial_impact = tx['total_amount'] / 1000000
        
        # Type criticality
        type_weights = {
            'Fraud': 10,
            'Fraudulent Claim': 10,
            'Capital Extraction': 8,
            'International Transfer': 8,
            'Debt': 7,
            'Interest': 6,
            'Reallocation': 5,
            'Loan': 4,
            'Adjustment': 3,
            'Revenue': 2,
            'Profit': 2
        }
        
        type_score = type_weights.get(tx['transaction_type'], 1)
        
        # Calculate overall edge criticality
        edge_criticality = (financial_impact * 0.3) + (type_score * 0.7)
        
        edges.append({
            'from': tx['from_entity'],
            'to': tx['to_entity'],
            'type': tx['transaction_type'],
            'amount': tx['total_amount'],
            'financial_impact': financial_impact,
            'type_score': type_score,
            'edge_criticality': edge_criticality,
            'criticality_level': tx.get('criticality', 'MEDIUM')
        })
    
    # Sort by edge criticality
    edges.sort(key=lambda x: x['edge_criticality'], reverse=True)
    
    return edges

def create_critical_nodes_visualization(nodes):
    """Create visualization of critical nodes"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # Left plot: Node criticality scores
    top_nodes = nodes[:8]
    names = [n['name'] for n in top_nodes]
    scores = [n['criticality_score'] for n in top_nodes]
    
    colors = []
    for node in top_nodes:
        if node['has_critical_role']:
            colors.append('#e74c3c')
        elif node['type'] == 'Group':
            colors.append('#e67e22')
        elif node['type'] == 'Person':
            colors.append('#3498db')
        else:
            colors.append('#2ecc71')
    
    bars = ax1.barh(names, scores, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    ax1.set_xlabel('Criticality Score', fontsize=14, fontweight='bold')
    ax1.set_title('Top 8 Critical Nodes by Centrality', fontsize=16, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (name, score) in enumerate(zip(names, scores)):
        ax1.text(score, i, f' {score:.1f}', va='center', fontsize=10, fontweight='bold')
    
    # Right plot: Role diversity vs event centrality
    all_names = [n['name'][:20] for n in nodes[:10]]
    event_counts = [n['event_centrality'] for n in nodes[:10]]
    role_counts = [n['role_diversity'] for n in nodes[:10]]
    critical_flags = [n['has_critical_role'] for n in nodes[:10]]
    
    colors2 = ['#e74c3c' if c else '#3498db' for c in critical_flags]
    sizes = [100 + (e * 100) for e in event_counts]
    
    scatter = ax2.scatter(role_counts, event_counts, s=sizes, c=colors2, alpha=0.6, edgecolors='black', linewidths=2)
    
    # Add labels
    for i, name in enumerate(all_names):
        ax2.annotate(name, (role_counts[i], event_counts[i]), 
                    fontsize=8, ha='center', va='bottom')
    
    ax2.set_xlabel('Role Diversity (Number of Different Roles)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Event Centrality (Number of Events)', fontsize=14, fontweight='bold')
    ax2.set_title('Node Centrality Analysis\nBubble Size = Event Count', fontsize=16, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#e74c3c', 
                   markersize=12, label='Has Critical Role', markeredgecolor='black', markeredgewidth=2),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#3498db', 
                   markersize=12, label='Standard Role', markeredgecolor='black', markeredgewidth=2),
    ]
    ax2.legend(handles=legend_elements, loc='upper left', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analysis/critical_nodes_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Critical nodes visualization saved")
    return fig

def create_critical_edges_visualization(edges):
    """Create visualization of critical edges"""
    fig, ax = plt.subplots(figsize=(18, 12))
    
    # Prepare data
    top_edges = edges[:10]
    labels = []
    for edge in top_edges:
        from_e = edge['from'] if edge['from'] else 'External'
        to_e = edge['to'] if edge['to'] else 'External'
        labels.append(f"{from_e[:15]} → {to_e[:15]}\n({edge['type']})")
    
    criticality_scores = [e['edge_criticality'] for e in top_edges]
    amounts = [e['amount'] / 1000000 for e in top_edges]
    
    # Color by criticality level
    color_map = {
        'CRITICAL': '#e74c3c',
        'HIGH': '#f39c12',
        'MEDIUM': '#3498db',
        'LOW': '#95a5a6'
    }
    colors = [color_map.get(e['criticality_level'], '#95a5a6') for e in top_edges]
    
    # Create horizontal bar chart
    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, criticality_scores, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel('Edge Criticality Score', fontsize=14, fontweight='bold')
    ax.set_title('Top 10 Critical Edges (Transactions/Relationships)\nScore = Financial Impact + Type Severity', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    
    # Add amount labels
    for i, (score, amount) in enumerate(zip(criticality_scores, amounts)):
        ax.text(score, i, f' {score:.1f} (R{amount:.1f}M)', 
               va='center', fontsize=9, fontweight='bold')
    
    # Legend
    legend_elements = [
        mpatches.Patch(color='#e74c3c', label='CRITICAL', alpha=0.7),
        mpatches.Patch(color='#f39c12', label='HIGH', alpha=0.7),
        mpatches.Patch(color='#3498db', label='MEDIUM', alpha=0.7),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analysis/critical_edges_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Critical edges visualization saved")
    return fig

def create_critical_path_visualization():
    """Create critical path through the fraud scheme"""
    fig, ax = plt.subplots(figsize=(20, 14))
    
    # Group events by phase
    phase_events = {1: [], 2: [], 3: [], 4: []}
    for event in CRITICAL_EVENTS:
        phase_events[event['phase']].append(event)
    
    # Y positions for phases
    phase_y = {1: 3, 2: 2, 3: 1, 4: 0}
    phase_colors = {1: '#3498db', 2: '#2ecc71', 3: '#f39c12', 4: '#e74c3c'}
    phase_names = {
        1: 'Phase 1: Financial Structure',
        2: 'Phase 2: Business Development',
        3: 'Phase 3: Debt & Manipulation',
        4: 'Phase 4: Fraud & Cover-up'
    }
    
    # Draw phase backgrounds
    for phase, y in phase_y.items():
        ax.axhspan(y - 0.35, y + 0.35, alpha=0.1, color=phase_colors[phase])
        ax.text(-0.5, y, phase_names[phase], fontsize=11, fontweight='bold', 
               va='center', ha='right', bbox=dict(boxstyle='round,pad=0.5', 
               facecolor=phase_colors[phase], alpha=0.3))
    
    # Plot events
    all_events_sorted = sorted(CRITICAL_EVENTS, key=lambda x: x['date'])
    
    for i, event in enumerate(all_events_sorted):
        phase = event['phase']
        y = phase_y[phase]
        x = i
        
        # Determine size and style based on impact
        if event['impact'] == 'CRITICAL':
            size = 800
            edge_width = 4
            edge_color = '#e74c3c'
        else:
            size = 400
            edge_width = 2
            edge_color = 'black'
        
        # Draw event node
        ax.scatter(x, y, s=size, c=phase_colors[phase], alpha=0.7, 
                  edgecolors=edge_color, linewidths=edge_width, zorder=3)
        
        # Add label
        ax.text(x, y + 0.5, event['date'], ha='center', va='bottom', 
               fontsize=7, fontweight='bold', rotation=45)
        ax.text(x, y - 0.5, event['title'][:30], ha='center', va='top', 
               fontsize=6, style='italic')
        
        # Draw connecting line to next event
        if i < len(all_events_sorted) - 1:
            next_event = all_events_sorted[i + 1]
            next_y = phase_y[next_event['phase']]
            ax.plot([x, i + 1], [y, next_y], 'k-', alpha=0.3, linewidth=1, zorder=1)
    
    # Highlight critical sequence in Phase 4 (May-June 2025)
    may_june_events = [e for e in all_events_sorted if '2025-05' in e['date'] or '2025-06' in e['date']]
    if len(may_june_events) >= 2:
        start_idx = all_events_sorted.index(may_june_events[0])
        end_idx = all_events_sorted.index(may_june_events[-1])
        ax.axvspan(start_idx - 0.5, end_idx + 0.5, alpha=0.15, color='red', zorder=0)
        ax.text((start_idx + end_idx) / 2, -0.8, 'CRITICAL COVER-UP SEQUENCE\n(7-23 days after confrontation)', 
               ha='center', va='top', fontsize=12, fontweight='bold', color='red',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))
    
    # Formatting
    ax.set_ylim(-1, 3.5)
    ax.set_xlim(-1, len(all_events_sorted))
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(['Phase 4', 'Phase 3', 'Phase 2', 'Phase 1'])
    ax.set_xlabel('Critical Event Sequence', fontsize=14, fontweight='bold')
    ax.set_title('Critical Path Through Fraud Scheme\nRed Border = CRITICAL Impact | Yellow Box = Cover-up Cluster', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.2)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analysis/critical_path_visualization.png', dpi=300, bbox_inches='tight')
    print("✓ Critical path visualization saved")
    return fig

def generate_critical_analysis_report(nodes, edges):
    """Generate detailed critical analysis report"""
    
    report = {
        "critical_nodes": {
            "top_5": [
                {
                    "rank": i + 1,
                    "name": node['name'],
                    "type": node['type'],
                    "criticality_score": round(node['criticality_score'], 2),
                    "event_centrality": node['event_centrality'],
                    "role_diversity": node['role_diversity'],
                    "roles": node['roles'],
                    "has_critical_role": node['has_critical_role'],
                    "analysis": get_node_analysis(node)
                }
                for i, node in enumerate(nodes[:5])
            ]
        },
        "critical_edges": {
            "top_5": [
                {
                    "rank": i + 1,
                    "from": edge['from'],
                    "to": edge['to'],
                    "type": edge['type'],
                    "amount": edge['amount'],
                    "criticality_score": round(edge['edge_criticality'], 2),
                    "criticality_level": edge['criticality_level'],
                    "analysis": get_edge_analysis(edge)
                }
                for i, edge in enumerate(edges[:5])
            ]
        },
        "critical_events": {
            "total": len(CRITICAL_EVENTS),
            "by_phase": {
                "phase_1": len([e for e in CRITICAL_EVENTS if e['phase'] == 1]),
                "phase_2": len([e for e in CRITICAL_EVENTS if e['phase'] == 2]),
                "phase_3": len([e for e in CRITICAL_EVENTS if e['phase'] == 3]),
                "phase_4": len([e for e in CRITICAL_EVENTS if e['phase'] == 4]),
            },
            "cover_up_sequence": [
                e for e in CRITICAL_EVENTS 
                if '2025-05' in e['date'] or '2025-06' in e['date']
            ]
        },
        "summary": {
            "total_nodes_analyzed": len(nodes),
            "total_edges_analyzed": len(edges),
            "critical_nodes_count": len([n for n in nodes if n['has_critical_role']]),
            "critical_edges_count": len([e for e in edges if e['criticality_level'] == 'CRITICAL']),
        }
    }
    
    with open('/home/ubuntu/analysis/critical_analysis_metrics.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("✓ Critical analysis report generated")
    return report

def get_node_analysis(node):
    """Get analysis text for a node"""
    analyses = {
        "RegimA Group": "Central hub of the fraud scheme. Involved in 11 events across all phases, playing 8 different roles from legitimate client to perpetrator and evidence destroyer. This entity represents the collective fraudulent activities.",
        "ReZonance": "Primary victim of the fraud scheme. Involved in 9 events, accumulating R2M in debt and R1.2M in fraudulent claims. Transitioned from service provider to creditor to victim.",
        "RegimA Skin Treatments": "Profit concentration entity. Receives interest payments from SLG while advancing loans to RWW. Controlled by co-director who also owns 50% of Villa Via, enabling self-dealing.",
        "Rynette Farrar": "Key individual confronted by Jax on May 15, 2025. This confrontation triggered the cover-up sequence. Beneficiary of the fraud scheme with family involvement (son Adderory).",
        "Daniel Faucitt": "CIO of RWW and beneficiary. Involved in damage control attempts and UK extraction pattern (R11.9M). Co-director with financial control.",
        "Strategic Logistics": "Loss-making entity with R5.4M manufactured loss. Pays R414K interest to RST while being used for transfer pricing manipulation. Classic expense dumping ground.",
        "Villa Via": "Capital extraction vehicle. Generated R3.7M profit from R4.4M rental income with R22.8M members loan extraction. Strategically excluded from 'Group' framing to hide profit extraction.",
        "Jacqui Faucitt": "FRAUD DETECTOR, not perpetrator. CEO of RST who confronted Rynette on May 15, 2025 about missing money owed to ReZonance and Kayla's estate. This confrontation triggered the cover-up.",
        "RegimA Worldwide": "Expense dumping ground. Forced to pay group expenses then blamed for excessive spending. Receives R750K loan from RST while bearing R810K in reallocated admin fees.",
    }
    return analyses.get(node['name'], "Entity involved in multiple events with varying roles.")

def get_edge_analysis(edge):
    """Get analysis text for an edge"""
    edge_key = f"{edge['type']}"
    analyses = {
        "Fraud": "Direct fraudulent transaction representing the discovered payment fraud scheme totaling R1.23M against ReZonance.",
        "Fraudulent Claim": "False payment claims made by RegimA Group that were never actually paid to ReZonance, escalating from R470K to R765K.",
        "Capital Extraction": "Massive R22.8M extraction from Villa Via through members loan, representing systematic wealth transfer from the entity.",
        "International Transfer": "R11.9M transferred from RegimA SA to RegimA UK, revealing international dimension of financial extraction.",
        "Debt": "Accumulated debt of R2M owed to ReZonance, representing systematic non-payment of legitimate services over extended period.",
        "Interest": "R414K interest payment from SLG to RST, demonstrating profit concentration in entity controlled by co-director.",
        "Reallocation": "R810K admin fee reallocated from RWW to production costs, part of expense dumping strategy.",
        "Loan": "R750K loan from RST to RWW for production costs, creating debt dependency while RST receives interest from SLG.",
    }
    return analyses.get(edge_key, "Financial transaction within the fraud scheme.")

def main():
    """Main execution"""
    print("\n" + "="*60)
    print("Critical Nodes and Edges Analysis")
    print("="*60 + "\n")
    
    # Calculate metrics
    print("Calculating node centrality metrics...")
    nodes = calculate_node_centrality()
    
    print("Calculating edge criticality metrics...")
    edges = calculate_edge_criticality()
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    create_critical_nodes_visualization(nodes)
    create_critical_edges_visualization(edges)
    create_critical_path_visualization()
    
    # Generate report
    print("\nGenerating critical analysis report...")
    report = generate_critical_analysis_report(nodes, edges)
    
    print("\n" + "="*60)
    print("Critical Analysis Summary")
    print("="*60)
    print(f"Top Critical Node: {nodes[0]['name']} (score: {nodes[0]['criticality_score']:.1f})")
    print(f"Top Critical Edge: {edges[0]['type']} (score: {edges[0]['edge_criticality']:.1f}, R{edges[0]['amount']/1000000:.1f}M)")
    print(f"Total Critical Events: {len(CRITICAL_EVENTS)}")
    print(f"Cover-up Sequence Events: {len(report['critical_events']['cover_up_sequence'])}")
    print("="*60 + "\n")
    
    print("✅ Critical analysis completed!\n")
    print("Generated files:")
    print("  - critical_nodes_analysis.png")
    print("  - critical_edges_analysis.png")
    print("  - critical_path_visualization.png")
    print("  - critical_analysis_metrics.json\n")

if __name__ == "__main__":
    main()

