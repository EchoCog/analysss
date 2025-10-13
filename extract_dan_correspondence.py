#!/usr/bin/env python3
"""
Extract and analyze Dan's correspondence to Bantjes
Focus on "NOT A GROUP" statement and legal entity ownership models
"""

import re
import json
import base64
from datetime import datetime
import hashlib

def decode_email_content(file_path):
    """Decode the email content from base64"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find base64 encoded content
    base64_pattern = r'Content-Transfer-Encoding: base64\s*Content-length: \d+\s*\n\n(.*?)(?=--_)'
    matches = re.findall(base64_pattern, content, re.DOTALL)
    
    decoded_content = ""
    for match in matches:
        try:
            # Clean up the base64 content
            clean_b64 = re.sub(r'\s+', '', match)
            decoded = base64.b64decode(clean_b64).decode('utf-8', errors='ignore')
            decoded_content += decoded + "\n"
        except Exception as e:
            print(f"Error decoding base64: {e}")
    
    return decoded_content

def extract_legal_entities(content):
    """Extract legal entities and their details"""
    
    entities = []
    
    # Find the LEGAL ENTITIES section
    legal_entities_pattern = r'# LEGAL ENTITIES\s*-+\s*(.*?)(?=# QUICKBOOKS|-+\s*# QUICKBOOKS)'
    legal_match = re.search(legal_entities_pattern, content, re.DOTALL)
    
    if legal_match:
        legal_section = legal_match.group(1)
        
        # Extract individual entities
        entity_pattern = r'([DJ\s\-P]+)\s*Company:\s*([^,]+),\s*(\d{4}/\d+/\d+)'
        entities_matches = re.findall(entity_pattern, legal_section)
        
        for ownership, name, reg_number in entities_matches:
            entity = {
                'name': name.strip(),
                'registration_number': reg_number.strip(),
                'ownership_structure': ownership.strip(),
                'entity_type': 'company',
                'legal_status': 'registered'
            }
            
            # Parse ownership structure
            if 'D J P' in ownership:
                entity['shareholders'] = ['Dan', 'Jax', 'Pete']
                entity['ownership_type'] = 'three_way_partnership'
            elif 'J P' in ownership:
                entity['shareholders'] = ['Jax', 'Pete']
                entity['ownership_type'] = 'two_way_partnership'
            elif 'D - P' in ownership:
                entity['shareholders'] = ['Dan', 'Pete']
                entity['ownership_type'] = 'two_way_partnership'
            elif 'D - -' in ownership:
                entity['shareholders'] = ['Dan']
                entity['ownership_type'] = 'sole_ownership'
            
            entities.append(entity)
    
    return entities

def extract_quickbooks_entities(content):
    """Extract QuickBooks entities and their configurations"""
    
    qb_entities = []
    
    # Find QuickBooks section
    qb_pattern = r'# QUICKBOOKS\s*-+\s*(.*?)(?=UK:|$)'
    qb_match = re.search(qb_pattern, content, re.DOTALL)
    
    if qb_match:
        qb_section = qb_match.group(1)
        
        # Extract ZA entities
        za_pattern = r'ZA:\s*(.*?)(?=UK:|$)'
        za_match = re.search(za_pattern, qb_section, re.DOTALL)
        
        if za_match:
            za_content = za_match.group(1)
            
            # Extract individual QB entities
            entity_lines = za_content.strip().split('\n')
            for line in entity_lines:
                if 'QuickBooks' in line:
                    parts = line.split('QuickBooks')
                    if len(parts) >= 2:
                        company_name = parts[0].strip()
                        qb_version = parts[1].strip()
                        
                        qb_entity = {
                            'name': company_name,
                            'quickbooks_version': qb_version,
                            'jurisdiction': 'ZA',
                            'system_type': 'accounting_software'
                        }
                        qb_entities.append(qb_entity)
    
    return qb_entities

def extract_critical_statements(content):
    """Extract critical statements and warnings"""
    
    critical_statements = []
    
    # Look for "NOT A GROUP" statements
    not_group_pattern = r'(NOT A GROUP[^.]*\.?)'
    not_group_matches = re.findall(not_group_pattern, content, re.IGNORECASE)
    
    for match in not_group_matches:
        critical_statements.append({
            'type': 'legal_structure_clarification',
            'statement': match.strip(),
            'importance': 'CRITICAL',
            'category': 'legal_entity_structure'
        })
    
    # Look for fraud warnings
    fraud_pattern = r'(may be viewed as fraudulent[^.]*\.?)'
    fraud_matches = re.findall(fraud_pattern, content, re.IGNORECASE)
    
    for match in fraud_matches:
        critical_statements.append({
            'type': 'fraud_warning',
            'statement': match.strip(),
            'importance': 'URGENT',
            'category': 'compliance_risk'
        })
    
    # Look for misallocation warnings
    misallocation_pattern = r'(minimum of just over a million has been misallocated[^.]*\.?)'
    misallocation_matches = re.findall(misallocation_pattern, content, re.IGNORECASE)
    
    for match in misallocation_matches:
        critical_statements.append({
            'type': 'financial_misallocation',
            'statement': match.strip(),
            'importance': 'URGENT',
            'category': 'financial_irregularity'
        })
    
    return critical_statements

def extract_timeline_events(content):
    """Extract timeline events from the correspondence"""
    
    timeline_events = []
    
    # Extract the email date
    date_pattern = r'Date: ([^,]+, \d+ \w+ \d+ at \d+:\d+)'
    date_match = re.search(date_pattern, content)
    
    if date_match:
        email_date = "2025-06-06"  # From the email headers
        
        # Key timeline event: Dan's analysis and warnings
        timeline_events.append({
            'date': email_date,
            'event_type': 'critical_correspondence',
            'description': 'Dan Faucitt sends critical analysis to Danie Bantjes highlighting legal entity structure issues and fraud risks',
            'entities_involved': ['Daniel Faucitt', 'Danie Bantjes', 'RegimA entities'],
            'importance': 'CRITICAL',
            'category': 'legal_compliance_warning'
        })
        
        # Misallocation discovery
        timeline_events.append({
            'date': email_date,
            'event_type': 'financial_irregularity_discovery',
            'description': 'Discovery of minimum R1 million misallocation in RegimA Skin Treatments resulting in vanishing debt',
            'entities_involved': ['RegimA Skin Treatments', 'Daniel Faucitt'],
            'importance': 'URGENT',
            'category': 'financial_fraud_indicator'
        })
        
        # Accounts processing gap identified
        timeline_events.append({
            'date': email_date,
            'event_type': 'accounting_gap_identification',
            'description': 'Identification that no accounts have been processed since August 2023, everything showing as supplier FNB',
            'entities_involved': ['FNB', 'RegimA Worldwide', 'Daniel Faucitt'],
            'importance': 'HIGH',
            'category': 'accounting_irregularity'
        })
    
    return timeline_events

def extract_entity_relationships(content):
    """Extract entity relationships and ownership structures"""
    
    relationships = []
    
    # Extract the key relationship statement about 4 legally distinct groups
    distinct_groups_pattern = r'(4 Legally distinct groups[^.]*\.?)'
    distinct_matches = re.findall(distinct_groups_pattern, content, re.IGNORECASE)
    
    for match in distinct_matches:
        relationships.append({
            'type': 'legal_separation',
            'description': match.strip(),
            'implication': 'Inter-company transactions require additional justification',
            'importance': 'CRITICAL'
        })
    
    # Extract supply chain relationships
    supply_chain_pattern = r'(supply chain activities[^.]*\.?)'
    supply_matches = re.findall(supply_chain_pattern, content, re.IGNORECASE)
    
    for match in supply_matches:
        relationships.append({
            'type': 'operational_relationship',
            'description': match.strip(),
            'category': 'supply_chain'
        })
    
    return relationships

def analyze_correspondence():
    """Main analysis function"""
    
    print("🔍 Analyzing Dan's Correspondence to Bantjes...")
    print("=" * 60)
    
    # Decode email content
    content = decode_email_content('/home/ubuntu/upload/Fwd_update-SomeInitialInformation&OperatingEntityLists.eml')
    
    # Extract all components
    legal_entities = extract_legal_entities(content)
    qb_entities = extract_quickbooks_entities(content)
    critical_statements = extract_critical_statements(content)
    timeline_events = extract_timeline_events(content)
    relationships = extract_entity_relationships(content)
    
    # Create comprehensive analysis
    analysis = {
        'correspondence_metadata': {
            'from': 'Daniel Faucitt <d@rzo.io>',
            'to': 'Danie Bantjes',
            'date': '2025-06-06',
            'subject': 'Re: update - Some Initial Information & Operating Entity Lists',
            'analysis_timestamp': datetime.now().isoformat(),
            'importance_level': 'CRITICAL'
        },
        'legal_entities': legal_entities,
        'quickbooks_entities': qb_entities,
        'critical_statements': critical_statements,
        'timeline_events': timeline_events,
        'entity_relationships': relationships,
        'key_findings': {
            'total_legal_entities': len(legal_entities),
            'ownership_structures_identified': len(set([e.get('ownership_type') for e in legal_entities])),
            'critical_warnings': len([s for s in critical_statements if s['importance'] == 'CRITICAL']),
            'urgent_issues': len([s for s in critical_statements if s['importance'] == 'URGENT']),
            'fraud_indicators': len([s for s in critical_statements if 'fraud' in s['type']])
        },
        'not_a_group_analysis': {
            'statement_found': any('NOT A GROUP' in s['statement'].upper() for s in critical_statements),
            'legal_implications': '4 legally distinct groups requiring additional transaction justification',
            'ownership_complexity': 'Multiple ownership structures (D J P, J P, D - P, D - -) indicating complex legal arrangements'
        }
    }
    
    return analysis, content

def save_analysis_results(analysis, content):
    """Save analysis results to files"""
    
    # Save main analysis
    analysis_file = '/home/ubuntu/analysis/dan_correspondence_analysis.json'
    with open(analysis_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    # Save decoded content for reference
    content_file = '/home/ubuntu/analysis/dan_correspondence_decoded.txt'
    with open(content_file, 'w') as f:
        f.write(content)
    
    # Create timeline update
    timeline_file = '/home/ubuntu/analysis/dan_correspondence_timeline.md'
    with open(timeline_file, 'w') as f:
        f.write("# Dan's Correspondence Timeline Events - CRITICAL\n\n")
        f.write("## 2025-06-06: Critical Legal Entity Analysis\n\n")
        
        for event in analysis['timeline_events']:
            f.write(f"### {event['event_type'].replace('_', ' ').title()}\n")
            f.write(f"- **Date**: {event['date']}\n")
            f.write(f"- **Importance**: {event['importance']}\n")
            f.write(f"- **Description**: {event['description']}\n")
            f.write(f"- **Entities**: {', '.join(event['entities_involved'])}\n")
            f.write(f"- **Category**: {event['category']}\n\n")
        
        f.write("## Critical Statements\n\n")
        for statement in analysis['critical_statements']:
            f.write(f"### {statement['type'].replace('_', ' ').title()}\n")
            f.write(f"- **Importance**: {statement['importance']}\n")
            f.write(f"- **Statement**: {statement['statement']}\n")
            f.write(f"- **Category**: {statement['category']}\n\n")
    
    # Create entity ownership model
    ownership_file = '/home/ubuntu/analysis/legal_entity_ownership_models.md'
    with open(ownership_file, 'w') as f:
        f.write("# Legal Entity Ownership Models - RegimA Group\n\n")
        f.write("## CRITICAL: NOT A GROUP Structure\n\n")
        f.write("**Key Finding**: 4 legally distinct groups requiring additional transaction justification\n\n")
        
        f.write("## Ownership Structures\n\n")
        
        ownership_groups = {}
        for entity in analysis['legal_entities']:
            ownership_type = entity.get('ownership_type', 'unknown')
            if ownership_type not in ownership_groups:
                ownership_groups[ownership_type] = []
            ownership_groups[ownership_type].append(entity)
        
        for ownership_type, entities in ownership_groups.items():
            f.write(f"### {ownership_type.replace('_', ' ').title()}\n")
            for entity in entities:
                f.write(f"- **{entity['name']}** ({entity['registration_number']})\n")
                f.write(f"  - Shareholders: {', '.join(entity.get('shareholders', []))}\n")
                f.write(f"  - Structure: {entity['ownership_structure']}\n\n")
    
    print(f"✅ Analysis saved to:")
    print(f"   📊 Main analysis: {analysis_file}")
    print(f"   📝 Decoded content: {content_file}")
    print(f"   📅 Timeline: {timeline_file}")
    print(f"   🏢 Ownership models: {ownership_file}")
    
    return analysis_file, content_file, timeline_file, ownership_file

def main():
    """Main execution function"""
    
    analysis, content = analyze_correspondence()
    files = save_analysis_results(analysis, content)
    
    print(f"\n📊 Analysis Summary:")
    print(f"   Legal Entities: {analysis['key_findings']['total_legal_entities']}")
    print(f"   Critical Warnings: {analysis['key_findings']['critical_warnings']}")
    print(f"   Urgent Issues: {analysis['key_findings']['urgent_issues']}")
    print(f"   Fraud Indicators: {analysis['key_findings']['fraud_indicators']}")
    print(f"   NOT A GROUP Found: {analysis['not_a_group_analysis']['statement_found']}")
    
    return analysis

if __name__ == "__main__":
    main()
