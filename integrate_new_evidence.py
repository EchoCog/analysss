#!/usr/bin/env python
# coding: utf-8

import json
import os
from datetime import datetime

def get_file_hash(file_path):
    import hashlib
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def integrate_new_evidence():
    processed_documents_path = '/home/ubuntu/analysis/processed_documents.json'
    
    # Load existing processed documents
    if os.path.exists(processed_documents_path):
        with open(processed_documents_path, 'r') as f:
            processed_data = json.load(f)
    else:
        processed_data = {"processed": {}}

    # New evidence files
    new_evidence_files = {
        'email_compliance_directive_2025-07-08.md': {
            'category': 'evidence',
            'destination': '02_evidence/communications',
            'entities': {
                'persons': ['Daniel Faucitt', 'Kent'],
                'organizations': ['RegimA Distribution companies', 'RegimA Skin Treatments', 'Shopify', 'inforegulator.org.za'],
                'dates': ['2025-07-08'],
                'document_types': ['Compliance Directive']
            },
            'events': [
                {
                    'date': '2025-07-08',
                    'type': 'legal_compliance_directive',
                    'document': 'email_compliance_directive_2025-07-08.md',
                    'description': 'Urgent compliance directive issued by Daniel Faucitt regarding customer data processing.'
                }
            ]
        },
        'timeline_entry_2025-07-08.json': {
            'category': 'timeline',
            'destination': '03_timeline/entries',
            'entities': {},
            'events': []
        },
        'entity_model_regima_compliance.json': {
            'category': 'models',
            'destination': '04_models/entity_models',
            'entities': {},
            'events': []
        }
    }

    for filename, metadata in new_evidence_files.items():
        file_path = os.path.join('/home/ubuntu/analysis/evidence', filename)
        if not os.path.exists(file_path):
            file_path = os.path.join('/home/ubuntu/analysis/models', filename)

        if os.path.exists(file_path):
            file_hash = get_file_hash(file_path)
            processed_data['processed'][filename] = {
                'hash': file_hash,
                'processed_date': datetime.utcnow().isoformat(),
                'category': metadata['category'],
                'destination': metadata['destination'],
                'entities': metadata.get('entities', {}),
                'events': metadata.get('events', [])
            }

    # Write updated data back to processed_documents.json
    with open(processed_documents_path, 'w') as f:
        json.dump(processed_data, f, indent=2)

    print("New evidence integrated successfully.")

if __name__ == '__main__':
    integrate_new_evidence()

