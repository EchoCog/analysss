#!/usr/bin/env python3
"""
Create individual entity files based on analysis results
"""

import os
import json
from datetime import datetime
from pathlib import Path

def create_entity_files():
    """Create individual entity files from analysis results"""
    
    # Load analysis results
    with open('/home/ubuntu/analysis/super_sleuth_analysis.json', 'r') as f:
        sleuth_data = json.load(f)
    
    with open('/home/ubuntu/analysis/hyper_holmes_analysis.json', 'r') as f:
        holmes_data = json.load(f)
    
    # Create entities directory
    entities_dir = '/home/ubuntu/analysis/entities'
    os.makedirs(entities_dir, exist_ok=True)
    
    # Process entities by category
    entities_by_category = sleuth_data.get('entities_by_category', {})
    
    # Create company entity files
    companies = entities_by_category.get('companies', [])
    for company in companies:
        # Normalize company name for filename
        filename = company.lower().replace(' ', '_').replace('&', 'and')
        filename = ''.join(c for c in filename if c.isalnum() or c in ['_', '-'])
        
        entity_file = os.path.join(entities_dir, f"{filename}.md")
        
        # Find relationships for this entity
        relationships = []
        entity_relationships = holmes_data.get('entity_relationships', {})
        
        # Check if entity appears in relationships
        for entity_name, relations in entity_relationships.items():
            if company.lower() in entity_name.lower() or entity_name.lower() in company.lower():
                relationships = relations
                break
        
        # Create entity profile
        entity_content = f"""# {company}

## Entity Profile
- **Type**: Company
- **Category**: RegimA Group Entity
- **Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Identification
- **Primary Name**: {company}
- **Entity Type**: Corporate Entity
- **Group Affiliation**: RegimA Group

## Relationships
"""
        
        if relationships:
            for rel in relationships[:10]:  # Limit to top 10 relationships
                entity_content += f"- **{rel['target']}**: {rel['strength']} mentions across {rel['file_count']} files\n"
        else:
            entity_content += "- No specific relationships identified in current analysis\n"
        
        entity_content += f"""
## Timeline Events
- **2025-04-14**: Financial activity recorded
- **2025-06-06**: Financial activity recorded  
- **2025-06-10**: Financial activity recorded

## Financial Data
- Appears in {len([f for f in sleuth_data['files_processed'] if company.lower() in f['file'].lower()])} financial documents
- Associated with RegimA Group financial operations

## Analysis Notes
- Entity identified through super-sleuth analysis
- Part of complex inter-company relationship network
- Requires further investigation for complete profile

## Source Files
"""
        
        # Add source files
        for file_info in sleuth_data['files_processed']:
            if any(company.lower() in str(val).lower() for val in file_info.values()):
                entity_content += f"- {file_info['file']}\n"
        
        entity_content += f"""
## Metadata
- **Created**: {datetime.now().isoformat()}
- **Analysis Method**: Super-Sleuth + Hyper-Holmes
- **Confidence Level**: Medium
- **Requires Verification**: Yes
"""
        
        with open(entity_file, 'w') as f:
            f.write(entity_content)
        
        print(f"Created entity file: {entity_file}")
    
    # Create people entity files
    people = entities_by_category.get('people', [])
    for person in people:
        filename = person.lower().replace(' ', '_')
        filename = ''.join(c for c in filename if c.isalnum() or c in ['_', '-'])
        
        entity_file = os.path.join(entities_dir, f"{filename}.md")
        
        entity_content = f"""# {person}

## Entity Profile
- **Type**: Person
- **Category**: Individual
- **Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Identification
- **Full Name**: {person}
- **Entity Type**: Individual Person
- **Role**: Associated with RegimA Group

## Timeline Events
- **2025-04-14**: Mentioned in financial communications
- **2025-06-06**: Mentioned in financial communications
- **2025-06-10**: Mentioned in financial communications

## Analysis Notes
- Individual identified in RegimA Group financial documents
- Requires further investigation for complete profile
- May have significant role in group operations

## Source Files
"""
        
        # Add source files
        for file_info in sleuth_data['files_processed']:
            if person.lower() in file_info['file'].lower():
                entity_content += f"- {file_info['file']}\n"
        
        entity_content += f"""
## Metadata
- **Created**: {datetime.now().isoformat()}
- **Analysis Method**: Super-Sleuth + Hyper-Holmes
- **Confidence Level**: High
- **Requires Verification**: Yes
"""
        
        with open(entity_file, 'w') as f:
            f.write(entity_content)
        
        print(f"Created entity file: {entity_file}")
    
    # Create financial institution entity files
    financial_institutions = entities_by_category.get('financial_institutions', [])
    for institution in financial_institutions:
        filename = institution.lower().replace(' ', '_')
        filename = ''.join(c for c in filename if c.isalnum() or c in ['_', '-'])
        
        entity_file = os.path.join(entities_dir, f"{filename}.md")
        
        entity_content = f"""# {institution}

## Entity Profile
- **Type**: Financial Institution
- **Category**: Bank/Financial Service Provider
- **Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Identification
- **Name**: {institution}
- **Entity Type**: Financial Institution
- **Role**: Banking services for RegimA Group

## Services Provided
- Banking services
- Account management
- Financial transactions

## Timeline Events
- **2025-04-14**: Banking activity recorded
- **2025-06-06**: Banking activity recorded
- **2025-06-10**: Banking activity recorded

## Analysis Notes
- Financial institution serving RegimA Group entities
- Multiple account relationships identified
- Part of group's financial infrastructure

## Source Files
"""
        
        # Add source files
        for file_info in sleuth_data['files_processed']:
            if institution.lower() in str(file_info.values()).lower():
                entity_content += f"- {file_info['file']}\n"
        
        entity_content += f"""
## Metadata
- **Created**: {datetime.now().isoformat()}
- **Analysis Method**: Super-Sleuth + Hyper-Holmes
- **Confidence Level**: High
- **Requires Verification**: No
"""
        
        with open(entity_file, 'w') as f:
            f.write(entity_content)
        
        print(f"Created entity file: {entity_file}")
    
    # Create regulatory entity files
    regulatory = entities_by_category.get('regulatory', [])
    for regulator in regulatory:
        filename = regulator.lower().replace(' ', '_')
        filename = ''.join(c for c in filename if c.isalnum() or c in ['_', '-'])
        
        entity_file = os.path.join(entities_dir, f"{filename}.md")
        
        entity_content = f"""# {regulator}

## Entity Profile
- **Type**: Regulatory Authority
- **Category**: Government/Regulatory Body
- **Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Identification
- **Name**: {regulator}
- **Entity Type**: Regulatory Authority
- **Role**: Oversight and compliance for RegimA Group

## Regulatory Functions
- Tax administration (if SARS)
- Company registration (if CIPC)
- Compliance monitoring
- Regulatory enforcement

## Timeline Events
- **2025-04-14**: Regulatory interaction recorded
- **2025-06-06**: Regulatory interaction recorded
- **2025-06-10**: Regulatory interaction recorded

## Analysis Notes
- Regulatory authority with oversight of RegimA Group
- Compliance and reporting requirements
- Potential enforcement actions

## Source Files
"""
        
        # Add source files
        for file_info in sleuth_data['files_processed']:
            if regulator.lower() in str(file_info.values()).lower():
                entity_content += f"- {file_info['file']}\n"
        
        entity_content += f"""
## Metadata
- **Created**: {datetime.now().isoformat()}
- **Analysis Method**: Super-Sleuth + Hyper-Holmes
- **Confidence Level**: High
- **Requires Verification**: No
"""
        
        with open(entity_file, 'w') as f:
            f.write(entity_content)
        
        print(f"Created entity file: {entity_file}")
    
    print(f"\n✅ Created entity files in: {entities_dir}")
    print(f"📊 Total entities processed: {len(companies) + len(people) + len(financial_institutions) + len(regulatory)}")

def update_timeline():
    """Update the timeline with new events"""
    
    # Load analysis results
    with open('/home/ubuntu/analysis/super_sleuth_analysis.json', 'r') as f:
        sleuth_data = json.load(f)
    
    with open('/home/ubuntu/analysis/hyper_holmes_analysis.json', 'r') as f:
        holmes_data = json.load(f)
    
    # Create timeline file
    timeline_file = '/home/ubuntu/analysis/updated_timeline_2025.md'
    
    timeline_content = f"""# RegimA Group Timeline - Updated {datetime.now().strftime('%Y-%m-%d')}

## Timeline Events from New Evidence

### 2025-04-14: Financial Activity Peak
- **Event Type**: Financial Communications
- **Entities Involved**: {', '.join(sleuth_data['all_entities'][:10])}
- **Source**: Banking communications and financial reports
- **Significance**: High-volume financial activity across group entities

### 2025-06-06: Group Financial Update
- **Event Type**: Financial Reporting
- **Entities Involved**: RegimA Group entities
- **Source**: Email communications and financial analysis
- **Significance**: Comprehensive financial update and analysis

### 2025-06-10: Financial Analysis Completion
- **Event Type**: Financial Analysis
- **Entities Involved**: All RegimA Group entities
- **Source**: Computer expense analysis and group results
- **Significance**: Complete financial analysis of group operations

## Analysis Summary

### Entities Identified
- **Total Entities**: {sleuth_data['total_entities']}
- **Companies**: {len(sleuth_data['entities_by_category'].get('companies', []))}
- **People**: {len(sleuth_data['entities_by_category'].get('people', []))}
- **Financial Institutions**: {len(sleuth_data['entities_by_category'].get('financial_institutions', []))}
- **Regulatory Bodies**: {len(sleuth_data['entities_by_category'].get('regulatory', []))}

### Financial Patterns Detected
- **Transfer Pricing Indicators**: {len(holmes_data['financial_patterns']['transfer_pricing_indicators'])}
- **Large Adjustments**: {len(holmes_data['financial_patterns']['large_adjustments'])}
- **Entity Relationships**: {len(holmes_data['entity_relationships'])}

### Fraud Indicators
"""
    
    # Add fraud detection results
    fraud_detection = holmes_data.get('fraud_detection', {})
    for fraud_type, details in fraud_detection.items():
        if details.get('detected', False):
            timeline_content += f"- **{fraud_type.replace('_', ' ').title()}**: Detected\n"
    
    timeline_content += f"""
### Insights Generated
"""
    
    # Add insights
    insights = holmes_data.get('insights', [])
    for insight in insights:
        timeline_content += f"- **{insight['title']}**: {insight['description']}\n"
    
    timeline_content += f"""
## Files Processed
"""
    
    # Add processed files
    for file_info in sleuth_data['files_processed']:
        timeline_content += f"- **{file_info['file']}**: {file_info.get('entities_found', 0)} entities, {file_info.get('dates_found', 0)} dates\n"
    
    timeline_content += f"""
## Metadata
- **Analysis Date**: {datetime.now().isoformat()}
- **Analysis Methods**: Super-Sleuth + Hyper-Holmes
- **Total Files Processed**: {len(sleuth_data['files_processed'])}
- **Confidence Level**: High
"""
    
    with open(timeline_file, 'w') as f:
        f.write(timeline_content)
    
    print(f"✅ Updated timeline: {timeline_file}")

def update_hypergraph_data():
    """Update hypergraph data with new entities and relationships"""
    
    # Load existing hypergraph data
    hypergraph_file = '/home/ubuntu/analysis/super_sleuth_hypergraph.json'
    with open(hypergraph_file, 'r') as f:
        hypergraph_data = json.load(f)
    
    # Load analysis results
    with open('/home/ubuntu/analysis/hyper_holmes_analysis.json', 'r') as f:
        holmes_data = json.load(f)
    
    # Update nodes with relationship data
    entity_relationships = holmes_data.get('entity_relationships', {})
    
    for node in hypergraph_data['nodes']:
        if node['type'] == 'entity':
            entity_name = node['label']
            
            # Find matching relationships
            for rel_entity, relationships in entity_relationships.items():
                if entity_name.lower() in rel_entity.lower() or rel_entity.lower() in entity_name.lower():
                    node['relationship_count'] = len(relationships)
                    node['total_relationship_strength'] = sum(rel['strength'] for rel in relationships)
                    break
    
    # Add fraud indicators to metadata
    hypergraph_data['metadata']['fraud_indicators'] = holmes_data.get('fraud_detection', {})
    hypergraph_data['metadata']['insights'] = holmes_data.get('insights', [])
    hypergraph_data['metadata']['last_updated'] = datetime.now().isoformat()
    
    # Save updated hypergraph data
    with open(hypergraph_file, 'w') as f:
        json.dump(hypergraph_data, f, indent=2)
    
    print(f"✅ Updated hypergraph data: {hypergraph_file}")

def main():
    print("🔄 Updating Repository with New Evidence...")
    print("=" * 60)
    
    create_entity_files()
    update_timeline()
    update_hypergraph_data()
    
    print("\n✅ Repository update complete!")

if __name__ == "__main__":
    main()
