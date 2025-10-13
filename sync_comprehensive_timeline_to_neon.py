#!/usr/bin/env python3
"""
Sync Comprehensive Timeline (2017-2025) to Neon Database
Processes timeline events and creates entity relationships for hypergraph analysis
"""

import os
import json
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values

# Database connection from environment
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(DATABASE_URL)

def create_timeline_tables(conn):
    """Create or update timeline tables in Neon"""
    with conn.cursor() as cur:
        # Add new columns to existing timeline_events table if they don't exist
        new_columns = [
            ("event_title", "TEXT"),
            ("phase", "TEXT"),
            ("phase_number", "INTEGER"),
            ("evidence_source", "TEXT"),
            ("evidence_location", "TEXT"),
            ("is_critical", "BOOLEAN DEFAULT FALSE"),
            ("updated_at", "TIMESTAMP DEFAULT NOW()")
        ]
        
        for column_name, column_type in new_columns:
            try:
                cur.execute(f"""
                    ALTER TABLE timeline_events 
                    ADD COLUMN IF NOT EXISTS {column_name} {column_type};
                """)
            except Exception as e:
                print(f"Note: Column {column_name} may already exist: {e}")
        
        # Timeline entities table (for entity involvement in events)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS timeline_event_entities (
                id SERIAL PRIMARY KEY,
                event_id INTEGER REFERENCES timeline_events(id) ON DELETE CASCADE,
                entity_name TEXT NOT NULL,
                entity_type TEXT,
                role_in_event TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # Timeline transactions table (for financial transactions in events)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS timeline_event_transactions (
                id SERIAL PRIMARY KEY,
                event_id INTEGER REFERENCES timeline_events(id) ON DELETE CASCADE,
                transaction_description TEXT NOT NULL,
                amount_zar DECIMAL(15,2),
                from_entity TEXT,
                to_entity TEXT,
                transaction_type TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # Create indexes
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_timeline_events_date 
            ON timeline_events(date);
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_timeline_events_phase 
            ON timeline_events(phase_number);
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_timeline_event_entities_entity 
            ON timeline_event_entities(entity_name);
        """)
        
        conn.commit()
        print("✓ Timeline tables created/updated")

def insert_timeline_events(conn):
    """Insert comprehensive timeline events"""
    
    timeline_events = [
        # Phase 1: Financial Structure Establishment (2019-2020)
        {
            'date': '2019-03-01',
            'title': 'Financial year commencement for RST and SLG',
            'description': 'Beginning of the period covered by the trial balance evidence',
            'significance': 'Establishes the baseline for inter-company financial manipulation',
            'phase': 'Financial Structure Establishment',
            'phase_number': 1,
            'evidence_source': 'Trial balance documentation',
            'evidence_location': 'case_2025_137857/02_evidence/evidence_package_20251012/',
            'is_critical': False,
            'entities': [
                {'name': 'RegimA Skin Treatments', 'type': 'Company', 'role': 'Financial year start'},
                {'name': 'Strategic Logistics', 'type': 'Company', 'role': 'Financial year start'}
            ],
            'transactions': []
        },
        {
            'date': '2019-05-01',
            'title': 'Financial year commencement for Villa Via',
            'description': 'Villa Via operates on different financial year, creating complexity in group reporting',
            'significance': 'Different financial year creates reporting complexity and manipulation opportunities',
            'phase': 'Financial Structure Establishment',
            'phase_number': 1,
            'evidence_source': 'VV-TRIALBALANCEAPR20202.xlsx',
            'evidence_location': 'case_2025_137857/02_evidence/financial/',
            'is_critical': False,
            'entities': [
                {'name': 'Villa Via', 'type': 'Company', 'role': 'Financial year start'}
            ],
            'transactions': []
        },
        {
            'date': '2020-02-20',
            'title': 'Multiple adjusting journal entries across entities',
            'description': 'Significant inter-company cost reallocations and adjustments',
            'significance': 'Evidence of systematic cost manipulation across group entities',
            'phase': 'Financial Structure Establishment',
            'phase_number': 1,
            'evidence_source': 'Trial balance AJEs',
            'evidence_location': 'case_2025_137857/02_evidence/financial/',
            'is_critical': True,
            'entities': [
                {'name': 'RegimA Worldwide', 'type': 'Company', 'role': 'Cost dumping ground'},
                {'name': 'Strategic Logistics', 'type': 'Company', 'role': 'Cost reallocation'},
                {'name': 'RegimA Skin Treatments', 'type': 'Company', 'role': 'Cost recipient'}
            ],
            'transactions': [
                {'description': 'Stock provision write-back', 'amount': 500000, 'from_entity': 'RWW', 'to_entity': None, 'type': 'Adjustment'},
                {'description': 'Admin fee reallocation to production costs', 'amount': 810000, 'from_entity': 'RWW', 'to_entity': None, 'type': 'Reallocation'},
                {'description': 'Admin fee reallocation to production costs', 'amount': 252000, 'from_entity': 'SLG', 'to_entity': None, 'type': 'Reallocation'},
                {'description': 'Production cost transfer', 'amount': 80000, 'from_entity': 'SLG', 'to_entity': 'RST', 'type': 'Transfer'}
            ]
        },
        {
            'date': '2020-02-28',
            'title': 'Year-end adjustments and inter-company interest payment',
            'description': 'Final adjustments including critical R414K interest payment from SLG to RST',
            'significance': 'Demonstrates profit concentration in RST at expense of SLG',
            'phase': 'Financial Structure Establishment',
            'phase_number': 1,
            'evidence_source': 'REG-TRIALBALANCE.xlsx, SL-TRIALBALANCE2020.xlsx',
            'evidence_location': 'case_2025_137857/02_evidence/financial/',
            'is_critical': True,
            'entities': [
                {'name': 'Strategic Logistics', 'type': 'Company', 'role': 'Interest payer'},
                {'name': 'RegimA Skin Treatments', 'type': 'Company', 'role': 'Interest receiver'},
                {'name': 'RegimA Worldwide', 'type': 'Company', 'role': 'Loan recipient'}
            ],
            'transactions': [
                {'description': 'Interest payment per loan agreement', 'amount': 414334.09, 'from_entity': 'SLG', 'to_entity': 'RST', 'type': 'Interest'},
                {'description': 'Loan for production costs', 'amount': 750000, 'from_entity': 'RST', 'to_entity': 'RWW', 'type': 'Loan'},
                {'description': 'Directors fee adjustment', 'amount': 784000, 'from_entity': 'RST', 'to_entity': None, 'type': 'Adjustment'}
            ]
        },
        {
            'date': '2020-04-30',
            'title': 'Villa Via financial year-end',
            'description': 'Completion of Villa Via financial year showing R3.7M profit from rental income',
            'significance': 'Reveals capital extraction mechanism through rental income and members loan',
            'phase': 'Financial Structure Establishment',
            'phase_number': 1,
            'evidence_source': 'VV-TRIALBALANCEAPR20202.xlsx',
            'evidence_location': 'case_2025_137857/02_evidence/financial/',
            'is_critical': True,
            'entities': [
                {'name': 'Villa Via', 'type': 'Company', 'role': 'Rental income vehicle'}
            ],
            'transactions': [
                {'description': 'Monthly rental income', 'amount': 4400000, 'from_entity': None, 'to_entity': 'Villa Via', 'type': 'Revenue'},
                {'description': 'Net profit', 'amount': 3700000, 'from_entity': None, 'to_entity': 'Villa Via', 'type': 'Profit'},
                {'description': 'Members loan account', 'amount': 22800000, 'from_entity': 'Villa Via', 'to_entity': None, 'type': 'Capital Extraction'}
            ]
        },
        {
            'date': '2020-08-13',
            'title': 'Email from Danie Bantjes with final trial balances',
            'description': 'Preparation for financial statement finalization meeting with Bernadine Wright',
            'significance': 'Documents formal communication of manipulated financial structures',
            'phase': 'Financial Structure Establishment',
            'phase_number': 1,
            'evidence_source': 'Email-body.html',
            'evidence_location': 'case_2025_137857/02_evidence/evidence_package_20251012/email-body.html',
            'is_critical': False,
            'entities': [
                {'name': 'Danie Bantjes', 'type': 'Person', 'role': 'Accountant'},
                {'name': 'Bernadine Wright', 'type': 'Person', 'role': 'Recipient'},
                {'name': 'Jacqui Faucitt', 'type': 'Person', 'role': 'CC recipient'},
                {'name': 'Peter Andrew Faucitt', 'type': 'Person', 'role': 'CC recipient'},
                {'name': 'Rynette Farrar', 'type': 'Person', 'role': 'CC recipient'},
                {'name': 'Daniel Faucitt', 'type': 'Person', 'role': 'CC recipient'}
            ],
            'transactions': []
        },
        
        # Phase 2: Business Relationship Development (2017-2021)
        {
            'date': '2017-06-30',
            'title': 'First invoice to RegimA Skin Treatments',
            'description': 'First invoice to RegimA Skin Treatments for Google GSuite services (R250.80)',
            'significance': 'Beginning of business relationship between ReZonance and RegimA Group',
            'phase': 'Business Relationship Development',
            'phase_number': 2,
            'evidence_source': 'Invoice records',
            'evidence_location': 'case_2025_137857/02_evidence/financial/',
            'is_critical': False,
            'entities': [
                {'name': 'ReZonance', 'type': 'Company', 'role': 'Service provider'},
                {'name': 'RegimA Skin Treatments', 'type': 'Company', 'role': 'Client'}
            ],
            'transactions': [
                {'description': 'Google GSuite services', 'amount': 250.80, 'from_entity': 'RST', 'to_entity': 'ReZonance', 'type': 'Service Payment'}
            ]
        },
        {
            'date': '2017-09-30',
            'title': 'Major service expansion with multiple enterprise services',
            'description': 'Substantial increase in service provision and financial exposure (R100,000+)',
            'significance': 'Establishes significant financial dependency and trust relationship',
            'phase': 'Business Relationship Development',
            'phase_number': 2,
            'evidence_source': 'Invoice records',
            'evidence_location': 'case_2025_137857/02_evidence/financial/',
            'is_critical': False,
            'entities': [
                {'name': 'ReZonance', 'type': 'Company', 'role': 'Service provider'},
                {'name': 'RegimA Group', 'type': 'Group', 'role': 'Client'}
            ],
            'transactions': [
                {'description': 'Enterprise services', 'amount': 100000, 'from_entity': 'RegimA Group', 'to_entity': 'ReZonance', 'type': 'Service Payment'}
            ]
        },
        
        # Phase 3: Debt Accumulation and Manipulation (2022-2023)
        {
            'date': '2022-03-01',
            'title': 'Opening balance showing substantial accumulated debt',
            'description': 'Opening balance showing substantial accumulated debt (R971,587.93)',
            'significance': 'Evidence of systematic non-payment of legitimate debts',
            'phase': 'Debt Accumulation and Manipulation',
            'phase_number': 3,
            'evidence_source': 'Financial analysis reports',
            'evidence_location': 'case_2025_137857/02_evidence/financial/',
            'is_critical': True,
            'entities': [
                {'name': 'RegimA Group', 'type': 'Group', 'role': 'Debtor'},
                {'name': 'ReZonance', 'type': 'Company', 'role': 'Creditor'}
            ],
            'transactions': [
                {'description': 'Accumulated debt', 'amount': 971587.93, 'from_entity': 'RegimA Group', 'to_entity': 'ReZonance', 'type': 'Debt'}
            ]
        },
        {
            'date': '2022-07-11',
            'title': 'First structured payments begin',
            'description': 'First structured payments begin (R40,000)',
            'significance': 'Attempt to manage debt through partial payments',
            'phase': 'Debt Accumulation and Manipulation',
            'phase_number': 3,
            'evidence_source': 'Payment records',
            'evidence_location': 'case_2025_137857/02_evidence/financial/',
            'is_critical': False,
            'entities': [
                {'name': 'RegimA Group', 'type': 'Group', 'role': 'Payer'},
                {'name': 'ReZonance', 'type': 'Company', 'role': 'Payee'}
            ],
            'transactions': [
                {'description': 'Partial payment', 'amount': 40000, 'from_entity': 'RegimA Group', 'to_entity': 'ReZonance', 'type': 'Payment'}
            ]
        },
        {
            'date': '2023-02-28',
            'title': 'Final balance showing persistent debt despite payments',
            'description': 'Final balance showing persistent debt despite payments (R1,035,361.34)',
            'significance': 'Debt continues to grow despite payment claims',
            'phase': 'Debt Accumulation and Manipulation',
            'phase_number': 3,
            'evidence_source': 'Financial analysis reports',
            'evidence_location': 'case_2025_137857/02_evidence/financial/',
            'is_critical': True,
            'entities': [
                {'name': 'RegimA Group', 'type': 'Group', 'role': 'Debtor'},
                {'name': 'ReZonance', 'type': 'Company', 'role': 'Creditor'}
            ],
            'transactions': [
                {'description': 'Outstanding debt', 'amount': 1035361.34, 'from_entity': 'RegimA Group', 'to_entity': 'ReZonance', 'type': 'Debt'}
            ]
        },
        {
            'date': '2023-03-15',
            'title': 'RegimA claims payment not reflected in ReZonance records',
            'description': 'RegimA claims payment of R470,000 not reflected in ReZonance records',
            'significance': 'First documented false payment claim - beginning of fraud',
            'phase': 'Debt Accumulation and Manipulation',
            'phase_number': 3,
            'evidence_source': 'Payment dispute documentation',
            'evidence_location': 'case_2025_137857/02_evidence/financial/',
            'is_critical': True,
            'entities': [
                {'name': 'RegimA Group', 'type': 'Group', 'role': 'False claimant'},
                {'name': 'ReZonance', 'type': 'Company', 'role': 'Victim'}
            ],
            'transactions': [
                {'description': 'False payment claim', 'amount': 470000, 'from_entity': 'RegimA Group', 'to_entity': 'ReZonance', 'type': 'Fraudulent Claim'}
            ]
        },
        {
            'date': '2023-09-20',
            'title': 'Additional false payment claims',
            'description': 'Additional false payment claims totaling R765,361.34',
            'significance': 'Escalation of fraudulent payment claims',
            'phase': 'Debt Accumulation and Manipulation',
            'phase_number': 3,
            'evidence_source': 'Payment dispute documentation',
            'evidence_location': 'case_2025_137857/02_evidence/financial/',
            'is_critical': True,
            'entities': [
                {'name': 'RegimA Group', 'type': 'Group', 'role': 'False claimant'},
                {'name': 'ReZonance', 'type': 'Company', 'role': 'Victim'}
            ],
            'transactions': [
                {'description': 'False payment claims', 'amount': 765361.34, 'from_entity': 'RegimA Group', 'to_entity': 'ReZonance', 'type': 'Fraudulent Claim'}
            ]
        },
        
        # Phase 4: Fraud Discovery and Cover-up (2025)
        {
            'date': '2025-04-15',
            'title': 'Bank accounts redirected',
            'description': 'Bank accounts redirected (precursor to subsequent events)',
            'significance': 'Beginning of systematic control consolidation',
            'phase': 'Fraud Discovery and Cover-up',
            'phase_number': 4,
            'evidence_source': 'Banking records',
            'evidence_location': 'case_2025_137857/02_evidence/financial/',
            'is_critical': True,
            'entities': [
                {'name': 'RegimA Group', 'type': 'Group', 'role': 'Control consolidator'}
            ],
            'transactions': []
        },
        {
            'date': '2025-05-15',
            'title': 'Jax confronts Rynette about missing money',
            'description': 'Jax confronts Rynette about missing money, notifies that funds need to be paid to ReZonance & Kayla\'s estate',
            'significance': 'CRITICAL: Confrontation triggers coordinated cover-up activities',
            'phase': 'Fraud Discovery and Cover-up',
            'phase_number': 4,
            'evidence_source': 'Communication records',
            'evidence_location': 'case_2025_137857/02_evidence/emails/',
            'is_critical': True,
            'entities': [
                {'name': 'Jacqui Faucitt', 'type': 'Person', 'role': 'Fraud detector (RST CEO)'},
                {'name': 'Rynette Farrar', 'type': 'Person', 'role': 'Confronted party'},
                {'name': 'ReZonance', 'type': 'Company', 'role': 'Creditor'},
                {'name': 'Kayla Estate', 'type': 'Estate', 'role': 'Creditor'}
            ],
            'transactions': []
        },
        {
            'date': '2025-05-22',
            'title': 'Disappearance of all orders & audit trails from Shopify',
            'description': 'Systematic destruction of digital evidence (7 days after confrontation)',
            'significance': 'CRITICAL: Evidence destruction in response to Jax\'s confrontation',
            'phase': 'Fraud Discovery and Cover-up',
            'phase_number': 4,
            'evidence_source': 'Shopify audit trail analysis',
            'evidence_location': 'case_2025_137857/02_evidence/evidence_package_20250523/',
            'is_critical': True,
            'entities': [
                {'name': 'RegimA Group', 'type': 'Group', 'role': 'Evidence destroyer'}
            ],
            'transactions': []
        },
        {
            'date': '2025-05-29',
            'title': 'Adderory purchases domain regimaskin.co.za',
            'description': 'Digital infrastructure control consolidation (14 days after confrontation)',
            'significance': 'CRITICAL: Infrastructure control by Rynette\'s family member',
            'phase': 'Fraud Discovery and Cover-up',
            'phase_number': 4,
            'evidence_source': 'Domain registration records',
            'evidence_location': 'case_2025_137857/02_evidence/misc/',
            'is_critical': True,
            'entities': [
                {'name': 'Adderory', 'type': 'Person', 'role': 'Domain purchaser (Rynette\'s son)'},
                {'name': 'Rynette Farrar', 'type': 'Person', 'role': 'Beneficiary'},
                {'name': 'RegimA Group', 'type': 'Group', 'role': 'Target'}
            ],
            'transactions': []
        },
        {
            'date': '2025-06-07',
            'title': 'Cards cancelled secretly',
            'description': 'Financial control consolidation (23 days after confrontation)',
            'significance': 'CRITICAL: Financial control consolidation following confrontation',
            'phase': 'Fraud Discovery and Cover-up',
            'phase_number': 4,
            'evidence_source': 'Banking records',
            'evidence_location': 'case_2025_137857/02_evidence/financial/',
            'is_critical': True,
            'entities': [
                {'name': 'RegimA Group', 'type': 'Group', 'role': 'Control consolidator'}
            ],
            'transactions': []
        },
        {
            'date': '2025-07-02',
            'title': 'CIPC Warning - Annual return reminder for Unicorn Dynamics',
            'description': 'Regulatory compliance issues emerge',
            'significance': 'Regulatory pressure adds to fraud exposure',
            'phase': 'Fraud Discovery and Cover-up',
            'phase_number': 4,
            'evidence_source': 'CIPC correspondence',
            'evidence_location': 'case_2025_137857/02_evidence/misc/',
            'is_critical': False,
            'entities': [
                {'name': 'Unicorn Dynamics', 'type': 'Company', 'role': 'Non-compliant entity'},
                {'name': 'CIPC', 'type': 'Regulator', 'role': 'Compliance enforcer'}
            ],
            'transactions': []
        },
        {
            'date': '2025-07-07',
            'title': 'Daniel Faucitt clarifies company status and payment disputes',
            'description': 'Attempt to manage regulatory and financial disputes',
            'significance': 'Damage control attempt by CIO',
            'phase': 'Fraud Discovery and Cover-up',
            'phase_number': 4,
            'evidence_source': 'Email correspondence',
            'evidence_location': 'case_2025_137857/02_evidence/emails/',
            'is_critical': False,
            'entities': [
                {'name': 'Daniel Faucitt', 'type': 'Person', 'role': 'CIO (RWW)'}
            ],
            'transactions': []
        },
        {
            'date': '2025-10-09',
            'title': 'Payment fraud scheme discovered',
            'description': 'Payment fraud scheme discovered through financial analysis (R1,235,361.34)',
            'significance': 'Full extent of fraud documented and analyzed',
            'phase': 'Fraud Discovery and Cover-up',
            'phase_number': 4,
            'evidence_source': 'Comprehensive financial analysis',
            'evidence_location': 'case_2025_137857/03_analysis/',
            'is_critical': True,
            'entities': [
                {'name': 'RegimA Group', 'type': 'Group', 'role': 'Perpetrator'},
                {'name': 'ReZonance', 'type': 'Company', 'role': 'Victim'}
            ],
            'transactions': [
                {'description': 'Total fraud amount', 'amount': 1235361.34, 'from_entity': 'RegimA Group', 'to_entity': 'ReZonance', 'type': 'Fraud'}
            ]
        },
        {
            'date': '2025-10-12',
            'title': 'UK transaction evidence integrated',
            'description': 'UK transaction evidence integrated showing R11.9M extraction pattern',
            'significance': 'International dimension of financial extraction revealed',
            'phase': 'Fraud Discovery and Cover-up',
            'phase_number': 4,
            'evidence_source': 'UK transaction analysis',
            'evidence_location': 'case_2025_137857/02_evidence/evidence_package_20251012/uk_transaction_analysis.md',
            'is_critical': True,
            'entities': [
                {'name': 'RegimA UK', 'type': 'Company', 'role': 'Extraction vehicle'},
                {'name': 'Peter Faucitt', 'type': 'Person', 'role': 'Beneficiary'},
                {'name': 'Daniel Faucitt', 'type': 'Person', 'role': 'Beneficiary'}
            ],
            'transactions': [
                {'description': 'UK extraction pattern', 'amount': 11900000, 'from_entity': 'RegimA SA', 'to_entity': 'RegimA UK', 'type': 'International Transfer'}
            ]
        }
    ]
    
    with conn.cursor() as cur:
        for event in timeline_events:
            # Insert event (using existing column names: date, description, significance)
            cur.execute("""
                INSERT INTO timeline_events 
                (date, description, significance, context,
                 evidence_package, event_title, phase, phase_number, 
                 evidence_source, evidence_location, is_critical)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                event['date'],
                event['description'],
                event['significance'],
                event['phase'],  # Store phase in context field
                event['evidence_location'],  # Store location in evidence_package
                event['title'],
                event['phase'],
                event['phase_number'],
                event['evidence_source'],
                event['evidence_location'],
                event['is_critical']
            ))
            
            event_id = cur.fetchone()[0]
            
            # Insert entities
            if event['entities']:
                entity_values = [
                    (event_id, entity['name'], entity['type'], entity['role'])
                    for entity in event['entities']
                ]
                execute_values(cur, """
                    INSERT INTO timeline_event_entities 
                    (event_id, entity_name, entity_type, role_in_event)
                    VALUES %s
                """, entity_values)
            
            # Insert transactions
            if event['transactions']:
                transaction_values = [
                    (event_id, tx['description'], tx['amount'], 
                     tx['from_entity'], tx['to_entity'], tx['type'])
                    for tx in event['transactions']
                ]
                execute_values(cur, """
                    INSERT INTO timeline_event_transactions 
                    (event_id, transaction_description, amount_zar, 
                     from_entity, to_entity, transaction_type)
                    VALUES %s
                """, transaction_values)
        
        conn.commit()
        print(f"✓ Inserted {len(timeline_events)} timeline events with entities and transactions")

def create_summary_view(conn):
    """Create summary view for timeline analysis"""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE OR REPLACE VIEW timeline_summary AS
            SELECT 
                te.id,
                te.date as event_date,
                te.event_title,
                te.phase,
                te.phase_number,
                te.is_critical,
                COUNT(DISTINCT tee.entity_name) as entity_count,
                COUNT(DISTINCT tet.id) as transaction_count,
                COALESCE(SUM(tet.amount_zar), 0) as total_amount,
                te.evidence_source,
                te.evidence_location,
                te.description,
                te.significance
            FROM timeline_events te
            LEFT JOIN timeline_event_entities tee ON te.id = tee.event_id
            LEFT JOIN timeline_event_transactions tet ON te.id = tet.event_id
            GROUP BY te.id, te.date, te.event_title, te.phase, 
                     te.phase_number, te.is_critical, te.evidence_source, 
                     te.evidence_location, te.description, te.significance
            ORDER BY te.date;
        """)
        
        conn.commit()
        print("✓ Created timeline summary view")

def main():
    """Main execution"""
    print("\n" + "="*60)
    print("Syncing Comprehensive Timeline to Neon Database")
    print("="*60 + "\n")
    
    try:
        conn = get_db_connection()
        print("✓ Connected to Neon database\n")
        
        # Create tables
        create_timeline_tables(conn)
        
        # Insert timeline events
        insert_timeline_events(conn)
        
        # Create summary view
        create_summary_view(conn)
        
        # Query summary
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM timeline_events")
            event_count = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM timeline_event_entities")
            entity_count = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM timeline_event_transactions")
            transaction_count = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM timeline_events WHERE is_critical = TRUE")
            critical_count = cur.fetchone()[0]
        
        print("\n" + "="*60)
        print("Timeline Sync Summary")
        print("="*60)
        print(f"Total Events: {event_count}")
        print(f"Critical Events: {critical_count}")
        print(f"Entity Involvements: {entity_count}")
        print(f"Transactions: {transaction_count}")
        print("="*60 + "\n")
        
        conn.close()
        print("✓ Database connection closed")
        print("\n✅ Timeline sync completed successfully!\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        raise

if __name__ == "__main__":
    main()

