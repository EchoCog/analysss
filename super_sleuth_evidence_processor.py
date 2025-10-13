#!/usr/bin/env python3
"""
Super-Sleuth Evidence Processor
Advanced entity and timeline extraction from RegimA Group financial evidence
"""

import os
import json
import re
import pandas as pd
from datetime import datetime
from pathlib import Path
import hashlib

class SuperSleuthProcessor:
    def __init__(self, evidence_dir="/home/ubuntu/upload"):
        self.evidence_dir = evidence_dir
        self.entities = set()
        self.dates = set()
        self.relationships = []
        self.financial_data = {}
        self.timeline_events = []
        
        # Known entity patterns for RegimA Group
        self.entity_patterns = {
            'companies': [
                r'RegimA\s+(?:Skin\s+Treatments?|Group)',
                r'Strategic\s+Logistics?',
                r'RegimA\s+Worldwide\s+Distribution',
                r'Villa\s+Via\s+Arcadia',
                r'RST\b',
                r'SLG\b', 
                r'RWD\b',
                r'VVA\b'
            ],
            'financial_institutions': [
                r'FNB\b',
                r'First\s+National\s+Bank',
                r'Standard\s+Bank',
                r'ABSA\b',
                r'Nedbank'
            ],
            'regulatory': [
                r'SARS\b',
                r'South\s+African\s+Revenue\s+Service',
                r'CIPC\b',
                r'Companies\s+and\s+Intellectual\s+Property\s+Commission'
            ],
            'people': [
                r'Danie\s+Bantjes?',
                r'Peter\s+Faucitt',
                r'Daniel\s+Bantjes?'
            ]
        }
        
        # Date patterns
        self.date_patterns = [
            r'\b(\d{4}[-/]\d{1,2}[-/]\d{1,2})\b',
            r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{4})\b',
            r'\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{4})\b',
            r'\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},?\s+\d{4})\b'
        ]
        
    def extract_from_markdown(self, file_path):
        """Extract entities and dates from markdown files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract entities
            for category, patterns in self.entity_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        entity = match.group(0).strip()
                        self.entities.add(entity)
                        
            # Extract dates
            for pattern in self.date_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    date_str = match.group(1)
                    try:
                        # Normalize date format
                        parsed_date = self._parse_date(date_str)
                        if parsed_date:
                            self.dates.add(parsed_date.strftime('%Y-%m-%d'))
                    except:
                        continue
                        
            # Extract financial amounts and relationships
            amount_pattern = r'R\s*([0-9,]+(?:\.[0-9]{2})?)'
            amounts = re.findall(amount_pattern, content)
            
            return {
                'file': os.path.basename(file_path),
                'entities_found': len([e for e in self.entities]),
                'dates_found': len(self.dates),
                'financial_amounts': len(amounts)
            }
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
            
    def extract_from_excel(self, file_path):
        """Extract entities and dates from Excel files"""
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            sheet_data = {}
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                sheet_data[sheet_name] = df
                
                # Extract from column headers and data
                content = ' '.join([str(col) for col in df.columns if pd.notna(col)])
                content += ' ' + ' '.join([str(val) for val in df.values.flatten() if pd.notna(val)])
                
                # Apply entity extraction
                for category, patterns in self.entity_patterns.items():
                    for pattern in patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            entity = match.group(0).strip()
                            self.entities.add(entity)
                            
                # Extract dates from data
                for col in df.columns:
                    if 'date' in str(col).lower() or 'period' in str(col).lower():
                        for val in df[col].dropna():
                            try:
                                if isinstance(val, datetime):
                                    self.dates.add(val.strftime('%Y-%m-%d'))
                                else:
                                    parsed_date = self._parse_date(str(val))
                                    if parsed_date:
                                        self.dates.add(parsed_date.strftime('%Y-%m-%d'))
                            except:
                                continue
                                
            return {
                'file': os.path.basename(file_path),
                'sheets': list(sheet_data.keys()),
                'entities_found': len([e for e in self.entities]),
                'dates_found': len(self.dates)
            }
            
        except Exception as e:
            print(f"Error processing Excel file {file_path}: {e}")
            return None
            
    def extract_from_email(self, file_path):
        """Extract entities and dates from email files"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Extract email headers for dates
            date_headers = re.findall(r'Date:\s*([^\n\r]+)', content, re.IGNORECASE)
            for date_header in date_headers:
                try:
                    parsed_date = self._parse_email_date(date_header)
                    if parsed_date:
                        self.dates.add(parsed_date.strftime('%Y-%m-%d'))
                except:
                    continue
                    
            # Extract entities from email content
            for category, patterns in self.entity_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        entity = match.group(0).strip()
                        self.entities.add(entity)
                        
            # Extract financial data from email
            amount_pattern = r'R\s*([0-9,]+(?:\.[0-9]{2})?)'
            amounts = re.findall(amount_pattern, content)
            
            return {
                'file': os.path.basename(file_path),
                'entities_found': len([e for e in self.entities]),
                'dates_found': len(self.dates),
                'financial_amounts': len(amounts)
            }
            
        except Exception as e:
            print(f"Error processing email {file_path}: {e}")
            return None
            
    def _parse_date(self, date_str):
        """Parse various date formats"""
        date_formats = [
            '%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y',
            '%d %b %Y', '%d %B %Y', '%b %d, %Y', '%B %d, %Y'
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except:
                continue
        return None
        
    def _parse_email_date(self, date_str):
        """Parse email date headers"""
        try:
            # Remove timezone info for parsing
            date_clean = re.sub(r'\s*[+-]\d{4}.*$', '', date_str.strip())
            date_clean = re.sub(r'\s*\([^)]+\).*$', '', date_clean)
            
            # Common email date formats
            formats = [
                '%a, %d %b %Y %H:%M:%S',
                '%d %b %Y %H:%M:%S',
                '%a, %d %B %Y %H:%M:%S',
                '%d %B %Y %H:%M:%S'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_clean, fmt)
                except:
                    continue
        except:
            pass
        return None
        
    def process_all_evidence(self):
        """Process all evidence files in the directory"""
        results = {
            'processing_timestamp': datetime.now().isoformat(),
            'files_processed': [],
            'total_entities': 0,
            'total_dates': 0,
            'entities_by_category': {},
            'timeline_events': [],
            'financial_summary': {}
        }
        
        # Process all files in evidence directory
        for root, dirs, files in os.walk(self.evidence_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext == '.md':
                    result = self.extract_from_markdown(file_path)
                elif file_ext in ['.xlsx', '.xls']:
                    result = self.extract_from_excel(file_path)
                elif file_ext == '.eml':
                    result = self.extract_from_email(file_path)
                else:
                    continue
                    
                if result:
                    results['files_processed'].append(result)
                    
        # Categorize entities
        for entity in self.entities:
            categorized = False
            for category, patterns in self.entity_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, entity, re.IGNORECASE):
                        if category not in results['entities_by_category']:
                            results['entities_by_category'][category] = []
                        results['entities_by_category'][category].append(entity)
                        categorized = True
                        break
                if categorized:
                    break
                    
        # Create timeline events
        sorted_dates = sorted(list(self.dates))
        for date in sorted_dates:
            results['timeline_events'].append({
                'date': date,
                'event_type': 'financial_activity',
                'description': f'Financial activity recorded for RegimA Group entities',
                'entities_involved': list(self.entities)[:5]  # Limit for readability
            })
            
        results['total_entities'] = len(self.entities)
        results['total_dates'] = len(self.dates)
        results['all_entities'] = sorted(list(self.entities))
        results['all_dates'] = sorted_dates
        
        return results
        
    def generate_hypergraph_nodes(self):
        """Generate nodes for hypergraph representation"""
        nodes = []
        
        # Entity nodes
        for entity in self.entities:
            node_id = hashlib.md5(entity.encode()).hexdigest()[:8]
            nodes.append({
                'id': node_id,
                'label': entity,
                'type': 'entity',
                'category': self._categorize_entity(entity)
            })
            
        # Date nodes (events)
        for date in self.dates:
            node_id = f"event_{date.replace('-', '_')}"
            nodes.append({
                'id': node_id,
                'label': f"Event {date}",
                'type': 'event',
                'date': date
            })
            
        return nodes
        
    def generate_hypergraph_edges(self):
        """Generate edges for hypergraph representation"""
        edges = []
        
        # Connect entities that appear in same documents
        entity_list = list(self.entities)
        for i, entity1 in enumerate(entity_list):
            for entity2 in entity_list[i+1:]:
                edge_id = f"rel_{hashlib.md5(f'{entity1}_{entity2}'.encode()).hexdigest()[:8]}"
                edges.append({
                    'id': edge_id,
                    'source': hashlib.md5(entity1.encode()).hexdigest()[:8],
                    'target': hashlib.md5(entity2.encode()).hexdigest()[:8],
                    'type': 'relationship',
                    'weight': 1.0
                })
                
        return edges
        
    def _categorize_entity(self, entity):
        """Categorize an entity based on patterns"""
        for category, patterns in self.entity_patterns.items():
            for pattern in patterns:
                if re.search(pattern, entity, re.IGNORECASE):
                    return category
        return 'unknown'

def main():
    processor = SuperSleuthProcessor()
    
    print("🕵️ Super-Sleuth Evidence Processor Starting...")
    print("=" * 60)
    
    # Process all evidence
    results = processor.process_all_evidence()
    
    # Save results
    output_file = '/home/ubuntu/analysis/super_sleuth_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
        
    # Generate hypergraph data
    nodes = processor.generate_hypergraph_nodes()
    edges = processor.generate_hypergraph_edges()
    
    hypergraph_data = {
        'nodes': nodes,
        'edges': edges,
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_nodes': len(nodes),
            'total_edges': len(edges)
        }
    }
    
    hypergraph_file = '/home/ubuntu/analysis/super_sleuth_hypergraph.json'
    with open(hypergraph_file, 'w') as f:
        json.dump(hypergraph_data, f, indent=2)
        
    print(f"✅ Analysis complete!")
    print(f"📊 Processed {len(results['files_processed'])} files")
    print(f"🏢 Found {results['total_entities']} unique entities")
    print(f"📅 Found {results['total_dates']} unique dates")
    print(f"🔗 Generated {len(nodes)} nodes and {len(edges)} edges")
    print(f"💾 Results saved to: {output_file}")
    print(f"🕸️ Hypergraph data saved to: {hypergraph_file}")
    
    return results

if __name__ == "__main__":
    main()
