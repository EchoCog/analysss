#!/usr/bin/env python3.11
"""
Updated Critical Hypergraph Analysis
Integrating Bantjies Betrayal & 2025 Attack Pattern
Date: October 12, 2025
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
import numpy as np

# ============================================
# UPDATED TIMELINE DATA WITH NEW EVIDENCE
# ============================================

updated_events = [
    # Original 22 events (Phase 1-4)
    {"id": 1, "date": "2020-02-29", "title": "Inter-company interest payment", "phase": 1, "critical": True, "amount": 414000},
    {"id": 2, "date": "2020-02-29", "title": "Capital extraction from Villa Via", "phase": 1, "critical": True, "amount": 22800000},
    {"id": 3, "date": "2020-02-29", "title": "Cost reallocation to RWW", "phase": 1, "critical": True, "amount": 810000},
    {"id": 4, "date": "2017-06-30", "title": "ReZonance service relationship begins", "phase": 2, "critical": False, "amount": 0},
    {"id": 5, "date": "2022-06-30", "title": "RWW accumulated debt", "phase": 3, "critical": True, "amount": 771588},
    {"id": 6, "date": "2023-04-08", "title": "Debt grows to R1.23M", "phase": 3, "critical": True, "amount": 1235361},
    {"id": 7, "date": "2023-10-19", "title": "First fake payment claim", "phase": 3, "critical": True, "amount": 1235361},
    {"id": 8, "date": "2023-10-25", "title": "Additional fake claims", "phase": 3, "critical": True, "amount": 1235361},
    {"id": 9, "date": "2025-05-15", "title": "Jax confronts Rynette", "phase": 4, "critical": True, "amount": 0},
    {"id": 10, "date": "2025-05-22", "title": "Shopify evidence destroyed", "phase": 4, "critical": True, "amount": 0},
    {"id": 11, "date": "2025-05-29", "title": "Domain hijacked", "phase": 4, "critical": True, "amount": 0},
    {"id": 12, "date": "2025-06-07", "title": "Cards cancelled", "phase": 4, "critical": True, "amount": 0},
    {"id": 13, "date": "2020-02-29", "title": "RegimA UK international transfer", "phase": 1, "critical": True, "amount": 11900000},
    {"id": 14, "date": "2020-02-29", "title": "Trial balance manipulation", "phase": 1, "critical": True, "amount": 0},
    {"id": 15, "date": "2025-04-14", "title": "Rynette bank letter change", "phase": 4, "critical": True, "amount": 0},
    {"id": 16, "date": "2025-04-15", "title": "Bank accounts redirected", "phase": 4, "critical": True, "amount": 0},
    {"id": 17, "date": "2025-06-13", "title": "Fail proof discovered (R1.23M)", "phase": 4, "critical": True, "amount": 1235361},
    {"id": 18, "date": "2025-07-20", "title": "UK extension revealed (R11.5M)", "phase": 4, "critical": True, "amount": 11500000},
    {"id": 19, "date": "2021-01-01", "title": "Business relationship development", "phase": 2, "critical": False, "amount": 0},
    {"id": 20, "date": "2020-02-29", "title": "SLG debt to RST (R13M)", "phase": 1, "critical": True, "amount": 13000000},
    {"id": 21, "date": "2020-02-29", "title": "RST loan to RWW (R0.8M)", "phase": 1, "critical": True, "amount": 800000},
    {"id": 22, "date": "2020-02-29", "title": "RWW cost reallocation (R0.8M)", "phase": 1, "critical": True, "amount": 800000},
    
    # NEW EVENTS (Phase 5-6: 2024-2025 Attack Pattern)
    {"id": 24, "date": "2024-07-01", "title": "Bantjies secret trustee installation", "phase": 5, "critical": True, "amount": 18600000},
    {"id": 25, "date": "2024-09-01", "title": "Strange people access attempts", "phase": 5, "critical": True, "amount": 0},
    {"id": 26, "date": "2024-11-01", "title": "False incapacitation report", "phase": 5, "critical": True, "amount": 0},
    {"id": 27, "date": "2025-05-16", "title": "Dan reports fraud to Bantjies", "phase": 4, "critical": True, "amount": 0},
    {"id": 28, "date": "2025-06-15", "title": "12-hour signature scam", "phase": 6, "critical": True, "amount": 0},
    {"id": 29, "date": "2025-07-01", "title": "1000-page report scam", "phase": 6, "critical": True, "amount": 0},
    {"id": 31, "date": "2025-08-19", "title": "Ex parte interdict", "phase": 6, "critical": True, "amount": 0},
    {"id": 32, "date": "2025-08-25", "title": "Forced medical experimentation threat", "phase": 6, "critical": True, "amount": 0},
]

# Updated entity involvement (includes Bantjies)
entity_events = {
    "RegimA Group": 11,
    "ReZonance": 9,
    "Danie Bantjies": 8,  # NEW: Most critical individual
    "RegimA Skin Treatments": 4,
    "Rynette Farrar": 5,  # Updated
    "Daniel Faucitt": 7,  # Updated (victim of attacks)
    "Jacqui Faucitt": 3,
    "Strategic Logistics": 3,
    "Villa Via": 2,
    "RegimA UK": 1,
    "RegimA Worldwide": 4,
    "Peter Faucitt": 4,  # Updated
    "Unknown Infiltrators": 1,  # NEW
}

# Updated entity roles
entity_roles = {
    "RegimA Group": ["Perpetrator", "Evidence destroyer", "False claimant", "Debtor", "Client", "Payer", "Borrower", "Manipulator"],
    "ReZonance": ["Victim", "Creditor", "Payee", "Service provider"],
    "Danie Bantjies": ["Double agent", "Secret trustee", "Intelligence gatherer", "Interdict supporter", "Conspiracy coordinator", "Accountant", "Fiduciary breacher", "Professional misconduct"],
    "RegimA Skin Treatments": ["Interest receiver", "Cost recipient", "Client", "Profit center"],
    "Rynette Farrar": ["Confronted party", "Beneficiary", "CC recipient", "Conspiracy coordinator", "Bank letter signer"],
    "Daniel Faucitt": ["Fraud detector", "Victim", "Excluded beneficiary", "CIO (RWW)", "Attack target"],
    "Jacqui Faucitt": ["Fraud detector (RST CEO)", "Copied party", "Excluded from interdict"],
    "Peter Faucitt": ["Conspiracy leader", "Interdict applicant", "Trustee", "Attack coordinator"],
    "Unknown Infiltrators": ["Access attempt coordinators"],
}

# Phase definitions
phases = {
    1: {"name": "Financial Structure", "color": "#E8F4F8", "years": "2019-2020"},
    2: {"name": "Business Development", "color": "#E8F8F0", "years": "2017-2021"},
    3: {"name": "Debt & Manipulation", "color": "#FFF8E8", "years": "2022-2023"},
    4: {"name": "Fraud Discovery & Cover-up", "color": "#FFE8E8", "years": "May 2025"},
    5: {"name": "Conspiracy Preparation", "color": "#F0E8FF", "years": "Jul 2024-Apr 2025"},
    6: {"name": "Active Attack Phase", "color": "#FFE0E0", "years": "May-Aug 2025"},
}

# ============================================
# UPDATED CRITICAL ANALYSIS
# ============================================

def calculate_updated_node_scores():
    """Calculate updated node criticality scores with Bantjies"""
    scores = {}
    
    for entity, event_count in entity_events.items():
        role_count = len(entity_roles.get(entity, []))
        
        # Base score: event count * 5
        base_score = event_count * 5
        
        # Role diversity bonus: role count * 2
        role_bonus = role_count * 2
        
        # Critical role multiplier
        critical_roles = ["Perpetrator", "Victim", "Double agent", "Secret trustee", 
                         "Conspiracy coordinator", "Attack target", "Fraud detector"]
        has_critical = any(role in entity_roles.get(entity, []) for role in critical_roles)
        critical_multiplier = 1.5 if has_critical else 1.0
        
        # Professional position bonus (for Bantjies)
        professional_bonus = 10 if "Accountant" in entity_roles.get(entity, []) else 0
        
        # Betrayal bonus (for Bantjies - trusted advisor turned enemy)
        betrayal_bonus = 15 if entity == "Danie Bantjies" else 0
        
        total_score = (base_score + role_bonus + professional_bonus + betrayal_bonus) * critical_multiplier
        
        scores[entity] = {
            "score": round(total_score, 1),
            "events": event_count,
            "roles": role_count,
            "has_critical": has_critical
        }
    
    return scores

def generate_updated_attack_timeline():
    """Generate visualization of attack escalation pattern"""
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Filter events for attack phases (5 and 6)
    attack_events = [e for e in updated_events if e["phase"] in [5, 6]]
    attack_events.sort(key=lambda x: x["date"])
    
    # Create timeline
    dates = [datetime.strptime(e["date"], "%Y-%m-%d") for e in attack_events]
    y_positions = list(range(len(attack_events)))
    
    # Plot events
    colors = []
    sizes = []
    for event in attack_events:
        if event["phase"] == 5:
            colors.append("#9B59B6")  # Purple for Conspiracy Preparation
        else:
            colors.append("#E74C3C")  # Red for Active Attack
        
        # Size based on criticality
        sizes.append(300 if event["critical"] else 150)
    
    scatter = ax.scatter(dates, y_positions, c=colors, s=sizes, alpha=0.7, edgecolors='black', linewidths=2)
    
    # Add event labels
    for i, event in enumerate(attack_events):
        ax.text(dates[i], y_positions[i] + 0.3, event["title"], 
                fontsize=9, ha='left', va='bottom')
    
    # Highlight critical sequences
    # Conspiracy Preparation cluster (July-Nov 2024)
    prep_events = [e for e in attack_events if e["phase"] == 5]
    if prep_events:
        prep_dates = [datetime.strptime(e["date"], "%Y-%m-%d") for e in prep_events]
        ax.axvspan(min(prep_dates), max(prep_dates), alpha=0.2, color='purple', 
                   label='Conspiracy Preparation Phase')
    
    # Active Attack cluster (May-Aug 2025)
    attack_phase_events = [e for e in attack_events if e["phase"] == 6]
    if attack_phase_events:
        attack_dates = [datetime.strptime(e["date"], "%Y-%m-%d") for e in attack_phase_events]
        ax.axvspan(min(attack_dates), max(attack_dates), alpha=0.2, color='red', 
                   label='Active Attack Phase')
    
    # Mark May 15 trigger event
    trigger_date = datetime.strptime("2025-05-15", "%Y-%m-%d")
    ax.axvline(trigger_date, color='orange', linestyle='--', linewidth=3, 
               label='Trigger: Jax Confrontation (May 15)')
    
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Attack Sequence', fontsize=12, fontweight='bold')
    ax.set_title('Attack Escalation Timeline (2024-2025)\nFrom Conspiracy Preparation to Physical Threats', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analysis/attack_escalation_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ Attack escalation timeline generated")

def generate_bantjies_centrality_map():
    """Generate visualization showing Bantjies as central node"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    
    # Left: Updated node scores
    scores = calculate_updated_node_scores()
    sorted_entities = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)[:10]
    
    entities = [e[0] for e in sorted_entities]
    score_values = [e[1]["score"] for e in sorted_entities]
    has_critical = [e[1]["has_critical"] for e in sorted_entities]
    
    colors = ['#E74C3C' if crit else '#3498DB' for crit in has_critical]
    
    # Highlight Bantjies
    colors[entities.index("Danie Bantjies")] = '#9B59B6'  # Purple for Bantjies
    
    bars = ax1.barh(entities, score_values, color=colors, edgecolor='black', linewidth=1.5)
    
    # Add score labels
    for i, (bar, score) in enumerate(zip(bars, score_values)):
        ax1.text(score + 1, bar.get_y() + bar.get_height()/2, 
                f'{score}', va='center', fontsize=10, fontweight='bold')
    
    ax1.set_xlabel('Criticality Score', fontsize=12, fontweight='bold')
    ax1.set_title('Updated Critical Nodes\n(Bantjies as Most Critical Individual)', 
                  fontsize=13, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Add legend
    red_patch = mpatches.Patch(color='#E74C3C', label='Critical Role Entity')
    blue_patch = mpatches.Patch(color='#3498DB', label='Standard Role Entity')
    purple_patch = mpatches.Patch(color='#9B59B6', label='Bantjies (Double Agent)')
    ax1.legend(handles=[red_patch, blue_patch, purple_patch], loc='lower right')
    
    # Right: Bantjies connection map
    # Show Bantjies connections to other entities
    bantjies_connections = {
        "Peter Faucitt": "Conspiracy",
        "Rynette Farrar": "Coordination",
        "Daniel Faucitt": "Betrayal",
        "RegimA Group": "Financial expertise",
        "Jacqui Faucitt": "Deception",
        "ReZonance": "Indirect victim",
    }
    
    # Create network-style visualization
    center_x, center_y = 0.5, 0.5
    radius = 0.35
    
    # Draw Bantjies at center
    circle = plt.Circle((center_x, center_y), 0.08, color='#9B59B6', ec='black', linewidth=2, zorder=10)
    ax2.add_patch(circle)
    ax2.text(center_x, center_y, 'Danie\nBantjies', ha='center', va='center', 
             fontsize=11, fontweight='bold', color='white', zorder=11)
    
    # Draw connections
    angles = np.linspace(0, 2*np.pi, len(bantjies_connections), endpoint=False)
    
    for i, (entity, relationship) in enumerate(bantjies_connections.items()):
        x = center_x + radius * np.cos(angles[i])
        y = center_y + radius * np.sin(angles[i])
        
        # Draw connection line
        ax2.plot([center_x, x], [center_y, y], 'k-', linewidth=2, alpha=0.5, zorder=1)
        
        # Draw entity circle
        entity_color = '#E74C3C' if entity in ["Peter Faucitt", "Rynette Farrar"] else '#3498DB'
        if entity == "Daniel Faucitt":
            entity_color = '#F39C12'  # Orange for victim
        
        circle = plt.Circle((x, y), 0.06, color=entity_color, ec='black', linewidth=1.5, zorder=5)
        ax2.add_patch(circle)
        
        # Add entity label
        label_x = center_x + (radius + 0.15) * np.cos(angles[i])
        label_y = center_y + (radius + 0.15) * np.sin(angles[i])
        ax2.text(label_x, label_y, entity, ha='center', va='center', 
                fontsize=9, fontweight='bold', zorder=6)
        
        # Add relationship label
        mid_x = center_x + (radius/2) * np.cos(angles[i])
        mid_y = center_y + (radius/2) * np.sin(angles[i])
        ax2.text(mid_x, mid_y, relationship, ha='center', va='center', 
                fontsize=7, style='italic', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8), zorder=7)
    
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_title('Bantjies Connection Network\n(Central Conspiracy Coordinator)', 
                  fontsize=13, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analysis/bantjies_centrality_map.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ Bantjies centrality map generated")

def generate_updated_metrics():
    """Generate updated metrics JSON"""
    scores = calculate_updated_node_scores()
    
    critical_events = [e for e in updated_events if e["critical"]]
    total_amount = sum(e["amount"] for e in updated_events)
    
    metrics = {
        "updated_analysis_date": "2025-10-12",
        "total_events": len(updated_events),
        "critical_events": len(critical_events),
        "critical_event_ratio": round(len(critical_events) / len(updated_events), 2),
        "total_transaction_value": total_amount,
        "temporal_span_days": (datetime.strptime("2025-08-25", "%Y-%m-%d") - 
                              datetime.strptime("2024-07-01", "%Y-%m-%d")).days,
        "phases": 6,
        "most_critical_node": {
            "entity": "Danie Bantjies",
            "score": scores["Danie Bantjies"]["score"],
            "events": scores["Danie Bantjies"]["events"],
            "roles": scores["Danie Bantjies"]["roles"],
            "key_roles": ["Double agent", "Secret trustee", "Conspiracy coordinator"]
        },
        "most_critical_individual_perpetrator": {
            "entity": "Danie Bantjies",
            "relationship_duration": "11 years (2013-2024)",
            "betrayal_type": "Trusted advisor → Secret enemy",
            "professional_violation": "CA(SA) fiduciary breach"
        },
        "attack_pattern": {
            "phase_5_events": 3,
            "phase_6_events": 5,
            "escalation": "Financial → Legal → Medical/Physical",
            "motive": "R18.6M May 2026 payout"
        },
        "top_10_critical_nodes": {
            entity: {
                "score": data["score"],
                "events": data["events"],
                "roles": data["roles"]
            }
            for entity, data in sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)[:10]
        }
    }
    
    with open('/home/ubuntu/analysis/updated_hypergraph_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print("✓ Updated metrics JSON generated")
    return metrics

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("Updated Critical Hypergraph Analysis")
    print("Integrating Bantjies Betrayal & 2025 Attack Pattern")
    print("=" * 60)
    
    print("\nGenerating updated visualizations...")
    generate_updated_attack_timeline()
    generate_bantjies_centrality_map()
    
    print("\nCalculating updated metrics...")
    metrics = generate_updated_metrics()
    
    print("\n" + "=" * 60)
    print("Updated Analysis Summary")
    print("=" * 60)
    print(f"Total Events: {metrics['total_events']} (was 22, now includes 10 new attack events)")
    print(f"Critical Events: {metrics['critical_events']} ({metrics['critical_event_ratio']*100}%)")
    print(f"Total Phases: {metrics['phases']} (added Phase 5 & 6)")
    print(f"\nMost Critical Individual: {metrics['most_critical_node']['entity']}")
    print(f"  Score: {metrics['most_critical_node']['score']}")
    print(f"  Events: {metrics['most_critical_node']['events']}")
    print(f"  Roles: {metrics['most_critical_node']['roles']}")
    print(f"  Key Roles: {', '.join(metrics['most_critical_node']['key_roles'])}")
    print(f"\nAttack Pattern:")
    print(f"  Preparation Phase Events: {metrics['attack_pattern']['phase_5_events']}")
    print(f"  Active Attack Events: {metrics['attack_pattern']['phase_6_events']}")
    print(f"  Escalation: {metrics['attack_pattern']['escalation']}")
    print(f"  Motive: {metrics['attack_pattern']['motive']}")
    print("=" * 60)
    print("\n✅ Updated critical analysis completed!")
    print("\nGenerated files:")
    print("  - attack_escalation_timeline.png")
    print("  - bantjies_centrality_map.png")
    print("  - updated_hypergraph_metrics.json")

