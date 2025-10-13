#!/usr/bin/env python3
"""
Extract dates, entities, and financial data from trial balance Excel files.
This script processes the trial balance files and extracts key information for timeline and entity analysis.
"""

import pandas as pd
import json
from datetime import datetime
import re
from pathlib import Path

def extract_dates_from_text(text):
    """Extract dates from text using various patterns."""
    if pd.isna(text) or not isinstance(text, str):
        return []
    
    dates = []
    
    # Pattern for dates like "01/03/19 to 29/02/20"
    date_range_pattern = r'(\d{1,2}/\d{1,2}/\d{2,4})\s*to\s*(\d{1,2}/\d{1,2}/\d{2,4})'
    matches = re.findall(date_range_pattern, text)
    for match in matches:
        dates.extend(match)
    
    # Pattern for individual dates
    date_pattern = r'\d{1,2}/\d{1,2}/\d{2,4}'
    individual_dates = re.findall(date_pattern, text)
    dates.extend(individual_dates)
    
    # Pattern for dates like "2020-02-28"
    iso_date_pattern = r'\d{4}-\d{2}-\d{2}'
    iso_dates = re.findall(iso_date_pattern, text)
    dates.extend(iso_dates)
    
    return list(set(dates))  # Remove duplicates

def normalize_date(date_str):
    """Normalize date string to standard format."""
    if not date_str:
        return None
    
    try:
        # Handle different date formats
        if '/' in date_str:
            parts = date_str.split('/')
            if len(parts) == 3:
                day, month, year = parts
                if len(year) == 2:
                    year = '20' + year if int(year) < 50 else '19' + year
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        elif '-' in date_str and len(date_str) == 10:
            return date_str
    except:
        pass
    
    return date_str

def extract_entities_from_account_names(df):
    """Extract entity names from account descriptions."""
    entities = set()
    
    # Look for entity names in account descriptions
    entity_patterns = [
        r'RegimA\s*(?:Skin\s*Treatments?)?',
        r'Strategic\s*Logistics?',
        r'Villa\s*Via',
        r'RWWD',
        r'RWW',
        r'RST',
        r'SLG',
        r'DERM',
        r'FNB',
        r'SARS'
    ]
    
    for col in df.columns:
        if df[col].dtype == 'object':
            for value in df[col].dropna():
                if isinstance(value, str):
                    for pattern in entity_patterns:
                        matches = re.findall(pattern, value, re.IGNORECASE)
                        entities.update(matches)
    
    return list(entities)

def extract_financial_transactions(df, entity_name):
    """Extract significant financial transactions."""
    transactions = []
    
    # Look for loan accounts and significant amounts
    for idx, row in df.iterrows():
        try:
            # Check for loan accounts
            account_desc = str(row.get('Account', '')) if 'Account' in row else ''
            if 'loan' in account_desc.lower() or 'members' in account_desc.lower():
                amount_cols = [col for col in df.columns if any(x in str(col).lower() for x in ['dr', 'cr', 'total', 'final', 'balance'])]
                for col in amount_cols:
                    if col in row and pd.notna(row[col]) and isinstance(row[col], (int, float)) and abs(row[col]) > 10000:
                        transactions.append({
                            'entity': entity_name,
                            'account': account_desc,
                            'amount': float(row[col]),
                            'type': 'loan_transaction',
                            'column': col
                        })
        except Exception as e:
            continue
    
    return transactions

def process_trial_balance_file(file_path, entity_name):
    """Process a single trial balance Excel file."""
    print(f"Processing {file_path} for entity {entity_name}")
    
    try:
        # Read all sheets
        excel_file = pd.ExcelFile(file_path)
        sheet_data = {}
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            sheet_data[sheet_name] = df
        
        # Extract information
        extracted_data = {
            'entity': entity_name,
            'file_path': str(file_path),
            'dates': [],
            'entities': [],
            'transactions': [],
            'sheets': list(sheet_data.keys())
        }
        
        # Process each sheet
        for sheet_name, df in sheet_data.items():
            print(f"  Processing sheet: {sheet_name}")
            
            # Extract dates from all text content
            for col in df.columns:
                if df[col].dtype == 'object':
                    for value in df[col].dropna():
                        dates = extract_dates_from_text(str(value))
                        extracted_data['dates'].extend(dates)
            
            # Extract entities
            entities = extract_entities_from_account_names(df)
            extracted_data['entities'].extend(entities)
            
            # Extract transactions
            transactions = extract_financial_transactions(df, entity_name)
            extracted_data['transactions'].extend(transactions)
        
        # Normalize and deduplicate dates
        extracted_data['dates'] = list(set([normalize_date(d) for d in extracted_data['dates'] if d]))
        extracted_data['entities'] = list(set(extracted_data['entities']))
        
        return extracted_data
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def main():
    """Main function to process all trial balance files."""
    
    # File mappings
    files_to_process = [
        ('/home/ubuntu/upload/REG-TRIALBALANCE.xlsx', 'RegimA Skin Treatments'),
        ('/home/ubuntu/upload/WW-TrialBalanceFEB20.xlsx', 'RegimA Worldwide Distribution'),
        ('/home/ubuntu/upload/SL-TRIALBALANCE2020.xlsx', 'Strategic Logistics'),
        ('/home/ubuntu/upload/VV-TRIALBALANCEAPR20202.xlsx', 'Villa Via')
    ]
    
    all_extracted_data = []
    
    # Process each file
    for file_path, entity_name in files_to_process:
        if Path(file_path).exists():
            data = process_trial_balance_file(file_path, entity_name)
            if data:
                all_extracted_data.append(data)
        else:
            print(f"File not found: {file_path}")
    
    # Save extracted data
    output_file = '/home/ubuntu/analysis/extracted_trial_balance_data.json'
    with open(output_file, 'w') as f:
        json.dump(all_extracted_data, f, indent=2, default=str)
    
    print(f"\nExtracted data saved to: {output_file}")
    
    # Print summary
    print("\n=== EXTRACTION SUMMARY ===")
    all_dates = set()
    all_entities = set()
    total_transactions = 0
    
    for data in all_extracted_data:
        print(f"\nEntity: {data['entity']}")
        print(f"  Dates found: {len(data['dates'])}")
        print(f"  Entities found: {len(data['entities'])}")
        print(f"  Transactions found: {len(data['transactions'])}")
        print(f"  Sheets processed: {', '.join(data['sheets'])}")
        
        all_dates.update(data['dates'])
        all_entities.update(data['entities'])
        total_transactions += len(data['transactions'])
    
    print(f"\n=== OVERALL SUMMARY ===")
    print(f"Total unique dates: {len(all_dates)}")
    print(f"Total unique entities: {len(all_entities)}")
    print(f"Total transactions: {total_transactions}")
    print(f"Date range: {min(all_dates) if all_dates else 'N/A'} to {max(all_dates) if all_dates else 'N/A'}")
    print(f"Entities found: {', '.join(sorted(all_entities))}")

if __name__ == "__main__":
    main()
