#!/usr/bin/env python3
"""
Tests for Legal Jurisdiction Analysis Components
==============================================

Tests for ZA legal jurisdiction, UK legal jurisdiction, relevance summarizer,
and GGML legal engines.
"""

import pytest
import numpy as np
from datetime import datetime
from unittest.mock import Mock, patch

# Import the modules we're testing
from frameworks.za_legal_jurisdiction import (
    ZALegalJurisdictionInterpreter, ZALegalCategory, ZAEvidenceStandard
)
from frameworks.uk_legal_jurisdiction import (
    UKLegalJurisdictionInterpreter, UKLegalCategory, UKEvidenceStandard
)
from frameworks.relevance_summarizer import (
    RelevanceSummarizer, RelevanceCategory, EvidenceType
)
from frameworks.ggml_legal_engine import (
    GGMLLegalEngine, GGMLTensorType, GGMLOperatorType
)
from frameworks.unified_legal_analysis import UnifiedLegalAnalysisFramework


class TestZALegalJurisdiction:
    """Test South African legal jurisdiction interpreter"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.za_interpreter = ZALegalJurisdictionInterpreter()
    
    def test_initialization(self):
        """Test ZA interpreter initialization"""
        assert self.za_interpreter is not None
        assert len(self.za_interpreter.legal_principles) > 0
        assert len(self.za_interpreter.inference_rules) > 0
    
    def test_shopify_evidence_interpretation(self):
        """Test interpretation of Shopify evidence under ZA law"""
        shopify_data = {
            "uk_funding_sa": True,
            "contradicts_sworn_statements": True
        }
        
        interpretation = self.za_interpreter.interpret_shopify_evidence(shopify_data)
        
        assert interpretation["jurisdiction"] == "South Africa"
        assert interpretation["evidence_weight"] >= 0.8
        assert len(interpretation["legal_implications"]) > 0
        assert len(interpretation["applicable_statutes"]) > 0
    
    def test_case_facts_analysis(self):
        """Test analysis of case facts under ZA jurisdiction"""
        case_facts = {
            "multiple_jurisdictions": True,
            "director_relationship": True,
            "financial_amount": 77000,
            "fraudulent_activity": True
        }
        
        analysis = self.za_interpreter.analyze_case_facts(case_facts)
        
        assert analysis.strength_assessment > 0.0
        assert analysis.legal_category in [cat for cat in ZALegalCategory]
        assert analysis.evidence_standard in [std for std in ZAEvidenceStandard]
        assert len(analysis.applicable_principles) > 0
        assert len(analysis.recommended_actions) > 0
    
    def test_fiduciary_duty_principle(self):
        """Test fiduciary duty principle evaluation"""
        case_facts = {
            "director_relationship": True,
            "company_involved": True,
            "financial_decision_making": True
        }
        
        # Find fiduciary duty principle
        fiduciary_principle = None
        for principle in self.za_interpreter.legal_principles:
            if principle.principle_id == "za_fiduciary_duty":
                fiduciary_principle = principle
                break
        
        assert fiduciary_principle is not None
        applicability = fiduciary_principle.evaluate_applicability(case_facts)
        assert applicability > 0.5


class TestUKLegalJurisdiction:
    """Test UK legal jurisdiction interpreter"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.uk_interpreter = UKLegalJurisdictionInterpreter()
    
    def test_initialization(self):
        """Test UK interpreter initialization"""
        assert self.uk_interpreter is not None
        assert len(self.uk_interpreter.legal_principles) > 0
        assert len(self.uk_interpreter.inference_rules) > 0
    
    def test_shopify_evidence_interpretation(self):
        """Test interpretation of Shopify evidence under UK law"""
        shopify_data = {
            "uk_company_payments": True,
            "international_elements": True,
            "director_authorization_unclear": True
        }
        
        interpretation = self.uk_interpreter.interpret_shopify_evidence(shopify_data)
        
        assert interpretation["jurisdiction"] == "United Kingdom"
        assert interpretation["evidence_weight"] >= 0.7
        assert len(interpretation["legal_implications"]) > 0
        assert len(interpretation["applicable_statutes"]) > 0
        assert len(interpretation["procedural_considerations"]) > 0
    
    def test_case_facts_analysis(self):
        """Test analysis of case facts under UK jurisdiction"""
        case_facts = {
            "multiple_jurisdictions": True,
            "uk_company_involved": True,
            "director_relationship": True,
            "financial_amount": 77000,
            "fraudulent_activity": True
        }
        
        analysis = self.uk_interpreter.analyze_case_facts(case_facts)
        
        assert analysis.strength_assessment > 0.0
        assert analysis.legal_category in [cat for cat in UKLegalCategory]
        assert analysis.evidence_standard in [std for std in UKEvidenceStandard]
        assert len(analysis.applicable_principles) > 0
        assert len(analysis.recommended_actions) > 0
    
    def test_directors_duties_principle(self):
        """Test directors' duties principle evaluation"""
        case_facts = {
            "director_relationship": True,
            "uk_company": True,
            "breach_of_duty": True
        }
        
        # Find directors' duties principle
        directors_principle = None
        for principle in self.uk_interpreter.legal_principles:
            if principle.principle_id == "uk_directors_duties":
                directors_principle = principle
                break
        
        assert directors_principle is not None
        applicability = directors_principle.evaluate_applicability(case_facts)
        assert applicability > 0.5


class TestRelevanceSummarizer:
    """Test relevance summarization engine"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.summarizer = RelevanceSummarizer()
    
    def test_initialization(self):
        """Test summarizer initialization"""
        assert self.summarizer is not None
        assert self.summarizer.za_interpreter is not None
        assert self.summarizer.uk_interpreter is not None
    
    def test_shopify_evidence_analysis(self):
        """Test analysis of Shopify evidence for relevance"""
        shopify_data = {
            "uk_funding_sa_operations": True,
            "contradicts_debt_claims": True,
            "total_funding_amount": 77000,
            "funding_duration_years": 9
        }
        
        relevance_item = self.summarizer.analyze_shopify_evidence(shopify_data)
        
        assert relevance_item.evidence_type == EvidenceType.DOCUMENTARY
        assert relevance_item.relevance_score.overall_score > 0.7
        assert relevance_item.relevance_score.get_category() in [
            RelevanceCategory.CRITICAL, RelevanceCategory.HIGH
        ]
        assert len(relevance_item.supporting_facts) > 0
        assert len(relevance_item.legal_implications) > 0
    
    def test_cross_jurisdictional_analysis(self):
        """Test comprehensive cross-jurisdictional analysis"""
        case_data = {
            "shopify_data": {
                "uk_funding_sa_operations": True,
                "contradicts_debt_claims": True,
                "total_funding_amount": 77000,
                "funding_duration_years": 9,
                "invoice_count": 16
            },
            "financial_evidence": {
                "total_amount": 77000,
                "transaction_count": 16
            },
            "corporate_documents": {
                "document_types": ["invoices", "payment_records"],
                "jurisdictions": ["UK", "South Africa"]
            }
        }
        
        summary = self.summarizer.analyze_cross_jurisdictional_case(case_data)
        
        assert summary.analysis_timestamp is not None
        assert len(summary.critical_items) >= 0
        assert len(summary.high_relevance_items) >= 0
        assert len(summary.main_conclusions) > 0
        assert len(summary.recommended_actions) > 0
    
    def test_relevance_report_generation(self):
        """Test generation of comprehensive relevance report"""
        case_data = {
            "shopify_data": {
                "uk_funding_sa_operations": True,
                "contradicts_debt_claims": True,
                "total_funding_amount": 77000
            }
        }
        
        report = self.summarizer.generate_relevance_report(case_data)
        
        assert "executive_summary" in report
        assert "critical_evidence" in report
        assert "jurisdictional_analysis" in report
        assert "south_africa" in report["jurisdictional_analysis"]
        assert "united_kingdom" in report["jurisdictional_analysis"]


class TestGGMLLegalEngine:
    """Test GGML legal analysis engine"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.engine = GGMLLegalEngine(quantization_enabled=True)
    
    def test_initialization(self):
        """Test GGML engine initialization"""
        assert self.engine is not None
        assert self.engine.quantization_enabled is True
        assert len(self.engine.operators) > 0
    
    def test_tensor_creation_and_quantization(self):
        """Test tensor creation and quantization"""
        data = np.random.rand(5, 10).astype(np.float32)
        tensor = self.engine.create_tensor(
            "test_tensor",
            GGMLTensorType.LEGAL_DOCUMENT,
            data.shape,
            data
        )
        
        assert tensor.name == "test_tensor"
        assert tensor.tensor_type == GGMLTensorType.LEGAL_DOCUMENT
        assert tensor.quantized is True  # Should be quantized due to engine settings
    
    def test_legal_document_analysis(self):
        """Test legal document analysis"""
        document = "This is a legal document discussing fraudulent financial transactions and fiduciary duties."
        
        analysis = self.engine.analyze_legal_document(document, "financial_evidence")
        
        assert "relevance_score" in analysis
        assert "legal_significance" in analysis
        assert "evidence_strength" in analysis
        assert analysis["ggml_optimized"] is True
        assert 0.0 <= analysis["relevance_score"] <= 1.0
    
    def test_cross_jurisdictional_analysis(self):
        """Test cross-jurisdictional analysis with GGML"""
        za_features = np.array([0.9, 0.8, 0.7, 0.9, 0.8, 0.8], dtype=np.float32)
        uk_features = np.array([0.8, 0.9, 0.7, 0.9, 0.7, 0.9], dtype=np.float32)
        
        analysis = self.engine.cross_jurisdictional_analysis(za_features, uk_features)
        
        assert "merged_score" in analysis
        assert "za_contribution" in analysis
        assert "uk_contribution" in analysis
        assert "cross_jurisdictional_strength" in analysis
        assert analysis["ggml_optimized"] is True
    
    def test_fraud_pattern_detection(self):
        """Test fraud pattern detection"""
        document_features = np.array([1.0, 0.9, 0.8, 0.7, 0.95, 0.8], dtype=np.float32)
        known_patterns = [
            np.array([0.9, 0.8, 0.7, 0.6, 0.9, 0.8], dtype=np.float32),
            np.array([0.8, 0.9, 0.6, 0.8, 0.7, 0.9], dtype=np.float32)
        ]
        
        result = self.engine.detect_fraud_patterns(document_features, known_patterns)
        
        assert "fraud_detected" in result
        assert "confidence_score" in result
        assert "all_pattern_matches" in result
        assert isinstance(result["fraud_detected"], bool)
        assert 0.0 <= result["confidence_score"] <= 1.0
    
    def test_performance_stats(self):
        """Test performance statistics retrieval"""
        stats = self.engine.get_performance_stats()
        
        assert "total_tensors" in stats
        assert "quantized_tensors" in stats
        assert "quantization_ratio" in stats
        assert "total_memory_bytes" in stats
        assert "operators_available" in stats


class TestUnifiedLegalAnalysis:
    """Test unified legal analysis framework"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.framework = UnifiedLegalAnalysisFramework(
            enable_ggml=True,
            ggml_quantization=True
        )
    
    def test_initialization(self):
        """Test framework initialization"""
        assert self.framework is not None
        assert self.framework.za_interpreter is not None
        assert self.framework.uk_interpreter is not None
        assert self.framework.relevance_summarizer is not None
        assert self.framework.ggml_enabled is True
        assert self.framework.ggml_engine is not None
    
    def test_shopify_case_analysis(self):
        """Test comprehensive Shopify case analysis"""
        shopify_data = {
            "uk_funding_sa_operations": True,
            "contradicts_debt_claims": True,
            "total_funding_amount": 77000,
            "funding_duration_years": 9,
            "invoice_count": 16
        }
        
        additional_evidence = {
            "perjury_risk": True,
            "asset_recovery_potential": True
        }
        
        result = self.framework.analyze_shopify_case(shopify_data, additional_evidence)
        
        # Check result structure
        assert result.analysis_id is not None
        assert result.za_analysis is not None
        assert result.uk_analysis is not None
        assert result.relevance_summary is not None
        assert 0.0 <= result.overall_legal_strength <= 1.0
        assert result.recommended_jurisdiction is not None
        assert len(result.priority_actions) > 0
        assert len(result.risk_assessment) > 0
    
    def test_executive_summary_generation(self):
        """Test executive summary generation"""
        shopify_data = {
            "uk_funding_sa_operations": True,
            "contradicts_debt_claims": True,
            "total_funding_amount": 77000
        }
        
        result = self.framework.analyze_shopify_case(shopify_data)
        summary = result.generate_executive_summary()
        
        assert "analysis_id" in summary
        assert "overall_legal_strength" in summary
        assert "recommended_jurisdiction" in summary
        assert "za_strength" in summary
        assert "uk_strength" in summary
        assert "priority_actions" in summary
        assert "risk_scores" in summary
    
    def test_detailed_report_generation(self):
        """Test detailed report generation"""
        shopify_data = {
            "uk_funding_sa_operations": True,
            "contradicts_debt_claims": True,
            "total_funding_amount": 77000
        }
        
        result = self.framework.analyze_shopify_case(shopify_data)
        detailed_report = result.generate_detailed_report()
        
        assert "executive_summary" in detailed_report
        assert "jurisdictional_analysis" in detailed_report
        assert "relevance_analysis" in detailed_report
        assert "ggml_analysis" in detailed_report
        assert "integrated_findings" in detailed_report
        assert "actionable_recommendations" in detailed_report
    
    @patch('frameworks.unified_legal_analysis.Path')
    def test_shopify_evidence_interpretation(self, mock_path):
        """Test comprehensive Shopify evidence interpretation"""
        interpretation = self.framework.interpret_shopify_evidence_comprehensive(
            "shopify_payment_flow_analysis.md"
        )
        
        assert "za_jurisdiction" in interpretation
        assert "uk_jurisdiction" in interpretation
        assert "unified_assessment" in interpretation
        
        # Check ZA jurisdiction interpretation
        za_interp = interpretation["za_jurisdiction"]
        assert za_interp["jurisdiction"] == "South Africa"
        
        # Check UK jurisdiction interpretation
        uk_interp = interpretation["uk_jurisdiction"]
        assert uk_interp["jurisdiction"] == "United Kingdom"
        
        # Check unified assessment
        unified = interpretation["unified_assessment"]
        assert unified["evidence_type"] == "documentary"
        assert unified["cross_border_implications"] is True


# Integration tests
class TestLegalAnalysisIntegration:
    """Integration tests for the complete legal analysis system"""
    
    def test_end_to_end_shopify_analysis(self):
        """Test complete end-to-end Shopify case analysis"""
        # Initialize framework
        framework = UnifiedLegalAnalysisFramework(
            enable_ggml=True,
            ggml_quantization=False  # Disable for faster testing
        )
        
        # Prepare test data
        shopify_data = {
            "uk_funding_sa_operations": True,
            "contradicts_debt_claims": True,
            "total_funding_amount": 77000,
            "funding_duration_years": 9,
            "invoice_count": 16,
            "payment_method": "UK Visa card ending 7147"
        }
        
        # Run analysis
        result = framework.analyze_shopify_case(shopify_data)
        
        # Verify comprehensive results
        assert result.overall_legal_strength > 0.5  # Should be strong case
        assert result.za_analysis.strength_assessment > 0.0
        assert result.uk_analysis.strength_assessment > 0.0
        assert len(result.relevance_summary.critical_items) > 0
        assert result.recommended_jurisdiction in [
            "za_primary", "uk_primary", "parallel_proceedings"
        ]
        
        # Verify GGML analysis was performed
        assert result.ggml_document_analysis is not None
        assert result.ggml_cross_jurisdictional is not None
        assert result.ggml_fraud_detection is not None
        
        # Verify risk assessment
        assert "enforcement_risk" in result.risk_assessment
        assert "fraud_detection_confidence" in result.risk_assessment
        
        # Verify actionable outputs
        assert len(result.priority_actions) >= 3
        
        # Test report generation
        executive_summary = result.generate_executive_summary()
        detailed_report = result.generate_detailed_report()
        
        assert executive_summary is not None
        assert detailed_report is not None
        assert len(detailed_report) >= 6  # Should have main sections


if __name__ == "__main__":
    pytest.main([__file__, "-v"])