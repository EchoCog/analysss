#!/usr/bin/env python3
"""
Enhanced Verification Integration Script
=======================================

Integrates document significance analysis with the interdict verification system
to provide comprehensive case assessment including document-specific findings.
"""

import json
from datetime import datetime
from pathlib import Path
import sys

# Add tools directory to path
sys.path.append(str(Path(__file__).parent / "tools"))

from interdict_verification_system import (
    InterdictVerificationSystem,
    EvidenceItem,
    InterdicClaim,
    ClaimType,
    VerificationLevel
)
from document_significance_analyzer import DocumentSignificanceAnalyzer


def enhance_verification_with_document_analysis(case_number: str = "2025-137857"):
    """
    Enhance the interdict verification system with document significance analysis
    """
    print("=== Enhanced Verification Integration ===")
    print(f"Case: {case_number}")
    print()
    
    # Initialize both systems
    verifier = InterdictVerificationSystem(case_number)
    doc_analyzer = DocumentSignificanceAnalyzer(case_number)
    
    # Load existing document significance analysis if available
    significance_path = doc_analyzer.case_path / "document_significance_analysis" / "significance_analysis.json"
    
    if significance_path.exists():
        print("📄 Loading existing document significance analysis...")
        with open(significance_path) as f:
            significance_data = json.load(f)
        print(f"✅ Loaded analysis for {len(significance_data)} document groups")
    else:
        print("⚠️  No existing document significance analysis found")
        print("   Run 'python tools/document_significance_analyzer.py' first")
        return
    
    # Set up court metadata for verification system
    from interdict_verification_system import CourtOrderMetadata
    
    court_metadata = CourtOrderMetadata(
        case_number=case_number,
        court_name="High Court of South Africa, Gauteng Division, Pretoria",
        judge_name="Justice Kumalo J",
        order_date=datetime(2025, 8, 19),
        document_hash="placeholder_hash",
        filing_verified=False,  # To be verified based on document analysis
        service_verified=False,  # To be verified
        legal_representation_verified=True,  # Verified but status changed per MAT4719
        jurisdiction_verified=True,
    )
    verifier.set_court_metadata(court_metadata)
    
    print("🔗 Integrating document significance findings...")
    
    # Process each document's significance and create corresponding claims/evidence
    for doc_name, doc_data in significance_data.items():
        print(f"   Processing: {doc_name}")
        
        # Create evidence item for the document significance finding
        evidence_id = f"doc_sig_{doc_name.replace(' ', '_').replace('.', '_').replace('-', '_')}"
        
        evidence_item = EvidenceItem(
            evidence_id=evidence_id,
            source_document=doc_name,
            page_reference="Document Significance Analysis",
            content_summary=f"Document significance: {doc_data['significance_level']}. " +
                          (doc_data['legal_implications'][0] if doc_data['legal_implications'] else ""),
            reliability_score=0.95,
            verification_date=datetime.fromisoformat(doc_data['analysis_date']),
            verifier="Document Significance Analyzer"
        )
        
        verifier.add_evidence(evidence_item)
        
        # Create claims based on document significance
        if doc_data['document_type'] == 'procedural' and doc_data['significance_level'] == 'critical':
            # Create procedural concern claim
            claim_id = f"procedural_concern_{doc_name.replace(' ', '_').replace('.', '_')}"
            
            if "MAT4719" in doc_name:
                # Specific concern about attorney withdrawal
                claim = InterdicClaim(
                    claim_id=claim_id,
                    claim_type=ClaimType.PROCEDURAL,
                    section_reference="Attorney Representation",
                    claim_text="Attorney withdrawal during active interdict proceedings may affect procedural compliance",
                    verification_notes=doc_data['procedural_impact'],
                    legal_basis_verified=False,  # Needs verification
                    procedural_compliance=False  # Concern identified
                )
                
                verifier.add_claim(claim)
                verifier.link_evidence_to_claim(claim_id, evidence_id, supports=True)
                
            elif "KF0019" in doc_name:
                # Specific concern about multiple applications
                claim = InterdicClaim(
                    claim_id=claim_id,
                    claim_type=ClaimType.PROCEDURAL,
                    section_reference="Application Filing",
                    claim_text="Second application filing suggests potential procedural defects in initial application",
                    verification_notes=doc_data['procedural_impact'],
                    legal_basis_verified=False,
                    procedural_compliance=False
                )
                
                verifier.add_claim(claim)
                verifier.link_evidence_to_claim(claim_id, evidence_id, supports=True)
                
                # Flag this as requiring urgent verification
                verifier.flag_impossible_claim(
                    claim_id, 
                    "Multiple applications without explanation of defects cured"
                )
        
        elif doc_data['document_type'] == 'financial' and 'BANK_RECORDS' in doc_name:
            # Create financial evidence verification claim
            claim_id = "bank_records_financial_verification"
            
            if claim_id not in verifier.claims:
                claim = InterdicClaim(
                    claim_id=claim_id,
                    claim_type=ClaimType.FINANCIAL,
                    section_reference="Financial Evidence",
                    claim_text="Personal bank records provide critical evidence for R500K and R8.8M financial misconduct allegations",
                    alleged_amount=8854166.94,  # R8.8M + R500K total concerns
                    verification_notes=doc_data['evidence_value']
                )
                
                verifier.add_claim(claim)
            
            # Link this document's evidence to the financial claim
            verifier.link_evidence_to_claim(claim_id, evidence_id, supports=True)
    
    # Generate enhanced verification report
    print("\n📊 Generating enhanced verification report...")
    
    report = verifier.generate_verification_report()
    
    # Add document significance summary to report
    doc_summary = generate_document_significance_summary(significance_data)
    enhanced_report = report + "\n\n" + doc_summary
    
    # Save enhanced report
    case_path = Path(__file__).parent / f"case_{case_number.replace('-', '_')}"
    enhanced_report_path = case_path / "enhanced_verification_report.md"
    
    with open(enhanced_report_path, 'w') as f:
        f.write(enhanced_report)
    
    print(f"📄 Enhanced report saved to: {enhanced_report_path}")
    
    # Generate updated verification checklist
    print("\n📋 Generating enhanced verification checklist...")
    
    checklist = verifier.generate_verification_checklist()
    
    # Add document-specific verification items
    doc_checklist = generate_document_verification_checklist(significance_data)
    enhanced_checklist = checklist + "\n\n" + doc_checklist
    
    checklist_path = case_path / "enhanced_verification_checklist.md"
    
    with open(checklist_path, 'w') as f:
        f.write(enhanced_checklist)
    
    print(f"📋 Enhanced checklist saved to: {checklist_path}")
    
    # Print summary
    print("\n=== INTEGRATION SUMMARY ===")
    print(f"✅ Processed {len(significance_data)} document groups")
    print(f"📊 Total claims in verification system: {len(verifier.claims)}")
    print(f"🔍 Total evidence items: {len(verifier.evidence_repository)}")
    print(f"⚠️  Verification requirements: {len(verifier.verification_requirements)}")
    
    # Show claim summary by verification level
    verification_levels = {}
    for claim in verifier.claims.values():
        level = claim.verification_level.value
        verification_levels[level] = verification_levels.get(level, 0) + 1
    
    print("\n📈 Claim Verification Status:")
    for level, count in verification_levels.items():
        print(f"   {level.title()}: {count}")
    
    return verifier, enhanced_report_path, checklist_path


def generate_document_significance_summary(significance_data: dict) -> str:
    """Generate summary section for document significance analysis"""
    
    lines = [
        "## 📄 DOCUMENT SIGNIFICANCE ANALYSIS INTEGRATION",
        "",
        f"**Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Documents Analyzed**: {len(significance_data)}",
        ""
    ]
    
    # Count by significance level
    significance_counts = {}
    document_types = {}
    
    for doc_data in significance_data.values():
        level = doc_data['significance_level']
        doc_type = doc_data['document_type']
        
        significance_counts[level] = significance_counts.get(level, 0) + 1
        document_types[doc_type] = document_types.get(doc_type, 0) + 1
    
    lines.extend([
        "### Significance Level Distribution",
        f"- **Critical**: {significance_counts.get('critical', 0)} documents",
        f"- **High**: {significance_counts.get('high', 0)} documents", 
        f"- **Medium**: {significance_counts.get('medium', 0)} documents",
        f"- **Low**: {significance_counts.get('low', 0)} documents",
        "",
        "### Document Type Distribution",
        f"- **Procedural**: {document_types.get('procedural', 0)} documents",
        f"- **Financial**: {document_types.get('financial', 0)} documents",
        f"- **Legal Strategy**: {document_types.get('legal_strategy', 0)} documents",
        "",
        "### Key Verification Impact",
        "- **Procedural Compliance**: Attorney withdrawal and multiple applications raise concerns",
        "- **Financial Evidence**: Bank records provide critical verification opportunity for R8.8M claims",
        "- **Timeline Integrity**: Document dates require cross-validation with case timeline",
        "- **Case Legitimacy**: Pattern of procedural issues affects overall legitimacy assessment",
        ""
    ])
    
    return "\n".join(lines)


def generate_document_verification_checklist(significance_data: dict) -> str:
    """Generate document-specific verification checklist items"""
    
    lines = [
        "## 📄 DOCUMENT-SPECIFIC VERIFICATION CHECKLIST",
        "",
        "### Procedural Document Verification",
        ""
    ]
    
    for doc_name, doc_data in significance_data.items():
        if doc_data['document_type'] == 'procedural':
            lines.extend([
                f"#### {doc_name}",
                *[f"- [ ] {req}" for req in doc_data['verification_requirements']],
                ""
            ])
    
    lines.extend([
        "### Financial Evidence Verification",
        ""
    ])
    
    for doc_name, doc_data in significance_data.items():
        if doc_data['document_type'] == 'financial':
            lines.extend([
                f"#### {doc_name}",
                *[f"- [ ] {req}" for req in doc_data['verification_requirements']], 
                ""
            ])
    
    lines.extend([
        "### Legal Strategy Analysis",
        ""
    ])
    
    for doc_name, doc_data in significance_data.items():
        if doc_data['document_type'] == 'legal_strategy':
            lines.extend([
                f"#### {doc_name}",
                *[f"- [ ] {req}" for req in doc_data['verification_requirements']],
                ""
            ])
    
    return "\n".join(lines)


def main():
    """Main function"""
    try:
        verifier, report_path, checklist_path = enhance_verification_with_document_analysis()
        
        print("\n🎉 Enhanced verification integration complete!")
        print(f"📊 Enhanced report: {report_path}")
        print(f"📋 Enhanced checklist: {checklist_path}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during integration: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())