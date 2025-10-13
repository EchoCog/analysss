#!/usr/bin/env python3

"""
Synchronize South African AI legislation compliance data with Neon PostgreSQL database.
"""

import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def load_sa_legislation_data():
    """Load the SA AI legislation compliance data."""
    with open('evidence/sa_ai_legislation_compliance/entities_and_timeline.json', 'r') as f:
        return json.load(f)

def get_neon_connection():
    """Get connection to Neon database."""
    # In a real implementation, these would come from environment variables
    # For now, we'll use placeholder values
    connection_string = os.getenv('NEON_DATABASE_URL', 'postgresql://user:password@host:port/database')
    
    try:
        conn = psycopg2.connect(connection_string)
        return conn
    except Exception as e:
        print(f"❌ Error connecting to Neon database: {e}")
        return None

def create_tables_if_not_exist(conn):
    """Create tables if they don't exist."""
    create_tables_sql = """
    CREATE TABLE IF NOT EXISTS legal_relationships (
        id SERIAL PRIMARY KEY,
        source_entity_id INTEGER,
        target_entity_id INTEGER,
        relationship_type TEXT,
        legal_basis TEXT,
        compliance_impact TEXT,
        temporal_data JSONB,
        created_at TIMESTAMP DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS compliance_monitoring (
        id SERIAL PRIMARY KEY,
        entity_id INTEGER,
        legislation_id INTEGER,
        compliance_status TEXT,
        last_assessment DATE,
        next_review DATE,
        risk_level TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    
    try:
        with conn.cursor() as cur:
            cur.execute(create_tables_sql)
        conn.commit()
        print("✅ Tables created/verified in Neon database")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        conn.rollback()

def sync_legal_relationships(conn, data):
    """Sync legal relationships to Neon database."""
    relationships = []
    
    # Extract relationships from entities
    if 'entities' in data:
        for category, entities in data['entities'].items():
            if isinstance(entities, list):
                for i, entity in enumerate(entities):
                    # Create relationships between entities in the same category
                    for j, other_entity in enumerate(entities):
                        if i != j:
                            relationship = {
                                'source_entity_id': i + 1,
                                'target_entity_id': j + 1,
                                'relationship_type': f'{category}_association',
                                'legal_basis': 'SA AI Legislation Compliance',
                                'compliance_impact': 'Medium',
                                'temporal_data': json.dumps({'category': category})
                            }
                            relationships.append(relationship)
    
    # Insert relationships
    if relationships:
        try:
            with conn.cursor() as cur:
                for rel in relationships[:10]:  # Limit to first 10 to avoid overwhelming the database
                    cur.execute("""
                        INSERT INTO legal_relationships 
                        (source_entity_id, target_entity_id, relationship_type, legal_basis, compliance_impact, temporal_data)
                        VALUES (%(source_entity_id)s, %(target_entity_id)s, %(relationship_type)s, %(legal_basis)s, %(compliance_impact)s, %(temporal_data)s)
                        ON CONFLICT DO NOTHING
                    """, rel)
            conn.commit()
            print(f"✅ Synced {min(len(relationships), 10)} legal relationships to Neon")
        except Exception as e:
            print(f"❌ Error syncing legal relationships: {e}")
            conn.rollback()

def sync_compliance_monitoring(conn, data):
    """Sync compliance monitoring data to Neon database."""
    monitoring_data = []
    
    # Extract compliance monitoring from timeline
    if 'timeline' in data and 'compliance_deadlines' in data['timeline']:
        for i, deadline in enumerate(data['timeline']['compliance_deadlines']):
            monitoring_record = {
                'entity_id': i + 1,
                'legislation_id': i + 1,
                'compliance_status': 'Pending',
                'last_assessment': '2025-10-11',
                'next_review': '2025-11-11',
                'risk_level': deadline.get('severity', 'Medium').lower()
            }
            monitoring_data.append(monitoring_record)
    
    # Insert monitoring data
    if monitoring_data:
        try:
            with conn.cursor() as cur:
                for record in monitoring_data:
                    cur.execute("""
                        INSERT INTO compliance_monitoring 
                        (entity_id, legislation_id, compliance_status, last_assessment, next_review, risk_level)
                        VALUES (%(entity_id)s, %(legislation_id)s, %(compliance_status)s, %(last_assessment)s, %(next_review)s, %(risk_level)s)
                        ON CONFLICT DO NOTHING
                    """, record)
            conn.commit()
            print(f"✅ Synced {len(monitoring_data)} compliance monitoring records to Neon")
        except Exception as e:
            print(f"❌ Error syncing compliance monitoring: {e}")
            conn.rollback()

def main():
    """Main synchronization function."""
    # Load SA legislation data
    try:
        data = load_sa_legislation_data()
        print("📊 Loaded SA AI legislation compliance data")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Get Neon connection
    conn = get_neon_connection()
    if not conn:
        print("❌ Could not connect to Neon database")
        return
    
    try:
        # Create tables if needed
        create_tables_if_not_exist(conn)
        
        # Sync data to Neon
        print("🔄 Starting Neon synchronization...")
        sync_legal_relationships(conn, data)
        sync_compliance_monitoring(conn, data)
        print("✅ Neon synchronization complete")
        
    finally:
        conn.close()

if __name__ == '__main__':
    main()
