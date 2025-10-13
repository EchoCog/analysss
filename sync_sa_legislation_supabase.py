#!/usr/bin/env python3

"""
Synchronize South African AI legislation compliance data with Supabase database.
"""

import json
import os
from supabase import create_client, Client

def load_sa_legislation_data():
    """Load the SA AI legislation compliance data."""
    with open('evidence/sa_ai_legislation_compliance/entities_and_timeline.json', 'r') as f:
        return json.load(f)

def sync_legislation_data(supabase: Client, data):
    """Sync legislation data to Supabase."""
    legislation_data = []
    
    # Extract legislation from entities
    if 'entities' in data and 'legislation' in data['entities']:
        for legislation in data['entities']['legislation']:
            legislation_record = {
                'name': legislation.get('name'),
                'full_name': legislation.get('full_name'),
                'year': legislation.get('year'),
                'type': legislation.get('type'),
                'significance': legislation.get('significance'),
                'key_requirements': legislation.get('key_requirements', [])
            }
            legislation_data.append(legislation_record)
    
    # Insert legislation data
    if legislation_data:
        try:
            result = supabase.table('sa_legislation').upsert(legislation_data).execute()
            print(f"✅ Synced {len(legislation_data)} legislation records to Supabase")
        except Exception as e:
            print(f"❌ Error syncing legislation data: {e}")

def sync_compliance_deadlines(supabase: Client, data):
    """Sync compliance deadlines to Supabase."""
    deadline_data = []
    
    # Extract compliance deadlines from timeline
    if 'timeline' in data and 'compliance_deadlines' in data['timeline']:
        for deadline in data['timeline']['compliance_deadlines']:
            deadline_record = {
                'requirement': deadline.get('requirement'),
                'timeframe': deadline.get('timeframe'),
                'legislation': deadline.get('legislation'),
                'severity': deadline.get('severity')
            }
            deadline_data.append(deadline_record)
    
    # Insert deadline data
    if deadline_data:
        try:
            result = supabase.table('compliance_deadlines').upsert(deadline_data).execute()
            print(f"✅ Synced {len(deadline_data)} compliance deadlines to Supabase")
        except Exception as e:
            print(f"❌ Error syncing compliance deadlines: {e}")

def sync_ai_fraud_threats(supabase: Client, data):
    """Sync AI fraud threats to Supabase."""
    threat_data = []
    
    # Extract AI fraud threats from entities
    if 'entities' in data and 'threats' in data['entities']:
        for threat in data['entities']['threats']:
            threat_record = {
                'threat_name': threat.get('name'),
                'threat_type': threat.get('type'),
                'description': threat.get('description'),
                'severity': threat.get('severity'),
                'legal_implications': threat.get('legal_implications', [])
            }
            threat_data.append(threat_record)
    
    # Insert threat data
    if threat_data:
        try:
            result = supabase.table('ai_fraud_threats').upsert(threat_data).execute()
            print(f"✅ Synced {len(threat_data)} AI fraud threats to Supabase")
        except Exception as e:
            print(f"❌ Error syncing AI fraud threats: {e}")

def main():
    """Main synchronization function."""
    # Get Supabase credentials from environment variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Error: SUPABASE_URL and SUPABASE_KEY environment variables must be set")
        return
    
    # Create Supabase client
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # Load SA legislation data
    try:
        data = load_sa_legislation_data()
        print("📊 Loaded SA AI legislation compliance data")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Sync data to Supabase
    print("🔄 Starting Supabase synchronization...")
    sync_legislation_data(supabase, data)
    sync_compliance_deadlines(supabase, data)
    sync_ai_fraud_threats(supabase, data)
    print("✅ Supabase synchronization complete")

if __name__ == '__main__':
    main()
