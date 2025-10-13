#!/usr/bin/env python3
"""
Sync new evidence to Supabase database
"""

import os
import json
from datetime import datetime
from supabase import create_client, Client

def sync_evidence_to_supabase():
    """Sync the new compliance directive evidence to Supabase"""
    
    # Initialize Supabase client
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        print("Error: SUPABASE_URL and SUPABASE_KEY environment variables must be set")
        return False
    
    supabase: Client = create_client(url, key)
    
    try:
        # Insert evidence record
        evidence_data = {
            "id": "evidence_compliance_directive_2025_07_08",
            "title": "URGENT: MANDATORY COMPLIANCE DIRECTIVE - PERSONAL CRIMINAL LIABILITY WARNING",
            "description": "Daniel Faucitt (CIO) issues urgent compliance directive regarding illegal instructions to employees about customer data processing",
            "date_created": "2025-07-08",
            "category": "legal_compliance_directive",
            "file_path": "evidence/email_compliance_directive_2025-07-08.md",
            "hash": "compliance_directive_hash",
            "entities_involved": ["Daniel Faucitt", "Kent", "RegimA Distribution companies", "RegimA Skin Treatments", "Shopify"],
            "metadata": {
                "sender": "Daniel Faucitt",
                "recipient": "Kent", 
                "urgency": "critical",
                "legal_framework": "POPI Act"
            }
        }
        
        # Insert or update evidence
        result = supabase.table("evidence").upsert(evidence_data).execute()
        print(f"Evidence synced: {result.data}")
        
        # Insert event record
        event_data = {
            "id": "event_compliance_directive_2025_07_08",
            "event_date": "2025-07-08",
            "event_type": "legal_compliance_directive",
            "title": "Compliance Directive Issued",
            "description": "Daniel Faucitt issues urgent compliance directive warning of personal criminal liability for POPI violations",
            "entities_involved": ["Daniel Faucitt", "Kent", "RegimA Distribution companies", "RegimA Skin Treatments"],
            "evidence_id": "evidence_compliance_directive_2025_07_08",
            "metadata": {
                "severity": "critical",
                "legal_act": "POPI",
                "penalties": {
                    "unauthorized_access": "10 years imprisonment",
                    "processing_violations": "R10 million fine"
                }
            }
        }
        
        # Insert or update event
        result = supabase.table("events").upsert(event_data).execute()
        print(f"Event synced: {result.data}")
        
        # Insert entities
        entities = [
            {
                "id": "entity_daniel_faucitt",
                "name": "Daniel Faucitt",
                "type": "person",
                "description": "Chief Information Officer (CIO) at RegimA",
                "metadata": {
                    "role": "CIO",
                    "email": "dan@regima.com",
                    "authority_level": "executive"
                }
            },
            {
                "id": "entity_kent_recipient",
                "name": "Kent",
                "type": "person", 
                "description": "Employee at RegimA",
                "metadata": {
                    "email": "kent@regima.zone",
                    "authority_level": "employee"
                }
            },
            {
                "id": "entity_regima_distribution",
                "name": "RegimA Distribution companies",
                "type": "organization",
                "description": "Legal owner of customer data",
                "metadata": {
                    "data_ownership": "customer_data_owner",
                    "legal_status": "authorized"
                }
            },
            {
                "id": "entity_regima_skin_treatments",
                "name": "RegimA Skin Treatments",
                "type": "organization",
                "description": "Unauthorized third party to customer data",
                "metadata": {
                    "data_ownership": "unauthorized_third_party",
                    "legal_status": "unauthorized",
                    "risk_level": "high"
                }
            },
            {
                "id": "entity_shopify",
                "name": "Shopify",
                "type": "technology_platform",
                "description": "Authorized system for customer data processing",
                "metadata": {
                    "authorization_status": "authorized",
                    "function": "customer_data_processing"
                }
            }
        ]
        
        # Insert or update entities
        for entity in entities:
            result = supabase.table("entities").upsert(entity).execute()
            print(f"Entity synced: {entity['name']}")
        
        # Insert relationships
        relationships = [
            {
                "id": "rel_faucitt_regima",
                "from_entity_id": "entity_daniel_faucitt",
                "to_entity_id": "entity_regima_distribution",
                "relationship_type": "employment",
                "description": "Daniel Faucitt is CIO at RegimA Distribution",
                "metadata": {
                    "authority": "high",
                    "relationship": "executive_employee"
                }
            },
            {
                "id": "rel_kent_regima",
                "from_entity_id": "entity_kent_recipient",
                "to_entity_id": "entity_regima_distribution",
                "relationship_type": "employment",
                "description": "Kent is employee at RegimA Distribution",
                "metadata": {
                    "authority": "low",
                    "relationship": "employee"
                }
            },
            {
                "id": "rel_regima_shopify",
                "from_entity_id": "entity_regima_distribution",
                "to_entity_id": "entity_shopify",
                "relationship_type": "data_processing_authorization",
                "description": "RegimA Distribution authorizes Shopify for customer data processing",
                "metadata": {
                    "status": "compliant",
                    "relationship": "authorized_processor"
                }
            },
            {
                "id": "rel_skin_treatments_risk",
                "from_entity_id": "entity_regima_skin_treatments",
                "to_entity_id": "entity_regima_distribution",
                "relationship_type": "unauthorized_access_risk",
                "description": "RegimA Skin Treatments poses unauthorized access risk to customer data",
                "metadata": {
                    "status": "violation_risk",
                    "relationship": "unauthorized_third_party"
                }
            }
        ]
        
        # Insert or update relationships
        for relationship in relationships:
            result = supabase.table("relationships").upsert(relationship).execute()
            print(f"Relationship synced: {relationship['id']}")
        
        print("✅ All evidence successfully synced to Supabase!")
        return True
        
    except Exception as e:
        print(f"❌ Error syncing to Supabase: {e}")
        return False

if __name__ == "__main__":
    sync_evidence_to_supabase()
