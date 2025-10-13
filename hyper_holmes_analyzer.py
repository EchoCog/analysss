#!/usr/bin/env python3
"""
Hyper-Holmes Turbo-Solve Mode
Comprehensive analysis of the complete evidence body in the GitHub repository
"""

import os
import json
import re
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
from collections import defaultdict, Counter
import networkx as nx

class HyperHolmesAnalyzer:
    def __init__(self, repo_path="/home/ubuntu/analysis", evidence_path="/home/ubuntu/upload"):
        self.repo_path = repo_path
        self.evidence_path = evidence_path
        self.entities = {}
        self.relationships = []
        self.timeline = []
        self.financial_patterns = {}
        self.anomalies = []
        self.insights = []
        
        # Load existing analysis
        self.load_existing_data()
        
        # Financial crime patterns
        self.fraud_indicators = {
            'transfer_pricing': [
                r'below\s+cost',
                r'transfer\s+price',
                r'related\s+part(?:y|ies)',
                r'inter-?company',
                r'cost\s+of\s+sales?\s+(?:manipulation|adjustment)'
            ],
            'inventory_manipulation': [
                r'inventory\s+(?:adjustment|write-?off)',
                r'negative\s+inventory',
                r'phantom\s+(?:inventory|write-?off)',
                r'inventory\s+(?:given\s+away|manipulation)'
            ],
            'expense_dumping': [
                r'expense\s+dump(?:ing)?',
                r'forced\s+to\s+pay',
                r'blamed\s+for\s+(?:excessive\s+)?spending',
                r'scapegoat'
            ],
            'profit_extraction': [
                r'profit\s+extraction',
                r'wealth\s+transfer',
                r'rent\s+to\s+(?:himself|herself)',
                r'conflict\s+of\s+interest'
            ],
            'revenue_hijacking': [
                r'revenue\s+hijack(?:ing)?',
                r'theft',
                r'control\s+over\s+staff',
                r'facilitate\s+fraud'
            ]
        }
        
        # Entity role patterns
        self.entity_roles = {
            'victim_entities': ['RWW', 'RegimA Worldwide', 'Strategic Logistics', 'SLG'],
            'profit_centers': ['RST', 'RegimA Skin Treatments', 'Villa Via', 'VVA'],
            'control_entities': ['Villa Via', 'VVA'],
            'regulatory': ['SARS', 'CIPC'],
            'financial_institutions': ['FNB', 'ABSA', 'Standard Bank', 'Nedbank']
        }
        
    def load_existing_data(self):
        """Load existing analysis data from repository"""
        try:
            # Load super-sleuth results
            sleuth_file = os.path.join(self.repo_path, 'super_sleuth_analysis.json')
            if os.path.exists(sleuth_file):
                with open(sleuth_file, 'r') as f:
                    self.sleuth_data = json.load(f)
            
            # Load existing entities
            entities_file = os.path.join(self.repo_path, 'entities_and_dates_extraction.json')
            if os.path.exists(entities_file):
                with open(entities_file, 'r') as f:
                    self.existing_entities = json.load(f)
                    
            # Load evidence-based analysis
            evidence_file = os.path.join(self.repo_path, 'evidence_based_analysis.json')
            if os.path.exists(evidence_file):
                with open(evidence_file, 'r') as f:
                    self.evidence_analysis = json.load(f)
                    
        except Exception as e:
            print(f"Warning: Could not load existing data: {e}")
            
    def analyze_financial_patterns(self):
        """Analyze financial patterns and detect anomalies"""
        patterns = {
            'transfer_pricing_indicators': [],
            'inventory_anomalies': [],
            'expense_dumping_evidence': [],
            'profit_extraction_mechanisms': [],
            'revenue_manipulation': []
        }
        
        # Analyze all markdown files for financial patterns
        for root, dirs, files in os.walk(self.evidence_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    content = self._read_file_safe(file_path)
                    if content:
                        patterns.update(self._detect_financial_patterns(content, file))
                        
        # Analyze Excel files for numerical anomalies
        for root, dirs, files in os.walk(self.evidence_path):
            for file in files:
                if file.endswith(('.xlsx', '.xls')):
                    file_path = os.path.join(root, file)
                    patterns.update(self._analyze_excel_anomalies(file_path, file))
                    
        return patterns
        
    def _detect_financial_patterns(self, content, filename):
        """Detect financial crime patterns in text content"""
        detected = {
            'transfer_pricing_indicators': [],
            'inventory_anomalies': [],
            'expense_dumping_evidence': [],
            'profit_extraction_mechanisms': [],
            'revenue_manipulation': []
        }
        
        # Map fraud indicators to detected categories
        indicator_mapping = {
            'transfer_pricing': 'transfer_pricing_indicators',
            'inventory_manipulation': 'inventory_anomalies',
            'expense_dumping': 'expense_dumping_evidence',
            'profit_extraction': 'profit_extraction_mechanisms',
            'revenue_hijacking': 'revenue_manipulation'
        }
        
        for pattern_type, patterns in self.fraud_indicators.items():
            detected_key = indicator_mapping.get(pattern_type, pattern_type)
            if detected_key not in detected:
                detected[detected_key] = []
                
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    context = self._extract_context(content, match.start(), match.end())
                    detected[detected_key].append({
                        'file': filename,
                        'pattern': pattern,
                        'match': match.group(0),
                        'context': context,
                        'position': match.start()
                    })
                    
        return detected
        
    def _analyze_excel_anomalies(self, file_path, filename):
        """Analyze Excel files for numerical anomalies"""
        anomalies = {
            'negative_values': [],
            'unusual_ratios': [],
            'large_adjustments': [],
            'inconsistent_data': []
        }
        
        try:
            excel_file = pd.ExcelFile(file_path)
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Detect negative inventory/assets
                for col in df.columns:
                    if any(keyword in str(col).lower() for keyword in ['inventory', 'asset', 'cash']):
                        negative_values = df[df[col] < 0][col].dropna()
                        if not negative_values.empty:
                            anomalies['negative_values'].append({
                                'file': filename,
                                'sheet': sheet_name,
                                'column': col,
                                'negative_count': len(negative_values),
                                'min_value': float(negative_values.min()),
                                'values': negative_values.tolist()[:10]  # Limit for storage
                            })
                            
                # Detect large percentage changes
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    if len(df[col].dropna()) > 1:
                        values = df[col].dropna().values
                        if len(values) >= 2:
                            pct_changes = []
                            for i in range(1, len(values)):
                                if values[i-1] != 0:
                                    pct_change = abs((values[i] - values[i-1]) / values[i-1])
                                    if pct_change > 5.0:  # 500% change
                                        pct_changes.append(pct_change)
                                        
                            if pct_changes:
                                anomalies['large_adjustments'].append({
                                    'file': filename,
                                    'sheet': sheet_name,
                                    'column': col,
                                    'max_change': max(pct_changes),
                                    'change_count': len(pct_changes)
                                })
                                
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            
        return anomalies
        
    def analyze_entity_relationships(self):
        """Analyze relationships between entities"""
        relationships = defaultdict(list)
        
        # Load all entity mentions from files
        entity_mentions = defaultdict(lambda: defaultdict(int))
        
        for root, dirs, files in os.walk(self.evidence_path):
            for file in files:
                if file.endswith(('.md', '.eml')):
                    file_path = os.path.join(root, file)
                    content = self._read_file_safe(file_path)
                    if content:
                        # Count entity co-occurrences
                        entities_in_file = []
                        for entity_type, entity_list in self.entity_roles.items():
                            for entity in entity_list:
                                if re.search(rf'\b{re.escape(entity)}\b', content, re.IGNORECASE):
                                    entities_in_file.append(entity)
                                    
                        # Record co-occurrences
                        for i, entity1 in enumerate(entities_in_file):
                            for entity2 in entities_in_file[i+1:]:
                                key = tuple(sorted([entity1, entity2]))
                                entity_mentions[key][file] += 1
                                
        # Convert to relationship strength
        for (entity1, entity2), file_counts in entity_mentions.items():
            total_mentions = sum(file_counts.values())
            file_count = len(file_counts)
            
            relationships[entity1].append({
                'target': entity2,
                'strength': total_mentions,
                'file_count': file_count,
                'files': list(file_counts.keys())
            })
            
        return dict(relationships)
        
    def generate_timeline_analysis(self):
        """Generate comprehensive timeline analysis"""
        timeline_events = []
        
        # Extract dates and associated events from all files
        date_events = defaultdict(list)
        
        for root, dirs, files in os.walk(self.evidence_path):
            for file in files:
                if file.endswith(('.md', '.eml')):
                    file_path = os.path.join(root, file)
                    content = self._read_file_safe(file_path)
                    if content:
                        dates = self._extract_dates_with_context(content, file)
                        for date_info in dates:
                            date_events[date_info['date']].append(date_info)
                            
        # Sort and structure timeline
        for date in sorted(date_events.keys()):
            events = date_events[date]
            
            # Categorize events
            event_types = []
            entities_involved = set()
            financial_amounts = []
            
            for event in events:
                entities_involved.update(event.get('entities', []))
                financial_amounts.extend(event.get('amounts', []))
                
                # Categorize based on content
                if any(indicator in event['context'].lower() for indicator in ['loss', 'adjustment', 'write-off']):
                    event_types.append('financial_anomaly')
                elif any(indicator in event['context'].lower() for indicator in ['transfer', 'payment', 'invoice']):
                    event_types.append('transaction')
                else:
                    event_types.append('general')
                    
            timeline_events.append({
                'date': date,
                'event_types': list(set(event_types)),
                'entities_involved': list(entities_involved),
                'financial_amounts': financial_amounts,
                'source_files': [e['file'] for e in events],
                'context_summary': self._summarize_contexts([e['context'] for e in events]),
                'significance_score': self._calculate_significance(events)
            })
            
        return timeline_events
        
    def detect_fraud_patterns(self):
        """Detect potential fraud patterns across all evidence"""
        fraud_analysis = {
            'transfer_pricing_scheme': {
                'detected': False,
                'evidence': [],
                'entities_involved': [],
                'estimated_impact': 0
            },
            'inventory_manipulation': {
                'detected': False,
                'evidence': [],
                'entities_involved': [],
                'estimated_impact': 0
            },
            'expense_dumping': {
                'detected': False,
                'evidence': [],
                'victim_entities': [],
                'perpetrator_entities': []
            },
            'profit_extraction': {
                'detected': False,
                'evidence': [],
                'mechanisms': [],
                'beneficiaries': []
            }
        }
        
        # Analyze financial patterns
        financial_patterns = self.analyze_financial_patterns()
        
        # Transfer pricing analysis
        if financial_patterns.get('transfer_pricing_indicators'):
            fraud_analysis['transfer_pricing_scheme']['detected'] = True
            fraud_analysis['transfer_pricing_scheme']['evidence'] = financial_patterns['transfer_pricing_indicators']
            
            # Extract entities and amounts
            for evidence in financial_patterns['transfer_pricing_indicators']:
                entities = self._extract_entities_from_context(evidence['context'])
                fraud_analysis['transfer_pricing_scheme']['entities_involved'].extend(entities)
                
        # Inventory manipulation analysis
        if financial_patterns.get('inventory_anomalies'):
            fraud_analysis['inventory_manipulation']['detected'] = True
            fraud_analysis['inventory_manipulation']['evidence'] = financial_patterns['inventory_anomalies']
            
        # Expense dumping analysis
        if financial_patterns.get('expense_dumping_evidence'):
            fraud_analysis['expense_dumping']['detected'] = True
            fraud_analysis['expense_dumping']['evidence'] = financial_patterns['expense_dumping_evidence']
            
            # Identify victims and perpetrators
            for evidence in financial_patterns['expense_dumping_evidence']:
                context = evidence['context'].lower()
                if any(victim in context for victim in ['rww', 'regima worldwide', 'strategic logistics']):
                    fraud_analysis['expense_dumping']['victim_entities'].extend(['RWW', 'Strategic Logistics'])
                    
        return fraud_analysis
        
    def generate_insights(self):
        """Generate high-level insights from all analysis"""
        insights = []
        
        # Financial pattern insights
        financial_patterns = self.analyze_financial_patterns()
        fraud_patterns = self.detect_fraud_patterns()
        relationships = self.analyze_entity_relationships()
        timeline = self.generate_timeline_analysis()
        
        # Insight 1: Transfer pricing manipulation
        if fraud_patterns['transfer_pricing_scheme']['detected']:
            insights.append({
                'type': 'fraud_detection',
                'severity': 'high',
                'title': 'Transfer Pricing Manipulation Detected',
                'description': 'Evidence suggests systematic transfer pricing manipulation between related entities',
                'evidence_count': len(fraud_patterns['transfer_pricing_scheme']['evidence']),
                'entities_involved': list(set(fraud_patterns['transfer_pricing_scheme']['entities_involved'])),
                'recommendation': 'Conduct detailed transfer pricing audit and review inter-company agreements'
            })
            
        # Insight 2: Inventory anomalies
        if fraud_patterns['inventory_manipulation']['detected']:
            insights.append({
                'type': 'financial_anomaly',
                'severity': 'high',
                'title': 'Significant Inventory Manipulation',
                'description': 'Large inventory adjustments and negative inventory values indicate potential manipulation',
                'evidence_count': len(fraud_patterns['inventory_manipulation']['evidence']),
                'recommendation': 'Perform physical inventory count and review inventory valuation methods'
            })
            
        # Insight 3: Expense dumping scheme
        if fraud_patterns['expense_dumping']['detected']:
            insights.append({
                'type': 'operational_fraud',
                'severity': 'medium',
                'title': 'Expense Dumping Pattern Identified',
                'description': 'Certain entities appear to be used as expense dumping grounds',
                'victim_entities': list(set(fraud_patterns['expense_dumping']['victim_entities'])),
                'recommendation': 'Review expense allocation policies and inter-company charge mechanisms'
            })
            
        # Insight 4: Timeline concentration
        high_activity_periods = [event for event in timeline if event['significance_score'] > 0.7]
        if high_activity_periods:
            insights.append({
                'type': 'temporal_analysis',
                'severity': 'medium',
                'title': 'High-Activity Financial Periods Identified',
                'description': f'Found {len(high_activity_periods)} periods with significant financial activity',
                'periods': [event['date'] for event in high_activity_periods],
                'recommendation': 'Focus investigation on identified high-activity periods'
            })
            
        # Insight 5: Entity relationship complexity
        complex_relationships = {k: v for k, v in relationships.items() if len(v) > 3}
        if complex_relationships:
            insights.append({
                'type': 'structural_analysis',
                'severity': 'low',
                'title': 'Complex Inter-Entity Relationships',
                'description': 'Multiple entities show complex relationship patterns',
                'complex_entities': list(complex_relationships.keys()),
                'recommendation': 'Map complete organizational structure and ownership relationships'
            })
            
        return insights
        
    def _read_file_safe(self, file_path):
        """Safely read file content"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
            
    def _extract_context(self, content, start, end, window=200):
        """Extract context around a match"""
        context_start = max(0, start - window)
        context_end = min(len(content), end + window)
        return content[context_start:context_end].strip()
        
    def _extract_dates_with_context(self, content, filename):
        """Extract dates with surrounding context"""
        dates = []
        date_patterns = [
            r'\b(\d{4}[-/]\d{1,2}[-/]\d{1,2})\b',
            r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{4})\b',
            r'\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{4})\b'
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                context = self._extract_context(content, match.start(), match.end())
                entities = self._extract_entities_from_context(context)
                amounts = self._extract_amounts_from_context(context)
                
                dates.append({
                    'date': match.group(1),
                    'context': context,
                    'entities': entities,
                    'amounts': amounts,
                    'file': filename
                })
                
        return dates
        
    def _extract_entities_from_context(self, context):
        """Extract entities from context"""
        entities = []
        for entity_type, entity_list in self.entity_roles.items():
            for entity in entity_list:
                if re.search(rf'\b{re.escape(entity)}\b', context, re.IGNORECASE):
                    entities.append(entity)
        return entities
        
    def _extract_amounts_from_context(self, context):
        """Extract financial amounts from context"""
        amount_pattern = r'R\s*([0-9,]+(?:\.[0-9]{2})?)'
        amounts = re.findall(amount_pattern, context)
        return [float(amount.replace(',', '')) for amount in amounts if amount]
        
    def _summarize_contexts(self, contexts):
        """Summarize multiple contexts"""
        # Simple keyword extraction for summary
        all_text = ' '.join(contexts)
        words = re.findall(r'\b\w+\b', all_text.lower())
        word_freq = Counter(words)
        
        # Get most common meaningful words
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
        meaningful_words = [word for word, freq in word_freq.most_common(10) if word not in stop_words and len(word) > 3]
        
        return ', '.join(meaningful_words[:5])
        
    def _calculate_significance(self, events):
        """Calculate significance score for events"""
        score = 0
        
        # More files = higher significance
        file_count = len(set(event['file'] for event in events))
        score += min(file_count * 0.2, 0.4)
        
        # Financial amounts = higher significance
        total_amounts = sum(sum(event.get('amounts', [])) for event in events)
        if total_amounts > 1000000:  # R1M+
            score += 0.3
        elif total_amounts > 100000:  # R100k+
            score += 0.2
            
        # Entity involvement = higher significance
        entity_count = len(set(entity for event in events for entity in event.get('entities', [])))
        score += min(entity_count * 0.1, 0.3)
        
        return min(score, 1.0)
        
    def run_complete_analysis(self):
        """Run complete hyper-holmes analysis"""
        print("🔍 Hyper-Holmes Turbo-Solve Mode Activated")
        print("=" * 60)
        
        analysis_results = {
            'analysis_timestamp': datetime.now().isoformat(),
            'financial_patterns': self.analyze_financial_patterns(),
            'entity_relationships': self.analyze_entity_relationships(),
            'timeline_analysis': self.generate_timeline_analysis(),
            'fraud_detection': self.detect_fraud_patterns(),
            'insights': self.generate_insights(),
            'summary_statistics': {
                'total_files_analyzed': 0,
                'entities_identified': 0,
                'relationships_mapped': 0,
                'anomalies_detected': 0,
                'fraud_indicators': 0
            }
        }
        
        # Calculate summary statistics
        analysis_results['summary_statistics']['total_files_analyzed'] = len(set(
            item['file'] for pattern_list in analysis_results['financial_patterns'].values() 
            for item in pattern_list if isinstance(pattern_list, list)
        ))
        
        analysis_results['summary_statistics']['entities_identified'] = len(analysis_results['entity_relationships'])
        
        analysis_results['summary_statistics']['relationships_mapped'] = sum(
            len(relationships) for relationships in analysis_results['entity_relationships'].values()
        )
        
        analysis_results['summary_statistics']['anomalies_detected'] = sum(
            len(pattern_list) for pattern_list in analysis_results['financial_patterns'].values()
            if isinstance(pattern_list, list)
        )
        
        analysis_results['summary_statistics']['fraud_indicators'] = sum(
            1 for fraud_type in analysis_results['fraud_detection'].values()
            if fraud_type.get('detected', False)
        )
        
        # Save results
        output_file = '/home/ubuntu/analysis/hyper_holmes_analysis.json'
        with open(output_file, 'w') as f:
            json.dump(analysis_results, f, indent=2)
            
        print(f"✅ Hyper-Holmes Analysis Complete!")
        print(f"📊 Files Analyzed: {analysis_results['summary_statistics']['total_files_analyzed']}")
        print(f"🏢 Entities Identified: {analysis_results['summary_statistics']['entities_identified']}")
        print(f"🔗 Relationships Mapped: {analysis_results['summary_statistics']['relationships_mapped']}")
        print(f"⚠️ Anomalies Detected: {analysis_results['summary_statistics']['anomalies_detected']}")
        print(f"🚨 Fraud Indicators: {analysis_results['summary_statistics']['fraud_indicators']}")
        print(f"💡 Insights Generated: {len(analysis_results['insights'])}")
        print(f"💾 Results saved to: {output_file}")
        
        return analysis_results

def main():
    analyzer = HyperHolmesAnalyzer()
    return analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()
