#!/usr/bin/env python3
"""
Demonstration of Unified Legal Analysis Framework
===============================================

This script demonstrates the complete legal analysis system integrating:
1. ZA (South African) legal jurisdiction interpretation
2. UK legal jurisdiction interpretation  
3. Relevance summarization engine
4. GGML (Georgi Gerganov Machine Learning) engines
5. Cross-jurisdictional legal analysis

Specifically analyzes the Shopify payment evidence case.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from frameworks.unified_legal_analysis import UnifiedLegalAnalysisFramework
from frameworks.opencog_hgnnql import AtomSpace

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_shopify_case_data() -> dict:
    """Create structured Shopify case data based on the evidence analysis"""
    return {
        "case_title": "UK Funding SA Operations - Shopify Evidence Analysis",
        "uk_funding_sa_operations": True,
        "contradicts_debt_claims": True,
        "total_funding_amount": 77000.0,  # USD from 9+ years
        "funding_duration_years": 9,
        "invoice_count": 16,
        "payment_method": "UK Visa card ending 7147",
        "uk_company": "RegimA Worldwide Distributions Pty Ltd",
        "uk_address": "Unit 9 Southview Park, Reading, RG4 5AF, United Kingdom",
        "sa_operations": [
            {"name": "RegimA Zone SA", "monthly_cost": 54.99},
            {"name": "RegimA ZA~NE", "monthly_cost": 136.93},
            {"name": "RegimA ZA-GP~NE", "monthly_cost": 54.99},
            {"name": "ZA-GP-BH (Brenda)", "monthly_cost": 55.00}
        ],
        "evidence_strength": "irrefutable_documentary",
        "perjury_implications": True,
        "cross_border_nature": True
    }


def demonstrate_za_legal_interpretation():
    """Demonstrate South African legal jurisdiction interpretation"""
    logger.info("=== ZA Legal Jurisdiction Interpretation ===")
    
    from frameworks.za_legal_jurisdiction import ZALegalJurisdictionInterpreter
    
    za_interpreter = ZALegalJurisdictionInterpreter()
    
    # Analyze Shopify evidence under ZA law
    shopify_evidence = {
        "uk_funding_sa": True,
        "contradicts_sworn_statements": True
    }
    
    za_shopify_interpretation = za_interpreter.interpret_shopify_evidence(shopify_evidence)
    logger.info(f"ZA Shopify Interpretation: {json.dumps(za_shopify_interpretation, indent=2)}")
    
    # Analyze case facts
    case_facts = {
        "multiple_jurisdictions": True,
        "director_relationship": True,
        "financial_amount": 77000,
        "fraudulent_activity": True
    }
    
    za_analysis = za_interpreter.analyze_case_facts(case_facts)
    logger.info(f"ZA Legal Analysis Strength: {za_analysis.strength_assessment:.2f}")
    logger.info(f"ZA Legal Category: {za_analysis.legal_category.value}")
    logger.info(f"ZA Evidence Standard: {za_analysis.evidence_standard.value}")


def demonstrate_uk_legal_interpretation():
    """Demonstrate UK legal jurisdiction interpretation"""
    logger.info("\n=== UK Legal Jurisdiction Interpretation ===")
    
    from frameworks.uk_legal_jurisdiction import UKLegalJurisdictionInterpreter
    
    uk_interpreter = UKLegalJurisdictionInterpreter()
    
    # Analyze Shopify evidence under UK law
    shopify_evidence = {
        "uk_company_payments": True,
        "international_elements": True,
        "director_authorization_unclear": True
    }
    
    uk_shopify_interpretation = uk_interpreter.interpret_shopify_evidence(shopify_evidence)
    logger.info(f"UK Shopify Interpretation: {json.dumps(uk_shopify_interpretation, indent=2)}")
    
    # Analyze case facts
    case_facts = {
        "multiple_jurisdictions": True,
        "uk_company_involved": True,
        "director_relationship": True,
        "financial_amount": 77000,
        "fraudulent_activity": True
    }
    
    uk_analysis = uk_interpreter.analyze_case_facts(case_facts)
    logger.info(f"UK Legal Analysis Strength: {uk_analysis.strength_assessment:.2f}")
    logger.info(f"UK Legal Category: {uk_analysis.legal_category.value}")
    logger.info(f"UK Appropriate Court: {uk_analysis.appropriate_court.value}")


def demonstrate_relevance_summarization():
    """Demonstrate relevance summarization engine"""
    logger.info("\n=== Relevance Summarization Engine ===")
    
    from frameworks.relevance_summarizer import RelevanceSummarizer
    
    summarizer = RelevanceSummarizer()
    
    # Prepare case data for relevance analysis
    case_data = {
        "shopify_data": create_shopify_case_data(),
        "financial_evidence": {
            "total_amount": 77000,
            "transaction_count": 16,
            "source_document": "shopify_payment_flow_analysis.md"
        },
        "corporate_documents": {
            "document_types": ["invoices", "payment_records", "corporate_filings"],
            "jurisdictions": ["UK", "South Africa"],
            "source_document": "uk_funding_sa_operations_perjury_evidence.md"
        }
    }
    
    relevance_report = summarizer.generate_relevance_report(case_data)
    logger.info(f"Relevance Report Generated - Critical Items: {len(relevance_report['critical_evidence'])}")
    logger.info(f"Executive Summary: {json.dumps(relevance_report['executive_summary'], indent=2)}")


def demonstrate_ggml_legal_engine():
    """Demonstrate GGML legal analysis engine"""
    logger.info("\n=== GGML Legal Analysis Engine ===")
    
    from frameworks.ggml_legal_engine import GGMLLegalEngine
    
    engine = GGMLLegalEngine(quantization_enabled=True)
    
    # Analyze legal document
    shopify_document = """
    Documentary evidence from Shopify payment platform shows RegimA Worldwide Distributions Pty Ltd
    (UK company) consistently funding South African operations over 9+ years. Total funding exceeds
    $77,000 USD. All payments made with UK Visa card ending 7147. Evidence directly contradicts 
    sworn statements claiming UK owes money to SA operations. This constitutes material 
    misrepresentation in legal proceedings with potential perjury implications.
    """
    
    doc_analysis = engine.analyze_legal_document(shopify_document, "financial_evidence")
    logger.info(f"GGML Document Analysis: {json.dumps(doc_analysis, indent=2)}")
    
    # Cross-jurisdictional analysis
    import numpy as np
    za_features = np.array([1.0, 1.0, 0.077, 1.0, 1.0, 0.8], dtype=np.float32)  # Strong ZA case
    uk_features = np.array([1.0, 1.0, 0.077, 1.0, 1.0, 0.9], dtype=np.float32)  # Strong UK case
    
    cross_analysis = engine.cross_jurisdictional_analysis(za_features, uk_features)
    logger.info(f"GGML Cross-Jurisdictional Analysis: {json.dumps(cross_analysis, indent=2)}")
    
    # Performance stats
    perf_stats = engine.get_performance_stats()
    logger.info(f"GGML Performance Stats: {json.dumps(perf_stats, indent=2)}")


def demonstrate_unified_analysis():
    """Demonstrate the complete unified legal analysis framework"""
    logger.info("\n=== Unified Legal Analysis Framework ===")
    
    # Initialize the unified framework
    framework = UnifiedLegalAnalysisFramework(
        atomspace=AtomSpace("shopify_case_analysis"),
        enable_ggml=True,
        ggml_quantization=True
    )
    
    # Prepare comprehensive Shopify case data
    shopify_data = create_shopify_case_data()
    
    # Additional evidence
    additional_evidence = {
        "perjury_risk": True,
        "asset_recovery_potential": True,
        "international_enforcement": True,
        "evidence_quality": "documentary_proof"
    }
    
    # Perform unified analysis
    logger.info("Performing comprehensive unified analysis...")
    unified_result = framework.analyze_shopify_case(shopify_data, additional_evidence)
    
    # Generate reports
    executive_summary = unified_result.generate_executive_summary()
    detailed_report = unified_result.generate_detailed_report()
    
    logger.info("=== EXECUTIVE SUMMARY ===")
    logger.info(json.dumps(executive_summary, indent=2))
    
    logger.info("\n=== KEY FINDINGS ===")
    logger.info(f"Overall Legal Strength: {unified_result.overall_legal_strength:.2f}")
    logger.info(f"Recommended Jurisdiction: {unified_result.recommended_jurisdiction}")
    logger.info(f"ZA Analysis Strength: {unified_result.za_analysis.strength_assessment:.2f}")
    logger.info(f"UK Analysis Strength: {unified_result.uk_analysis.strength_assessment:.2f}")
    
    logger.info("\n=== PRIORITY ACTIONS ===")
    for i, action in enumerate(unified_result.priority_actions[:5], 1):
        logger.info(f"{i}. {action}")
    
    logger.info("\n=== RISK ASSESSMENT ===")
    for risk_type, risk_score in unified_result.risk_assessment.items():
        logger.info(f"{risk_type}: {risk_score:.2f}")
    
    return unified_result, detailed_report


def save_analysis_results(unified_result, detailed_report):
    """Save analysis results to files"""
    logger.info("\n=== Saving Analysis Results ===")
    
    output_dir = Path("analysis_outputs")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save executive summary
    exec_summary_file = output_dir / f"executive_summary_{timestamp}.json"
    with open(exec_summary_file, 'w') as f:
        json.dump(unified_result.generate_executive_summary(), f, indent=2)
    logger.info(f"Executive summary saved to: {exec_summary_file}")
    
    # Save detailed report
    detailed_report_file = output_dir / f"detailed_report_{timestamp}.json"
    with open(detailed_report_file, 'w') as f:
        json.dump(detailed_report, f, indent=2, default=str)
    logger.info(f"Detailed report saved to: {detailed_report_file}")
    
    # Save main conclusions
    conclusions_file = output_dir / f"main_conclusions_{timestamp}.md"
    with open(conclusions_file, 'w') as f:
        f.write(f"# Legal Analysis Main Conclusions - {timestamp}\n\n")
        f.write(f"## Analysis ID: {unified_result.analysis_id}\n\n")
        f.write(f"**Overall Legal Strength:** {unified_result.overall_legal_strength:.2f}\n\n")
        f.write(f"**Recommended Jurisdiction:** {unified_result.recommended_jurisdiction}\n\n")
        
        f.write("## Key Findings\n\n")
        for conclusion in unified_result.relevance_summary.main_conclusions:
            f.write(f"- {conclusion}\n")
        
        f.write("\n## Priority Actions\n\n")
        for i, action in enumerate(unified_result.priority_actions[:10], 1):
            f.write(f"{i}. {action}\n")
        
        f.write("\n## Jurisdictional Analysis\n\n")
        f.write(f"### South Africa\n")
        f.write(f"- **Strength:** {unified_result.za_analysis.strength_assessment:.2f}\n")
        f.write(f"- **Category:** {unified_result.za_analysis.legal_category.value}\n")
        f.write(f"- **Evidence Standard:** {unified_result.za_analysis.evidence_standard.value}\n\n")
        
        f.write(f"### United Kingdom\n")
        f.write(f"- **Strength:** {unified_result.uk_analysis.strength_assessment:.2f}\n")
        f.write(f"- **Category:** {unified_result.uk_analysis.legal_category.value}\n")
        f.write(f"- **Court Level:** {unified_result.uk_analysis.appropriate_court.value}\n\n")
    
    logger.info(f"Main conclusions saved to: {conclusions_file}")


def main():
    """Main demonstration function"""
    logger.info("Starting Legal Analysis Framework Demonstration")
    logger.info("=" * 60)
    
    try:
        # Individual component demonstrations
        demonstrate_za_legal_interpretation()
        demonstrate_uk_legal_interpretation() 
        demonstrate_relevance_summarization()
        demonstrate_ggml_legal_engine()
        
        # Unified analysis demonstration
        unified_result, detailed_report = demonstrate_unified_analysis()
        
        # Save results
        save_analysis_results(unified_result, detailed_report)
        
        logger.info("\n" + "=" * 60)
        logger.info("Legal Analysis Framework Demonstration Complete")
        logger.info(f"Analysis ID: {unified_result.analysis_id}")
        logger.info(f"Overall Legal Strength: {unified_result.overall_legal_strength:.2f}")
        logger.info(f"Recommended Approach: {unified_result.recommended_jurisdiction}")
        
    except Exception as e:
        logger.error(f"Error during demonstration: {str(e)}")
        raise


if __name__ == "__main__":
    main()