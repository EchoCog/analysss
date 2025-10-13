#!/usr/bin/env python3
"""
Enhanced analysis of Dan's correspondence focusing on legal entity structure
Key finding: "4 Legally distinct groups" - NOT A GROUP structure
"""

import json
from datetime import datetime
import hashlib

def create_enhanced_timeline_events():
    """Create enhanced timeline events with critical legal structure findings"""
    
    timeline_events = [
        {
            'date': '2025-06-06',
            'event_type': 'CRITICAL_LEGAL_STRUCTURE_DISCLOSURE',
            'description': 'Daniel Faucitt reveals "4 Legally distinct groups" structure - NOT A GROUP entity arrangement',
            'entities_involved': ['Daniel Faucitt', 'Danie Bantjes', 'RegimA entities'],
            'importance': 'CRITICAL',
            'category': 'legal_entity_structure',
            'legal_implications': 'Simple intercompany transactions require additional transactions to justify asset transfer',
            'key_statement': '4 Legally distinct groups between which simple intercompany transactions require additional transactions in order to justify asset transfer etc.'
        },
        {
            'date': '2025-06-06',
            'event_type': 'FINANCIAL_MISALLOCATION_DISCOVERY',
            'description': 'Discovery of minimum R1 million misallocation in RegimA Skin Treatments resulting in vanishing debt',
            'entities_involved': ['RegimA Skin Treatments', 'Daniel Faucitt'],
            'importance': 'URGENT',
            'category': 'financial_fraud_indicator',
            'fraud_risk': 'HIGH',
            'key_statement': 'minimum of just over a million has been misallocated resulting in vanishing debt'
        },
        {
            'date': '2025-06-06',
            'event_type': 'FRAUD_WARNING_ISSUED',
            'description': 'Daniel Faucitt warns that misreported forex transactions may be viewed as fraudulent by receiver',
            'entities_involved': ['Daniel Faucitt', 'Danie Bantjes', 'RegimA Skin Treatments'],
            'importance': 'URGENT',
            'category': 'compliance_risk',
            'fraud_risk': 'HIGH',
            'key_statement': 'may be viewed as fraudulent by the receiver since it misreports forex transactions by the same amount'
        },
        {
            'date': '2025-06-06',
            'event_type': 'ACCOUNTING_PROCESSING_GAP_IDENTIFIED',
            'description': 'No accounts processed since August 2023, everything showing as supplier FNB in Worldwide',
            'entities_involved': ['FNB', 'RegimA Worldwide Distribution', 'Daniel Faucitt'],
            'importance': 'HIGH',
            'category': 'accounting_irregularity',
            'time_gap': 'August 2023 to June 2025 (22 months)',
            'key_statement': 'nobody has actually processed any of those accounts since Aug 2023'
        },
        {
            'date': '2025-06-06',
            'event_type': 'COMPLEX_BUSINESS_STRUCTURE_REVEALED',
            'description': 'Revelation of 2 Marketplaces, 4 Distribution platforms, 36 Shopify Stores, 1100+ B2B Salon Tenants',
            'entities_involved': ['RegimA distribution network', 'Daniel Faucitt'],
            'importance': 'HIGH',
            'category': 'business_complexity',
            'scale': '36 Shopify Stores, 1100+ B2B Salon Tenants',
            'key_statement': '2 Marketplaces, 4 Distribution platforms with 36 Shopify Stores and over 1100 B2B Salon Tenants'
        }
    ]
    
    return timeline_events

def create_legal_entity_ownership_analysis():
    """Create detailed legal entity ownership analysis"""
    
    ownership_structures = {
        'J_P_Companies': {
            'description': 'Jax & Pete ownership structure',
            'shareholders': ['Jax', 'Pete'],
            'entities': [
                {'name': 'CORPCLO 2065', 'reg': '2003/086391/23'},
                {'name': 'CORPCLO 2304', 'reg': '2005/014378/23'},
                {'name': 'VILLA VIA ARCADIA NO 2', 'reg': '1996/004451/23'},
                {'name': 'REGIMA SKIN TREATMENTS', 'reg': '1992/005371/23'},
                {'name': 'REGIMA INTERNATIONAL SKIN TREATMENTS', 'reg': '2008/127748/23'}
            ],
            'legal_group': 1
        },
        'D_J_P_Companies': {
            'description': 'Dan, Jax & Pete ownership structure',
            'shareholders': ['Dan', 'Jax', 'Pete'],
            'entities': [
                {'name': 'AYMAC INTERNATIONAL', 'reg': '1999/061687/23'},
                {'name': 'STRATEGIC LOGISTICS', 'reg': '2008/136496/23'},
                {'name': 'REGIMA MEDIC', 'reg': '2017/087877/07'},
                {'name': 'REGIMA SPAZONE', 'reg': '2017/081833/07'},
                {'name': 'REGIMA WORLDWIDE DISTRIBUTION', 'reg': '2011/005722/07'}
            ],
            'legal_group': 2
        },
        'D_P_Companies': {
            'description': 'Dan & Pete ownership structure',
            'shareholders': ['Dan', 'Pete'],
            'entities': [
                {'name': 'REGIMA SA', 'reg': '2017/087935/07'}
            ],
            'legal_group': 3
        },
        'D_Only_Companies': {
            'description': 'Dan sole ownership structure',
            'shareholders': ['Dan'],
            'entities': [
                {'name': 'REGIMA ZONE', 'reg': '2017/110437/07'},
                {'name': 'REGIMA ZONE ACADEMY', 'reg': '2017/113134/07'},
                {'name': 'REGIMA ZONE IMPACT', 'reg': '2017/109415/07'},
                {'name': 'REZONANCE', 'reg': '2017/081396/07'},
                {'name': 'UNICORN DYNAMICS', 'reg': '2016/307425/07'},
                {'name': 'JOZI WAY TRADING', 'reg': '2016/240702/07'},
                {'name': 'PANDAMANIA', 'reg': '2021/306676/07'},
                {'name': 'VILLA PALMER HOMEOWNERS ASSOCIATION', 'reg': '2003/030388/08'}
            ],
            'legal_group': 4
        }
    }
    
    return ownership_structures

def create_critical_compliance_analysis():
    """Create critical compliance and fraud risk analysis"""
    
    compliance_analysis = {
        'legal_structure_implications': {
            'finding': '4 Legally distinct groups - NOT A GROUP structure',
            'implication': 'Inter-company transactions require additional justification',
            'compliance_risk': 'HIGH',
            'regulatory_concern': 'Transfer pricing and related party transaction compliance'
        },
        'fraud_indicators': [
            {
                'type': 'Financial Misallocation',
                'amount': 'Minimum R1 million',
                'entity': 'RegimA Skin Treatments',
                'description': 'Vanishing debt through misallocation',
                'risk_level': 'URGENT'
            },
            {
                'type': 'Forex Transaction Misreporting',
                'entity': 'RegimA Skin Treatments',
                'description': 'Misreports forex transactions by same amount as vanishing debt',
                'risk_level': 'URGENT'
            }
        ],
        'accounting_irregularities': [
            {
                'type': 'Processing Gap',
                'duration': '22 months (Aug 2023 - Jun 2025)',
                'description': 'No account processing, everything showing as supplier FNB',
                'affected_entity': 'RegimA Worldwide Distribution',
                'risk_level': 'HIGH'
            }
        ],
        'hidden_business_complexity': {
            'marketplaces': 2,
            'distribution_platforms': 4,
            'shopify_stores': 36,
            'b2b_salon_tenants': '1100+',
            'visibility_to_bantjes': 'Never seen these accounts',
            'risk_level': 'HIGH'
        }
    }
    
    return compliance_analysis

def update_hypergnn_with_legal_structure():
    """Update HyperGNN model with legal structure findings"""
    
    # Load existing hypergraph data
    try:
        with open('/home/ubuntu/analysis/super_sleuth_hypergraph.json', 'r') as f:
            hypergraph = json.load(f)
    except:
        hypergraph = {'nodes': [], 'edges': [], 'metadata': {}}
    
    # Add legal structure nodes
    legal_structure_nodes = [
        {
            'id': 'legal_group_1',
            'label': 'J P Legal Group',
            'type': 'legal_structure',
            'category': 'ownership_group',
            'shareholders': ['Jax', 'Pete'],
            'entity_count': 5,
            'legal_separation': True
        },
        {
            'id': 'legal_group_2',
            'label': 'D J P Legal Group',
            'type': 'legal_structure',
            'category': 'ownership_group',
            'shareholders': ['Dan', 'Jax', 'Pete'],
            'entity_count': 5,
            'legal_separation': True
        },
        {
            'id': 'legal_group_3',
            'label': 'D P Legal Group',
            'type': 'legal_structure',
            'category': 'ownership_group',
            'shareholders': ['Dan', 'Pete'],
            'entity_count': 1,
            'legal_separation': True
        },
        {
            'id': 'legal_group_4',
            'label': 'D Only Legal Group',
            'type': 'legal_structure',
            'category': 'ownership_group',
            'shareholders': ['Dan'],
            'entity_count': 8,
            'legal_separation': True
        },
        {
            'id': 'daniel_faucitt',
            'label': 'Daniel Faucitt',
            'type': 'entity',
            'category': 'people',
            'role': 'Financial Analyst/Whistleblower',
            'email': 'd@rzo.io',
            'critical_disclosure': True
        }
    ]
    
    # Add legal separation edges
    legal_separation_edges = [
        {
            'id': 'legal_sep_1_2',
            'source': 'legal_group_1',
            'target': 'legal_group_2',
            'type': 'legal_separation',
            'weight': 1.0,
            'requires_justification': True
        },
        {
            'id': 'legal_sep_1_3',
            'source': 'legal_group_1',
            'target': 'legal_group_3',
            'type': 'legal_separation',
            'weight': 1.0,
            'requires_justification': True
        },
        {
            'id': 'legal_sep_1_4',
            'source': 'legal_group_1',
            'target': 'legal_group_4',
            'type': 'legal_separation',
            'weight': 1.0,
            'requires_justification': True
        },
        {
            'id': 'legal_sep_2_3',
            'source': 'legal_group_2',
            'target': 'legal_group_3',
            'type': 'legal_separation',
            'weight': 1.0,
            'requires_justification': True
        },
        {
            'id': 'legal_sep_2_4',
            'source': 'legal_group_2',
            'target': 'legal_group_4',
            'type': 'legal_separation',
            'weight': 1.0,
            'requires_justification': True
        },
        {
            'id': 'legal_sep_3_4',
            'source': 'legal_group_3',
            'target': 'legal_group_4',
            'type': 'legal_separation',
            'weight': 1.0,
            'requires_justification': True
        }
    ]
    
    # Update hypergraph
    hypergraph['nodes'].extend(legal_structure_nodes)
    hypergraph['edges'].extend(legal_separation_edges)
    
    # Update metadata
    hypergraph['metadata'].update({
        'legal_structure_analysis': True,
        'legal_groups_identified': 4,
        'not_a_group_structure': True,
        'critical_disclosure_date': '2025-06-06',
        'disclosure_source': 'Daniel Faucitt'
    })
    
    return hypergraph

def main():
    """Main enhanced analysis function"""
    
    print("🚨 Enhanced Dan Correspondence Analysis - CRITICAL LEGAL STRUCTURE")
    print("=" * 80)
    
    # Create enhanced analysis components
    timeline_events = create_enhanced_timeline_events()
    ownership_structures = create_legal_entity_ownership_analysis()
    compliance_analysis = create_critical_compliance_analysis()
    updated_hypergraph = update_hypergnn_with_legal_structure()
    
    # Create comprehensive enhanced analysis
    enhanced_analysis = {
        'analysis_metadata': {
            'analysis_type': 'CRITICAL_LEGAL_STRUCTURE_DISCLOSURE',
            'source_document': 'Dan Faucitt correspondence to Danie Bantjes',
            'analysis_date': datetime.now().isoformat(),
            'criticality_level': 'MAXIMUM',
            'key_finding': '4 Legally distinct groups - NOT A GROUP structure'
        },
        'critical_timeline_events': timeline_events,
        'legal_entity_ownership_structures': ownership_structures,
        'compliance_and_fraud_analysis': compliance_analysis,
        'updated_hypergraph_structure': {
            'total_nodes': len(updated_hypergraph['nodes']),
            'legal_structure_nodes_added': 5,
            'legal_separation_edges_added': 6,
            'not_a_group_confirmed': True
        },
        'key_insights': {
            'legal_structure_complexity': '4 distinct legal groups requiring transaction justification',
            'fraud_risk_level': 'URGENT - R1M+ misallocation identified',
            'accounting_gap': '22 months of unprocessed accounts',
            'business_scale_hidden': '36 Shopify stores, 1100+ B2B tenants unknown to Bantjes',
            'regulatory_implications': 'Transfer pricing and related party transaction compliance issues'
        }
    }
    
    # Save enhanced analysis
    enhanced_file = '/home/ubuntu/analysis/CRITICAL_dan_correspondence_enhanced.json'
    with open(enhanced_file, 'w') as f:
        json.dump(enhanced_analysis, f, indent=2)
    
    # Save updated hypergraph
    hypergraph_file = '/home/ubuntu/analysis/enhanced_hypergraph_legal_structure.json'
    with open(hypergraph_file, 'w') as f:
        json.dump(updated_hypergraph, f, indent=2)
    
    # Create critical timeline update
    critical_timeline_file = '/home/ubuntu/analysis/CRITICAL_TIMELINE_LEGAL_STRUCTURE.md'
    with open(critical_timeline_file, 'w') as f:
        f.write("# CRITICAL TIMELINE UPDATE - LEGAL STRUCTURE DISCLOSURE\n\n")
        f.write("## 🚨 MAXIMUM IMPORTANCE: NOT A GROUP STRUCTURE REVEALED\n\n")
        f.write("**Date**: 2025-06-06\n")
        f.write("**Source**: Daniel Faucitt correspondence to Danie Bantjes\n")
        f.write("**Criticality**: MAXIMUM\n\n")
        
        f.write("### KEY FINDING: 4 LEGALLY DISTINCT GROUPS\n\n")
        f.write("**Critical Statement**: \"4 Legally distinct groups between which simple intercompany transactions require additional transactions in order to justify asset transfer etc.\"\n\n")
        
        f.write("### LEGAL STRUCTURE BREAKDOWN\n\n")
        for group_key, group_data in ownership_structures.items():
            f.write(f"#### {group_data['description']}\n")
            f.write(f"- **Shareholders**: {', '.join(group_data['shareholders'])}\n")
            f.write(f"- **Legal Group**: {group_data['legal_group']}\n")
            f.write(f"- **Entities**: {len(group_data['entities'])}\n")
            for entity in group_data['entities']:
                f.write(f"  - {entity['name']} ({entity['reg']})\n")
            f.write("\n")
        
        f.write("### CRITICAL TIMELINE EVENTS\n\n")
        for event in timeline_events:
            f.write(f"#### {event['event_type'].replace('_', ' ').title()}\n")
            f.write(f"- **Date**: {event['date']}\n")
            f.write(f"- **Importance**: {event['importance']}\n")
            f.write(f"- **Description**: {event['description']}\n")
            if 'key_statement' in event:
                f.write(f"- **Key Statement**: \"{event['key_statement']}\"\n")
            f.write(f"- **Entities**: {', '.join(event['entities_involved'])}\n\n")
    
    print(f"✅ Enhanced analysis completed!")
    print(f"📊 Enhanced analysis: {enhanced_file}")
    print(f"🕸️ Updated hypergraph: {hypergraph_file}")
    print(f"📅 Critical timeline: {critical_timeline_file}")
    print(f"\n🚨 CRITICAL FINDINGS:")
    print(f"   Legal Groups: 4 distinct groups")
    print(f"   Fraud Risk: URGENT (R1M+ misallocation)")
    print(f"   Accounting Gap: 22 months unprocessed")
    print(f"   Hidden Scale: 36 Shopify stores, 1100+ B2B tenants")
    
    return enhanced_analysis

if __name__ == "__main__":
    main()
