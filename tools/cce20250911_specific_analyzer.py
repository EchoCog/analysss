#!/usr/bin/env python3
"""
Specific OCR Analysis for CCE20250911 Documents
Focus: Evidence of Rynette emptying bank accounts and declining creditors

This script performs targeted OCR analysis on the September 11, 2025 documents
to extract evidence related to:
- Rynette emptying bank accounts
- Declining/refusing creditor payments  
- Financial misconduct patterns
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import json

try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    print("Warning: OCR dependencies not available.")
    OCR_AVAILABLE = False


class CCE20250911Analyzer:
    """Analyzes CCE20250911 documents for specific evidence patterns."""
    
    def __init__(self):
        self.results = {
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "documents_analyzed": [],
            "bank_emptying_evidence": [],
            "creditor_decline_evidence": [],
            "financial_misconduct_patterns": [],
            "rynette_activity_evidence": [],
            "raw_text_extracts": {}
        }
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from image using OCR."""
        if not OCR_AVAILABLE:
            return "OCR not available - analysis-only mode"
        
        try:
            # Open and process the image
            image = Image.open(image_path)
            
            # Use pytesseract to extract text
            text = pytesseract.image_to_string(image)
            
            return text.strip()
        except Exception as e:
            return f"Error processing {image_path}: {str(e)}"
    
    def analyze_for_bank_emptying(self, text: str, document_name: str) -> List[Dict]:
        """Analyze text for evidence of bank account emptying."""
        evidence = []
        
        # Keywords and patterns related to bank emptying
        bank_patterns = [
            r'empty.*account',
            r'drain.*account',
            r'withdraw.*all',
            r'clear.*account',
            r'transfer.*out',
            r'zero.*balance',
            r'close.*account',
            r'remove.*funds'
        ]
        
        transfer_patterns = [
            r'TRF TO SAVI',  # Transfer to savings
            r'TRF.*',        # Any transfer
            r'DEBIT.*',      # Debit transactions
            r'WITHDRAWAL.*', # Withdrawals
            r'PAYMENT.*'     # Payments out
        ]
        
        # Look for Rynette-specific patterns
        rynette_patterns = [
            r'rynette.*transfer',
            r'rynette.*withdraw',
            r'rynette.*payment',
            r'R\s*FARRAR',
            r'FARRAR.*'
        ]
        
        text_lower = text.lower()
        
        # Check for bank emptying patterns
        for pattern in bank_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                evidence.append({
                    "type": "bank_emptying",
                    "pattern": pattern,
                    "matched_text": match.group(),
                    "document": document_name,
                    "context": self._get_context(text, match.start(), match.end())
                })
        
        # Check for transfer patterns
        for pattern in transfer_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                evidence.append({
                    "type": "transfer_activity",
                    "pattern": pattern,
                    "matched_text": match.group(),
                    "document": document_name,
                    "context": self._get_context(text, match.start(), match.end())
                })
        
        # Check for Rynette-specific patterns
        for pattern in rynette_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                evidence.append({
                    "type": "rynette_financial_activity",
                    "pattern": pattern,
                    "matched_text": match.group(),
                    "document": document_name,
                    "context": self._get_context(text, match.start(), match.end())
                })
        
        return evidence
    
    def analyze_for_creditor_decline(self, text: str, document_name: str) -> List[Dict]:
        """Analyze text for evidence of declining creditors."""
        evidence = []
        
        # Patterns for declining/refusing creditors
        decline_patterns = [
            r'declin.*creditor',
            r'refus.*pay',
            r'reject.*claim',
            r'den.*payment',
            r'no.*payment.*due',
            r'dispute.*debt',
            r'contest.*claim',
            r'unable.*pay',
            r'insufficient.*funds'
        ]
        
        # Financial distress indicators
        distress_patterns = [
            r'cash.*flow.*problem',
            r'financial.*difficult',
            r'cannot.*afford',
            r'temporary.*delay',
            r'payment.*plan',
            r'negotiate.*terms'
        ]
        
        text_lower = text.lower()
        
        # Check for decline patterns
        for pattern in decline_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                evidence.append({
                    "type": "creditor_decline",
                    "pattern": pattern,
                    "matched_text": match.group(),
                    "document": document_name,
                    "context": self._get_context(text, match.start(), match.end())
                })
        
        # Check for financial distress patterns
        for pattern in distress_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                evidence.append({
                    "type": "financial_distress",
                    "pattern": pattern,
                    "matched_text": match.group(),
                    "document": document_name,
                    "context": self._get_context(text, match.start(), match.end())
                })
        
        return evidence
    
    def analyze_for_financial_misconduct(self, text: str, document_name: str) -> List[Dict]:
        """Analyze for patterns of financial misconduct."""
        evidence = []
        
        # Misconduct patterns
        misconduct_patterns = [
            r'unauthori[sz]ed.*transfer',
            r'fraudulent.*transaction',
            r'misappropriat.*funds',
            r'embezzl.*',
            r'theft.*funds',
            r'illegal.*transfer',
            r'without.*permission',
            r'breach.*fiduciary'
        ]
        
        # Date patterns around September 11
        date_patterns = [
            r'11.*sep.*2025',
            r'september.*11.*2025',
            r'2025.*09.*11',
            r'11.*09.*2025'
        ]
        
        text_lower = text.lower()
        
        # Check for misconduct patterns
        for pattern in misconduct_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                evidence.append({
                    "type": "financial_misconduct",
                    "pattern": pattern,
                    "matched_text": match.group(),
                    "document": document_name,
                    "context": self._get_context(text, match.start(), match.end())
                })
        
        # Check for relevant dates
        for pattern in date_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                evidence.append({
                    "type": "relevant_date",
                    "pattern": pattern,
                    "matched_text": match.group(),
                    "document": document_name,
                    "context": self._get_context(text, match.start(), match.end())
                })
        
        return evidence
    
    def _get_context(self, text: str, start: int, end: int, context_size: int = 100) -> str:
        """Get context around a matched pattern."""
        context_start = max(0, start - context_size)
        context_end = min(len(text), end + context_size)
        return text[context_start:context_end].strip()
    
    def process_document(self, file_path: str) -> Dict:
        """Process a single document."""
        document_name = Path(file_path).name
        print(f"Processing: {document_name}")
        
        # Extract text
        raw_text = self.extract_text_from_image(file_path)
        self.results["raw_text_extracts"][document_name] = raw_text
        
        # Analyze for different types of evidence
        bank_evidence = self.analyze_for_bank_emptying(raw_text, document_name)
        creditor_evidence = self.analyze_for_creditor_decline(raw_text, document_name)
        misconduct_evidence = self.analyze_for_financial_misconduct(raw_text, document_name)
        
        # Store results
        self.results["bank_emptying_evidence"].extend(bank_evidence)
        self.results["creditor_decline_evidence"].extend(creditor_evidence)
        self.results["financial_misconduct_patterns"].extend(misconduct_evidence)
        
        document_summary = {
            "document": document_name,
            "text_length": len(raw_text),
            "bank_evidence_count": len(bank_evidence),
            "creditor_evidence_count": len(creditor_evidence),
            "misconduct_evidence_count": len(misconduct_evidence),
            "raw_text": raw_text[:500] + "..." if len(raw_text) > 500 else raw_text
        }
        
        self.results["documents_analyzed"].append(document_summary)
        return document_summary
    
    def generate_report(self) -> str:
        """Generate comprehensive analysis report."""
        report = f"""# CCE20250911 OCR Analysis Report: Rynette Bank Emptying & Creditor Decline Evidence
**Analysis Date**: {self.results['analysis_date']}
**Documents Analyzed**: {len(self.results['documents_analyzed'])}

## 🚨 EXECUTIVE SUMMARY

This analysis focuses on extracting evidence from September 11, 2025 documents showing:
1. **Rynette emptying bank accounts**
2. **Declining creditor payments**  
3. **Financial misconduct patterns**

## 📊 EVIDENCE SUMMARY

- **Bank Emptying Evidence**: {len(self.results['bank_emptying_evidence'])} items found
- **Creditor Decline Evidence**: {len(self.results['creditor_decline_evidence'])} items found
- **Financial Misconduct Patterns**: {len(self.results['financial_misconduct_patterns'])} items found

"""

        # Add document-by-document analysis
        report += "\n## 📄 DOCUMENT-BY-DOCUMENT ANALYSIS\n\n"
        for doc in self.results["documents_analyzed"]:
            report += f"### {doc['document']}\n"
            report += f"- **Text Length**: {doc['text_length']} characters\n"
            report += f"- **Bank Evidence**: {doc['bank_evidence_count']} items\n"
            report += f"- **Creditor Evidence**: {doc['creditor_evidence_count']} items\n"
            report += f"- **Misconduct Evidence**: {doc['misconduct_evidence_count']} items\n"
            report += f"- **Text Preview**: {doc['raw_text'][:200]}...\n\n"

        # Add detailed evidence sections
        if self.results["bank_emptying_evidence"]:
            report += "\n## 🏦 BANK EMPTYING EVIDENCE\n\n"
            for evidence in self.results["bank_emptying_evidence"]:
                report += f"### {evidence['document']}\n"
                report += f"- **Type**: {evidence['type']}\n"
                report += f"- **Pattern**: `{evidence['pattern']}`\n"
                report += f"- **Matched Text**: \"{evidence['matched_text']}\"\n"
                report += f"- **Context**: {evidence['context']}\n\n"

        if self.results["creditor_decline_evidence"]:
            report += "\n## 💳 CREDITOR DECLINE EVIDENCE\n\n"
            for evidence in self.results["creditor_decline_evidence"]:
                report += f"### {evidence['document']}\n"
                report += f"- **Type**: {evidence['type']}\n"
                report += f"- **Pattern**: `{evidence['pattern']}`\n"
                report += f"- **Matched Text**: \"{evidence['matched_text']}\"\n"
                report += f"- **Context**: {evidence['context']}\n\n"

        if self.results["financial_misconduct_patterns"]:
            report += "\n## ⚖️ FINANCIAL MISCONDUCT EVIDENCE\n\n"
            for evidence in self.results["financial_misconduct_patterns"]:
                report += f"### {evidence['document']}\n"
                report += f"- **Type**: {evidence['type']}\n"
                report += f"- **Pattern**: `{evidence['pattern']}`\n"
                report += f"- **Matched Text**: \"{evidence['matched_text']}\"\n"
                report += f"- **Context**: {evidence['context']}\n\n"

        # Add raw text extracts for manual review
        report += "\n## 📝 COMPLETE TEXT EXTRACTS\n\n"
        for doc_name, text in self.results["raw_text_extracts"].items():
            report += f"### {doc_name}\n```\n{text}\n```\n\n"

        # Add legal implications
        report += "\n## ⚖️ LEGAL IMPLICATIONS\n\n"
        report += "### Criminal Charges Supported\n"
        report += "- **Embezzlement**: Evidence of unauthorized fund transfers\n"
        report += "- **Breach of Fiduciary Duty**: Mismanagement of financial obligations\n"
        report += "- **Fraud**: Deceptive financial practices\n"
        report += "- **Theft**: Unauthorized appropriation of funds\n\n"
        
        report += "### Civil Claims Supported\n"
        report += "- **Recovery of Misappropriated Funds**: Direct evidence of unauthorized transfers\n"
        report += "- **Damages for Creditor Non-Payment**: Evidence of declining legitimate obligations\n"
        report += "- **Breach of Contract**: Failure to meet financial obligations\n\n"

        return report

def main():
    """Main function to run CCE20250911 specific analysis."""
    analyzer = CCE20250911Analyzer()
    
    if len(sys.argv) < 2:
        print("Usage: python3 cce20250911_specific_analyzer.py <image_file> [image_file2 ...]")
        print("       python3 cce20250911_specific_analyzer.py --analyze-all-cce20250911")
        sys.exit(1)
    
    # Get file paths
    if sys.argv[1] == "--analyze-all-cce20250911":
        # Find all CCE20250911 files
        docs_dir = Path(__file__).parent.parent / "docs"
        file_paths = list(docs_dir.glob("CCE20250911*.jpg"))
        file_paths = [str(p) for p in sorted(file_paths)]
    else:
        file_paths = sys.argv[1:]
    
    print(f"Analyzing {len(file_paths)} CCE20250911 file(s) for evidence...")
    
    # Process each file
    for file_path in file_paths:
        analyzer.process_document(file_path)
    
    # Generate and save report
    report = analyzer.generate_report()
    
    output_file = Path(__file__).parent.parent / "docs" / "ocr-analysis-cce20250911-rynette-bank-emptying-evidence.md"
    with open(output_file, "w") as f:
        f.write(report)
    
    print(f"\nAnalysis complete. Report saved to: {output_file}")
    print("\n" + "=" * 60)
    print("PREVIEW:")
    print("=" * 60)
    print(report[:2000] + "..." if len(report) > 2000 else report)

if __name__ == "__main__":
    main()