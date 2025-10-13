#!/usr/bin/env python3
"""
Analysis of intersecting ownership structures in RegimA entities
Focus on how corporate respondents create overlapping control between groups
"""

import json
from datetime import datetime

def analyze_ownership_intersections():
    """Analyze the intersecting ownership patterns"""
    
    # Define the ownership groups from Dan's correspondence
    ownership_groups = {
        'J_P_Group': {
            'shareholders': ['Jax', 'Pete'],
            'entities': [
                'CORPCLO 2065',
                'CORPCLO 2304', 
                'VILLA VIA ARCADIA NO 2',
                'REGIMA SKIN TREATMENTS',
                'REGIMA INTERNATIONAL SKIN TREATMENTS'
            ]
        },
        'D_J_P_Group': {
            'shareholders': ['Dan', 'Jax', 'Pete'],
            'entities': [
                'AYMAC INTERNATIONAL',
                'STRATEGIC LOGISTICS',
                'REGIMA MEDIC',
                'REGIMA SPAZONE',
                'REGIMA WORLDWIDE DISTRIBUTION'
            ]
        },
        'D_P_Group': {
            'shareholders': ['Dan', 'Pete'],
            'entities': [
                'REGIMA SA'
            ]
        },
        'D_Only_Group': {
            'shareholders': ['Dan'],
            'entities': [
                'REGIMA ZONE',
                'REGIMA ZONE ACADEMY',
                'REGIMA ZONE IMPACT',
                'REZONANCE',
                'UNICORN DYNAMICS',
                'JOZI WAY TRADING',
                'PANDAMANIA',
                'VILLA PALMER HOMEOWNERS ASSOCIATION'
            ]
        }
    }
    
    return ownership_groups

def identify_shareholder_intersections(ownership_groups):
    """Identify how shareholders create intersections between groups"""
    
    intersections = {}
    
    # Analyze each shareholder's presence across groups
    all_shareholders = set()
    for group_name, group_data in ownership_groups.items():
        all_shareholders.update(group_data['shareholders'])
    
    for shareholder in all_shareholders:
        shareholder_groups = []
        for group_name, group_data in ownership_groups.items():
            if shareholder in group_data['shareholders']:
                shareholder_groups.append({
                    'group': group_name,
                    'entities': group_data['entities'],
                    'co_shareholders': [s for s in group_data['shareholders'] if s != shareholder]
                })
        
        intersections[shareholder] = {
            'groups_involved': len(shareholder_groups),
            'total_entities_controlled': sum(len(g['entities']) for g in shareholder_groups),
            'group_details': shareholder_groups
        }
    
    return intersections

def analyze_corporate_respondent_implications(intersections):
    """Analyze how corporate respondents create legal complexities"""
    
    corporate_implications = {}
    
    for shareholder, data in intersections.items():
        if data['groups_involved'] > 1:
            # This shareholder creates intersections
            corporate_implications[shareholder] = {
                'intersection_type': 'multi_group_shareholder',
                'groups_count': data['groups_involved'],
                'entities_count': data['total_entities_controlled'],
                'legal_implications': [],
                'control_analysis': {}
            }
            
            # Analyze control implications
            if shareholder == 'Dan':
                corporate_implications[shareholder]['legal_implications'].extend([
                    'Common control across 3 groups (D_J_P, D_P, D_Only)',
                    'Potential deemed control through multiple group participation',
                    'Related party transaction complexity across 14 entities',
                    'Transfer pricing implications for inter-group transactions'
                ])
                corporate_implications[shareholder]['control_analysis'] = {
                    'direct_control_entities': 8,  # D_Only group
                    'shared_control_entities': 6,  # D_J_P + D_P groups
                    'total_influence': 14,
                    'control_percentage_estimate': 'Varies by entity - potentially 33.3% in D_J_P, 50% in D_P, 100% in D_Only'
                }
            
            elif shareholder == 'Pete':
                corporate_implications[shareholder]['legal_implications'].extend([
                    'Common control across 3 groups (J_P, D_J_P, D_P)',
                    'Intersection with both Jax and Dan creates complex web',
                    'Potential swing vote in D_J_P group decisions',
                    'Related party implications across 11 entities'
                ])
                corporate_implications[shareholder]['control_analysis'] = {
                    'shared_control_entities': 11,  # All groups except D_Only
                    'total_influence': 11,
                    'control_percentage_estimate': 'Potentially 50% in J_P, 33.3% in D_J_P, 50% in D_P'
                }
            
            elif shareholder == 'Jax':
                corporate_implications[shareholder]['legal_implications'].extend([
                    'Common control across 2 groups (J_P, D_J_P)',
                    'Shared control with Pete in J_P group',
                    'Minority position in D_J_P group with Dan and Pete',
                    'Related party implications across 10 entities'
                ])
                corporate_implications[shareholder]['control_analysis'] = {
                    'shared_control_entities': 10,  # J_P + D_J_P groups
                    'total_influence': 10,
                    'control_percentage_estimate': 'Potentially 50% in J_P, 33.3% in D_J_P'
                }
    
    return corporate_implications

def calculate_effective_control_scenarios():
    """Calculate different control scenarios based on intersections"""
    
    control_scenarios = {
        'scenario_1_individual_control': {
            'description': 'Each shareholder controls only their direct holdings',
            'dan_control': 8,  # D_Only entities
            'pete_control': 0,  # No sole control
            'jax_control': 0,   # No sole control
            'shared_entities': 11,  # All others require joint decisions
            'legal_group_formation': 'No groups formed - all below control thresholds'
        },
        'scenario_2_deemed_control': {
            'description': 'Shareholders deemed to have control through intersections',
            'dan_potential_control': 14,  # D_Only + influence in D_J_P + D_P
            'pete_potential_control': 11,  # Influence in J_P + D_J_P + D_P
            'jax_potential_control': 10,   # Influence in J_P + D_J_P
            'legal_group_formation': 'Potential for deemed control groups'
        },
        'scenario_3_concert_party': {
            'description': 'Shareholders acting in concert across intersections',
            'combined_control': 19,  # All entities under concert party control
            'legal_group_formation': 'Single group if concert party established',
            'regulatory_implications': 'Would require disclosure and compliance as single group'
        }
    }
    
    return control_scenarios

def analyze_legal_group_implications():
    """Analyze what the intersections mean for legal group formation"""
    
    legal_implications = {
        'current_structure_problems': [
            'Overlapping shareholders create ambiguous control relationships',
            'No clear single controlling entity across all 19 companies',
            'Multiple potential control interpretations depending on legal analysis',
            'Related party relationships exist but group control unclear'
        ],
        'potential_group_formations': {
            'dan_centric_group': {
                'entities': 14,
                'control_basis': 'Direct control (D_Only) + significant influence (D_J_P, D_P)',
                'likelihood': 'Medium - depends on actual shareholding percentages'
            },
            'three_way_partnership_group': {
                'entities': 5,  # D_J_P entities
                'control_basis': 'Joint control by Dan, Jax, Pete',
                'likelihood': 'Low - joint control typically doesn\'t create group relationships'
            },
            'no_group_formation': {
                'entities': 19,
                'control_basis': 'All entities remain separate due to shared control',
                'likelihood': 'High - current evidence supports this interpretation'
            }
        },
        'regulatory_risks': [
            'SARS may deem control relationships exist despite shared ownership',
            'Transfer pricing rules apply regardless of formal group status',
            'Related party disclosure requirements triggered by intersections',
            'Corporate governance complexity due to overlapping directorships'
        ]
    }
    
    return legal_implications

def create_intersection_visualization_data():
    """Create data for visualizing the ownership intersections"""
    
    visualization_data = {
        'nodes': [
            # Shareholders
            {'id': 'dan', 'type': 'shareholder', 'label': 'Dan', 'groups': 3, 'entities': 14},
            {'id': 'pete', 'type': 'shareholder', 'label': 'Pete', 'groups': 3, 'entities': 11},
            {'id': 'jax', 'type': 'shareholder', 'label': 'Jax', 'groups': 2, 'entities': 10},
            
            # Legal Groups
            {'id': 'jp_group', 'type': 'legal_group', 'label': 'J P Group', 'entities': 5},
            {'id': 'djp_group', 'type': 'legal_group', 'label': 'D J P Group', 'entities': 5},
            {'id': 'dp_group', 'type': 'legal_group', 'label': 'D P Group', 'entities': 1},
            {'id': 'd_group', 'type': 'legal_group', 'label': 'D Only Group', 'entities': 8}
        ],
        'edges': [
            # Dan's intersections
            {'source': 'dan', 'target': 'djp_group', 'type': 'shared_control', 'weight': 0.33},
            {'source': 'dan', 'target': 'dp_group', 'type': 'shared_control', 'weight': 0.5},
            {'source': 'dan', 'target': 'd_group', 'type': 'sole_control', 'weight': 1.0},
            
            # Pete's intersections
            {'source': 'pete', 'target': 'jp_group', 'type': 'shared_control', 'weight': 0.5},
            {'source': 'pete', 'target': 'djp_group', 'type': 'shared_control', 'weight': 0.33},
            {'source': 'pete', 'target': 'dp_group', 'type': 'shared_control', 'weight': 0.5},
            
            # Jax's intersections
            {'source': 'jax', 'target': 'jp_group', 'type': 'shared_control', 'weight': 0.5},
            {'source': 'jax', 'target': 'djp_group', 'type': 'shared_control', 'weight': 0.33},
            
            # Group intersections (through shared shareholders)
            {'source': 'jp_group', 'target': 'djp_group', 'type': 'shareholder_intersection', 'via': 'pete_jax'},
            {'source': 'djp_group', 'target': 'dp_group', 'type': 'shareholder_intersection', 'via': 'dan_pete'},
            {'source': 'djp_group', 'target': 'd_group', 'type': 'shareholder_intersection', 'via': 'dan'},
            {'source': 'dp_group', 'target': 'd_group', 'type': 'shareholder_intersection', 'via': 'dan'}
        ]
    }
    
    return visualization_data

def main():
    """Main analysis function"""
    
    print("🔍 Analyzing Ownership Intersections and Corporate Respondent Implications")
    print("=" * 80)
    
    # Perform analysis
    ownership_groups = analyze_ownership_intersections()
    intersections = identify_shareholder_intersections(ownership_groups)
    corporate_implications = analyze_corporate_respondent_implications(intersections)
    control_scenarios = calculate_effective_control_scenarios()
    legal_implications = analyze_legal_group_implications()
    visualization_data = create_intersection_visualization_data()
    
    # Create comprehensive analysis
    intersection_analysis = {
        'analysis_metadata': {
            'analysis_type': 'OWNERSHIP_INTERSECTION_ANALYSIS',
            'focus': 'Corporate respondent intersections between legal groups',
            'analysis_date': datetime.now().isoformat(),
            'key_finding': 'Shareholders create complex intersections between supposedly distinct groups'
        },
        'ownership_groups': ownership_groups,
        'shareholder_intersections': intersections,
        'corporate_respondent_implications': corporate_implications,
        'control_scenarios': control_scenarios,
        'legal_group_implications': legal_implications,
        'visualization_data': visualization_data,
        'key_insights': {
            'dan_intersection_impact': 'Controls/influences 14 entities across 3 groups',
            'pete_intersection_impact': 'Influences 11 entities across 3 groups',
            'jax_intersection_impact': 'Influences 10 entities across 2 groups',
            'total_intersections': 6,  # Number of group-to-group connections
            'control_complexity': 'High - multiple potential control interpretations'
        }
    }
    
    # Save analysis
    analysis_file = '/home/ubuntu/analysis/ownership_intersection_analysis.json'
    with open(analysis_file, 'w') as f:
        json.dump(intersection_analysis, f, indent=2)
    
    # Create summary report
    summary_file = '/home/ubuntu/analysis/OWNERSHIP_INTERSECTION_SUMMARY.md'
    with open(summary_file, 'w') as f:
        f.write("# Ownership Intersection Analysis - Corporate Respondent Implications\n\n")
        f.write("## Key Finding: Shareholders Create Complex Group Intersections\n\n")
        
        f.write("### Shareholder Intersection Matrix\n\n")
        f.write("| Shareholder | Groups Involved | Entities Controlled | Intersection Type |\n")
        f.write("|-------------|-----------------|--------------------|-----------------|\n")
        for shareholder, data in intersections.items():
            f.write(f"| {shareholder} | {data['groups_involved']} | {data['total_entities_controlled']} | ")
            if data['groups_involved'] > 1:
                f.write("Multi-group intersection |\n")
            else:
                f.write("Single group |\n")
        
        f.write("\n### Corporate Respondent Implications\n\n")
        for shareholder, implications in corporate_implications.items():
            f.write(f"#### {shareholder}\n")
            f.write(f"- **Groups**: {implications['groups_count']}\n")
            f.write(f"- **Entities**: {implications['entities_count']}\n")
            f.write(f"- **Control Analysis**: {implications['control_analysis']}\n")
            f.write("- **Legal Implications**:\n")
            for implication in implications['legal_implications']:
                f.write(f"  - {implication}\n")
            f.write("\n")
        
        f.write("### Control Scenarios\n\n")
        for scenario_name, scenario_data in control_scenarios.items():
            f.write(f"#### {scenario_data['description']}\n")
            f.write(f"- **Legal Group Formation**: {scenario_data['legal_group_formation']}\n")
            if 'regulatory_implications' in scenario_data:
                f.write(f"- **Regulatory Implications**: {scenario_data['regulatory_implications']}\n")
            f.write("\n")
    
    print(f"✅ Intersection analysis completed!")
    print(f"📊 Analysis file: {analysis_file}")
    print(f"📝 Summary report: {summary_file}")
    print(f"\n🔍 Key Intersections:")
    print(f"   Dan: 3 groups, 14 entities")
    print(f"   Pete: 3 groups, 11 entities") 
    print(f"   Jax: 2 groups, 10 entities")
    print(f"   Total group intersections: 6")
    
    return intersection_analysis

if __name__ == "__main__":
    main()
