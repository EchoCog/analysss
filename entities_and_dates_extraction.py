#!/usr/bin/env python3
"""
Extract entities and dates from Excel trial balance attachments.
This script provides a comprehensive extraction of all entities and dates found in the trial balance files.
"""

import pandas as pd
import json
import re
from datetime import datetime
from pathlib import Path

def extract_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    all_dates = []
    all_entities = []

    if 'timeline' in data:
        for category, events in data['timeline'].items():
            for event in events:
                if 'date' in event:
                    all_dates.append(event['date'])

    if 'entities' in data:
        for category, entities in data['entities'].items():
            for entity in entities:
                if 'name' in entity:
                    all_entities.append(entity['name'])

    return list(set(all_dates)), list(set(all_entities))

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
    
    return list(set(dates))

def normalize_date(date_str):
    """Normalize date string to standard format."""
    if not date_str:
        return None
    
    try:
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

def extract_entities_from_content(df, context=""):
    """Extract entity names from DataFrame content."""
    entities = set()
    
    # Common entity patterns
    entity_patterns = [
        r'RegimA\s*Skin\s*Treatments?',
        r'Strategic\s*Logistics?',
        r'Villa\s*Via',
        r'RWWD',
        r'RWW',
        r'RST',
        r'SLG',
        r'DERM',
        r'FNB',
        r'SARS',
        r'Regima\s*Worldwide',
        r'Regima(?!\s*Skin)',
        r'Bernadine\s*Wright',
        r'Jacqui\s*Faucitt',
        r'Peter\s*(?:Andrew\s*)?Faucitt',
        r'Rynette\s*Farrar',
        r'Daniel\s*Faucitt',
        r'Danie\s*Bantjes'
    ]
    
    # Search in all columns
    for col in df.columns:
        if df[col].dtype == 'object':
            for value in df[col].dropna():
                if isinstance(value, str):
                    for pattern in entity_patterns:
                        matches = re.findall(pattern, value, re.IGNORECASE)
                        entities.update([match.strip() for match in matches])
    
    return list(entities)

def process_reg_trial_balance():
    """Process RegimA Skin Treatments trial balance."""
    file_path = '/home/ubuntu/upload/REG-TRIALBALANCE.xlsx'
    
    if not Path(file_path).exists():
        return None
    
    # Read both sheets
    tb_df = pd.read_excel(file_path, sheet_name='TB')
    aje_df = pd.read_excel(file_path, sheet_name='AJEs')
    
    extraction = {
        'file': 'REG-TRIALBALANCE.xlsx',
        'entity': 'RegimA Skin Treatments (RST)',
        'dates': [],
        'entities': [],
        'key_accounts': [],
        'significant_amounts': []
    }
    
    # Extract dates
    all_dates = []
    for df in [tb_df, aje_df]:
        for col in df.columns:
            if df[col].dtype == 'object':
                for value in df[col].dropna():
                    all_dates.extend(extract_dates_from_text(str(value)))
    
    extraction['dates'] = list(set([normalize_date(d) for d in all_dates if d]))
    
    # Extract entities
    all_entities = []
    for df in [tb_df, aje_df]:
        all_entities.extend(extract_entities_from_content(df))
    extraction['entities'] = list(set(all_entities))
    
    # Extract key accounts and amounts
    if 'Account' in tb_df.columns:
        for idx, row in tb_df.iterrows():
            account = str(row.get('Account', ''))
            if any(keyword in account.lower() for keyword in ['loan', 'interest', 'admin', 'director']):
                # Find amount columns
                amount_cols = [col for col in tb_df.columns if any(x in str(col).lower() for x in ['final', 'total', 'dr', 'cr'])]
                for col in amount_cols:
                    if col in row and pd.notna(row[col]) and isinstance(row[col], (int, float)) and abs(row[col]) > 100000:
                        extraction['key_accounts'].append({
                            'account': account,
                            'amount': float(row[col]),
                            'column': col
                        })
    
    return extraction

def process_ww_trial_balance():
    """Process RegimA Worldwide Distribution trial balance."""
    file_path = '/home/ubuntu/upload/WW-TrialBalanceFEB20.xlsx'
    
    if not Path(file_path).exists():
        return None
    
    # Read both sheets
    tb_df = pd.read_excel(file_path, sheet_name='WW - TrialBalance FEB20')
    aje_df = pd.read_excel(file_path, sheet_name="AJE'S")
    
    extraction = {
        'file': 'WW-TrialBalanceFEB20.xlsx',
        'entity': 'RegimA Worldwide Distribution (RWW/RWWD)',
        'dates': [],
        'entities': [],
        'key_accounts': [],
        'significant_amounts': []
    }
    
    # Extract dates
    all_dates = []
    for df in [tb_df, aje_df]:
        for col in df.columns:
            if df[col].dtype == 'object':
                for value in df[col].dropna():
                    all_dates.extend(extract_dates_from_text(str(value)))
    
    extraction['dates'] = list(set([normalize_date(d) for d in all_dates if d]))
    
    # Extract entities
    all_entities = []
    for df in [tb_df, aje_df]:
        all_entities.extend(extract_entities_from_content(df))
    extraction['entities'] = list(set(all_entities))
    
    # Extract key accounts
    if 'Name' in tb_df.columns:
        for idx, row in tb_df.iterrows():
            account = str(row.get('Name', ''))
            if any(keyword in account.lower() for keyword in ['loan', 'admin', 'regima', 'cost']):
                # Find amount columns
                amount_cols = [col for col in tb_df.columns if 'FINAL TB' in str(col) or 'Total' in str(col)]
                for col in amount_cols:
                    if col in row and pd.notna(row[col]) and isinstance(row[col], (int, float)) and abs(row[col]) > 50000:
                        extraction['key_accounts'].append({
                            'account': account,
                            'amount': float(row[col]),
                            'column': col
                        })
    
    return extraction

def process_sl_trial_balance():
    """Process Strategic Logistics trial balance."""
    file_path = '/home/ubuntu/upload/SL-TRIALBALANCE2020.xlsx'
    
    if not Path(file_path).exists():
        return None
    
    # Read all sheets
    tb_df = pd.read_excel(file_path, sheet_name='TB')
    aje_df = pd.read_excel(file_path, sheet_name='AJEs')
    vat_df = pd.read_excel(file_path, sheet_name='VAT')
    
    extraction = {
        'file': 'SL-TRIALBALANCE2020.xlsx',
        'entity': 'Strategic Logistics (SLG)',
        'dates': [],
        'entities': [],
        'key_accounts': [],
        'significant_amounts': []
    }
    
    # Extract dates
    all_dates = []
    for df in [tb_df, aje_df, vat_df]:
        for col in df.columns:
            if df[col].dtype == 'object':
                for value in df[col].dropna():
                    all_dates.extend(extract_dates_from_text(str(value)))
    
    extraction['dates'] = list(set([normalize_date(d) for d in all_dates if d]))
    
    # Extract entities
    all_entities = []
    for df in [tb_df, aje_df, vat_df]:
        all_entities.extend(extract_entities_from_content(df))
    extraction['entities'] = list(set(all_entities))
    
    # Extract key accounts
    if 'Account' in tb_df.columns:
        for idx, row in tb_df.iterrows():
            account = str(row.get('Account', ''))
            if any(keyword in account.lower() for keyword in ['loan', 'regima', 'villa', 'interest']):
                # Find amount columns
                amount_cols = [col for col in tb_df.columns if 'FINAL TB' in str(col) or 'Total' in str(col)]
                for col in amount_cols:
                    if col in row and pd.notna(row[col]) and isinstance(row[col], (int, float)) and abs(row[col]) > 100000:
                        extraction['key_accounts'].append({
                            'account': account,
                            'amount': float(row[col]),
                            'column': col
                        })
    
    return extraction

def process_vv_trial_balance():
    """Process Villa Via trial balance."""
    file_path = '/home/ubuntu/upload/VV-TRIALBALANCEAPR20202.xlsx'
    
    if not Path(file_path).exists():
        return None
    
    # Read both sheets
    tb_df = pd.read_excel(file_path, sheet_name='TB')
    aje_df = pd.read_excel(file_path, sheet_name="AJE'S")
    
    extraction = {
        'file': 'VV-TRIALBALANCEAPR20202.xlsx',
        'entity': 'Villa Via',
        'dates': [],
        'entities': [],
        'key_accounts': [],
        'significant_amounts': []
    }
    
    # Extract dates
    all_dates = []
    for df in [tb_df, aje_df]:
        for col in df.columns:
            if df[col].dtype == 'object':
                for value in df[col].dropna():
                    all_dates.extend(extract_dates_from_text(str(value)))
    
    extraction['dates'] = list(set([normalize_date(d) for d in all_dates if d]))
    
    # Extract entities
    all_entities = []
    for df in [tb_df, aje_df]:
        all_entities.extend(extract_entities_from_content(df))
    extraction['entities'] = list(set(all_entities))
    
    # Extract key accounts
    if 'Account' in tb_df.columns:
        for idx, row in tb_df.iterrows():
            account = str(row.get('Account', ''))
            if any(keyword in account.lower() for keyword in ['loan', 'rental', 'members', 'strategic', 'regima']):
                # Find amount columns
                amount_cols = [col for col in tb_df.columns if 'FINAL TB' in str(col) or 'Net' in str(col)]
                for col in amount_cols:
                    if col in row and pd.notna(row[col]) and isinstance(row[col], (int, float)) and abs(row[col]) > 100000:
                        extraction['key_accounts'].append({
                            'account': account,
                            'amount': float(row[col]),
                            'column': col
                        })
    
    return extraction

def main():
    """Main extraction function."""
    print("📊 EXTRACTING ENTITIES AND DATES FROM EXCEL ATTACHMENTS")
    print("=" * 60)
    
    # Process all files
    extractions = []
    
    reg_data = process_reg_trial_balance()
    if reg_data:
        extractions.append(reg_data)
        print(f"✅ Processed: {reg_data['file']}")
    
    ww_data = process_ww_trial_balance()
    if ww_data:
        extractions.append(ww_data)
        print(f"✅ Processed: {ww_data['file']}")
    
    sl_data = process_sl_trial_balance()
    if sl_data:
        extractions.append(sl_data)
        print(f"✅ Processed: {sl_data['file']}")
    
    vv_data = process_vv_trial_balance()
    if vv_data:
        extractions.append(vv_data)
        print(f"✅ Processed: {vv_data['file']}")
    
    # Compile summary
    all_dates = set()
    all_entities = set()
    
    for extraction in extractions:
        all_dates.update(extraction['dates'])
        all_entities.update(extraction['entities'])
    
    summary = {
        'extraction_timestamp': datetime.now().isoformat(),
        'files_processed': len(extractions),
        'total_unique_dates': len(all_dates),
        'total_unique_entities': len(all_entities),
        'date_range': {
            'earliest': min(all_dates) if all_dates else None,
            'latest': max(all_dates) if all_dates else None
        },
        'all_dates': sorted(list(all_dates)),
        'all_entities': sorted(list(all_entities)),
        'detailed_extractions': extractions
    }
    
    # Save results
    output_file = '/home/ubuntu/entities_and_dates_extraction.json'
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    print(f"\n📋 EXTRACTION SUMMARY")
    print(f"Files processed: {summary['files_processed']}")
    print(f"Total unique dates: {summary['total_unique_dates']}")
    print(f"Total unique entities: {summary['total_unique_entities']}")
    print(f"Date range: {summary['date_range']['earliest']} to {summary['date_range']['latest']}")
    
    print(f"\n📅 ALL DATES FOUND:")
    for date in summary['all_dates']:
        print(f"  • {date}")
    
    print(f"\n🏢 ALL ENTITIES FOUND:")
    for entity in summary['all_entities']:
        print(f"  • {entity}")
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return summary

if __name__ == "__main__":
    main()
