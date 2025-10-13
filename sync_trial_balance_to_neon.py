#!/usr/bin/env python3
"""
Synchronize trial balance analysis data with Neon database.
This script updates the database with new entities, events, and evidence from the trial balance analysis.
"""

import json
import subprocess
from datetime import datetime

def run_mcp_command(tool_name, params):
    """Execute MCP command and return result."""
    cmd = [
        'manus-mcp-cli', 'tool', 'call', tool_name,
        '--server', 'neon',
        '--input', json.dumps({"params": params})
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing {tool_name}: {result.stderr}")
        return None
    
    return result.stdout

def sync_entities():
    """Sync entity data from trial balance analysis."""
    print("🔄 Syncing entities to Neon database...")
    
    # Load the financial model data
    with open('/home/ubuntu/analysis/models/regima_group_financial_model_2020.json', 'r') as f:
        model_data = json.load(f)
    
    entities_to_sync = []
    
    for entity_code, entity_data in model_data['entities'].items():
        entity_record = {
            'entity_code': entity_code,
            'full_name': entity_data['full_name'],
            'entity_type': entity_data['entity_type'],
            'financial_year_end': entity_data['financial_year_end'],
            'strategic_role': entity_data['strategic_role'],
            'metadata': json.dumps({
                'ownership_structure': entity_data.get('ownership_structure', {}),
                'key_personnel': entity_data.get('key_personnel', {}),
                'financial_metrics_2020': entity_data.get('financial_metrics_2020', {})
            })
        }
        entities_to_sync.append(entity_record)
    
    # Insert entities into database
    for entity in entities_to_sync:
        sql = f"""
        INSERT INTO entities (entity_code, full_name, entity_type, financial_year_end, strategic_role, metadata, updated_at)
        VALUES ('{entity['entity_code']}', '{entity['full_name']}', '{entity['entity_type']}', 
                '{entity['financial_year_end']}', '{entity['strategic_role']}', 
                '{entity['metadata']}', NOW())
        ON CONFLICT (entity_code) 
        DO UPDATE SET 
            full_name = EXCLUDED.full_name,
            entity_type = EXCLUDED.entity_type,
            financial_year_end = EXCLUDED.financial_year_end,
            strategic_role = EXCLUDED.strategic_role,
            metadata = EXCLUDED.metadata,
            updated_at = NOW();
        """
        
        result = run_mcp_command('run_sql', {
            'projectId': 'sweet-sea-69912135',
            'sql': sql
        })
        
        if result:
            print(f"  ✅ Synced entity: {entity['entity_code']}")
        else:
            print(f"  ❌ Failed to sync entity: {entity['entity_code']}")

def sync_events():
    """Sync timeline events from trial balance analysis."""
    print("🔄 Syncing events to Neon database...")
    
    # Load the comprehensive timeline
    with open('/home/ubuntu/analysis/comprehensive_trial_balance_analysis.json', 'r') as f:
        analysis_data = json.load(f)
    
    events_to_sync = []
    
    for event in analysis_data['consolidated_timeline']:
        event_record = {
            'event_date': event['date'],
            'event_description': event['event'],
            'entities_involved': json.dumps(event['entities']),
            'significance': event['significance'],
            'event_type': 'financial_manipulation',
            'source': 'trial_balance_2020'
        }
        events_to_sync.append(event_record)
    
    # Insert events into database
    for event in events_to_sync:
        sql = f"""
        INSERT INTO events (event_date, event_description, entities_involved, significance, event_type, source, created_at)
        VALUES ('{event['event_date']}', '{event['event_description'].replace("'", "''")}', 
                '{event['entities_involved']}', '{event['significance'].replace("'", "''")}',
                '{event['event_type']}', '{event['source']}', NOW())
        ON CONFLICT (event_date, event_description) 
        DO UPDATE SET 
            entities_involved = EXCLUDED.entities_involved,
            significance = EXCLUDED.significance,
            event_type = EXCLUDED.event_type,
            source = EXCLUDED.source,
            updated_at = NOW();
        """
        
        result = run_mcp_command('run_sql', {
            'projectId': 'sweet-sea-69912135',
            'sql': sql
        })
        
        if result:
            print(f"  ✅ Synced event: {event['event_date']}")
        else:
            print(f"  ❌ Failed to sync event: {event['event_date']}")

def sync_evidence():
    """Sync evidence records from trial balance analysis."""
    print("🔄 Syncing evidence to Neon database...")
    
    evidence_records = [
        {
            'evidence_id': 'TB_2020_REG',
            'evidence_type': 'financial_statement',
            'file_path': 'evidence/trial_balances_2020/REG-TRIALBALANCE.xlsx',
            'description': 'RegimA Skin Treatments Trial Balance 2020',
            'date_created': '2020-02-28',
            'entities_involved': json.dumps(['RST']),
            'significance_score': 9,
            'metadata': json.dumps({
                'entity': 'RegimA Skin Treatments',
                'period': '01/03/19 to 29/02/20',
                'key_figures': {
                    'sales': 21822058.61,
                    'cost_of_sales': 8206221.57,
                    'directors_fees': 2400000.00
                }
            })
        },
        {
            'evidence_id': 'TB_2020_RWW',
            'evidence_type': 'financial_statement',
            'file_path': 'evidence/trial_balances_2020/WW-TrialBalanceFEB20.xlsx',
            'description': 'RegimA Worldwide Distribution Trial Balance 2020',
            'date_created': '2020-02-20',
            'entities_involved': json.dumps(['RWW']),
            'significance_score': 8,
            'metadata': json.dumps({
                'entity': 'RegimA Worldwide Distribution',
                'period': 'Trial Balance FEB20',
                'key_figures': {
                    'sales': 7440828.33,
                    'cost_of_sales': 5622740.58,
                    'admin_fees_reallocated': 810097.70
                }
            })
        },
        {
            'evidence_id': 'TB_2020_SLG',
            'evidence_type': 'financial_statement',
            'file_path': 'evidence/trial_balances_2020/SL-TRIALBALANCE2020.xlsx',
            'description': 'Strategic Logistics Trial Balance 2020',
            'date_created': '2020-02-29',
            'entities_involved': json.dumps(['SLG']),
            'significance_score': 10,
            'metadata': json.dumps({
                'entity': 'Strategic Logistics',
                'period': '01/03/19 to 29/02/20',
                'key_figures': {
                    'sales': 14900286.76,
                    'cost_of_sales': 13578642.35,
                    'regima_loan_account': 12971390.13
                }
            })
        },
        {
            'evidence_id': 'TB_2020_VV',
            'evidence_type': 'financial_statement',
            'file_path': 'evidence/trial_balances_2020/VV-TRIALBALANCEAPR20202.xlsx',
            'description': 'Villa Via Trial Balance 2020',
            'date_created': '2020-04-30',
            'entities_involved': json.dumps(['VV']),
            'significance_score': 7,
            'metadata': json.dumps({
                'entity': 'Villa Via',
                'period': '01/05/19 to 30/04/20',
                'key_figures': {
                    'monthly_rental_income': 4384701.36,
                    'net_profit': 3727475.50,
                    'members_loan_account': 22806538.74
                }
            })
        },
        {
            'evidence_id': 'EMAIL_2020_DANIE',
            'evidence_type': 'communication',
            'file_path': 'evidence/trial_balances_2020/email-body.html',
            'description': 'Email from Danie Bantjes with final trial balances',
            'date_created': '2020-08-13',
            'entities_involved': json.dumps(['RST', 'RWW', 'SLG', 'VV']),
            'significance_score': 8,
            'metadata': json.dumps({
                'from': 'Danie Bantjes <danie.bantjes@gmail.com>',
                'subject': 'Final TB\'s',
                'recipients': [
                    'Bernadine Wright <bern@regima.zone>',
                    'Jacqui Faucitt <jax@regima.zone>',
                    'Peter Andrew Faucitt <pete@regima.com>',
                    'Rynette Farrar <rynette@regima.zone>',
                    'Daniel Faucitt <d@rzo.io>'
                ]
            })
        }
    ]
    
    # Insert evidence into database
    for evidence in evidence_records:
        sql = f"""
        INSERT INTO evidence (evidence_id, evidence_type, file_path, description, date_created, 
                            entities_involved, significance_score, metadata, created_at)
        VALUES ('{evidence['evidence_id']}', '{evidence['evidence_type']}', '{evidence['file_path']}',
                '{evidence['description'].replace("'", "''")}', '{evidence['date_created']}',
                '{evidence['entities_involved']}', {evidence['significance_score']},
                '{evidence['metadata']}', NOW())
        ON CONFLICT (evidence_id) 
        DO UPDATE SET 
            evidence_type = EXCLUDED.evidence_type,
            file_path = EXCLUDED.file_path,
            description = EXCLUDED.description,
            date_created = EXCLUDED.date_created,
            entities_involved = EXCLUDED.entities_involved,
            significance_score = EXCLUDED.significance_score,
            metadata = EXCLUDED.metadata,
            updated_at = NOW();
        """
        
        result = run_mcp_command('run_sql', {
            'projectId': 'sweet-sea-69912135',
            'sql': sql
        })
        
        if result:
            print(f"  ✅ Synced evidence: {evidence['evidence_id']}")
        else:
            print(f"  ❌ Failed to sync evidence: {evidence['evidence_id']}")

def sync_relationships():
    """Sync inter-company relationships from trial balance analysis."""
    print("🔄 Syncing relationships to Neon database...")
    
    # Load the financial model data
    with open('/home/ubuntu/analysis/models/regima_group_financial_model_2020.json', 'r') as f:
        model_data = json.load(f)
    
    relationships_to_sync = [
        {
            'from_entity': 'SLG',
            'to_entity': 'RST',
            'relationship_type': 'debt',
            'amount': 12971390.13,
            'description': 'Massive inter-company loan creating artificial dependency',
            'date_established': '2020-02-28'
        },
        {
            'from_entity': 'RST',
            'to_entity': 'RWW',
            'relationship_type': 'loan',
            'amount': 750000.00,
            'description': 'Production cost allocation loan',
            'date_established': '2020-02-28'
        },
        {
            'from_entity': 'VV',
            'to_entity': 'SLG',
            'relationship_type': 'loan',
            'amount': 600000.00,
            'description': 'Additional debt burden on SLG',
            'date_established': '2020-04-30'
        }
    ]
    
    # Insert relationships into database
    for rel in relationships_to_sync:
        sql = f"""
        INSERT INTO relationships (from_entity, to_entity, relationship_type, amount, description, 
                                 date_established, created_at)
        VALUES ('{rel['from_entity']}', '{rel['to_entity']}', '{rel['relationship_type']}',
                {rel['amount']}, '{rel['description'].replace("'", "''")}', 
                '{rel['date_established']}', NOW())
        ON CONFLICT (from_entity, to_entity, relationship_type) 
        DO UPDATE SET 
            amount = EXCLUDED.amount,
            description = EXCLUDED.description,
            date_established = EXCLUDED.date_established,
            updated_at = NOW();
        """
        
        result = run_mcp_command('run_sql', {
            'projectId': 'sweet-sea-69912135',
            'sql': sql
        })
        
        if result:
            print(f"  ✅ Synced relationship: {rel['from_entity']} -> {rel['to_entity']}")
        else:
            print(f"  ❌ Failed to sync relationship: {rel['from_entity']} -> {rel['to_entity']}")

def main():
    """Main synchronization function."""
    print("🚀 STARTING NEON DATABASE SYNCHRONIZATION")
    print("=" * 60)
    
    try:
        sync_entities()
        sync_events()
        sync_evidence()
        sync_relationships()
        
        print("\n✅ DATABASE SYNCHRONIZATION COMPLETE")
        print("All trial balance data has been synchronized with Neon database.")
        
    except Exception as e:
        print(f"\n❌ SYNCHRONIZATION FAILED: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
