#!/usr/bin/env python3
"""
Tests for Medical Testing Agreement Analyzer

Validates the comprehensive analysis tool that integrates forensic linguistic analysis 
with citizenship capacity assessment for medical testing settlement agreements.
"""

import pytest
import sys
import os
from pathlib import Path
from datetime import datetime

# Add the tools directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../tools'))

from medical_testing_agreement_analyzer import (
    MedicalTestingAgreementAnalyzer,
    ForensicFinding,
    MedicalTestingAnalysis
)
from citizenship_settlement_analyzer import CitizenshipProfile, CitizenshipStatus


class TestMedicalTestingAgreementAnalyzer:
    """Test suite for Medical Testing Agreement Analyzer"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.analyzer = MedicalTestingAgreementAnalyzer()
        self.test_case_id = "case_2025_137857"
    
    def test_analyzer_initialization(self):
        """Test that analyzer initializes correctly"""
        assert self.analyzer is not None
        assert hasattr(self.analyzer, 'citizenship_analyzer')
        assert hasattr(self.analyzer, 'case_root_dir')
    
    def test_analyze_medical_testing_agreement(self):
        """Test comprehensive medical testing agreement analysis"""
        # Perform analysis
        analysis = self.analyzer.analyze_medical_testing_agreement(self.test_case_id)
        
        # Verify analysis object structure
        assert isinstance(analysis, MedicalTestingAnalysis)
        assert analysis.case_id == self.test_case_id
        assert isinstance(analysis.analysis_date, datetime)
        assert isinstance(analysis.citizenship_profile, CitizenshipProfile)
        assert isinstance(analysis.forensic_findings, list)
        assert isinstance(analysis.capacity_assessment, dict)
        assert isinstance(analysis.evidence_suppression_confirmed, bool)
        assert isinstance(analysis.legal_validity, str)
        assert isinstance(analysis.recommendations, list)
        assert isinstance(analysis.integration_status, dict)
    
    def test_british_citizen_capacity_assessment(self):
        """Test that British citizen capacity is properly assessed"""
        analysis = self.analyzer.analyze_medical_testing_agreement(self.test_case_id)
        
        # Verify citizenship profile
        profile = analysis.citizenship_profile
        assert profile.primary_citizenship == "British"
        assert profile.residency_status == CitizenshipStatus.PERMANENT_RESIDENT
        assert profile.tax_residence == "South Africa"
        
        # Verify capacity assessment identifies NO_CAPACITY for medical testing
        capacity = analysis.capacity_assessment
        medical_capacity = capacity['capacity_by_clause_type']['psychological_medical']
        assert medical_capacity['capacity_level'] == 'NO_CAPACITY'
        assert len(medical_capacity['unenforceable_elements']) > 0
        assert len(medical_capacity['restrictions']) > 0
    
    def test_forensic_findings_extraction(self):
        """Test that forensic findings are properly extracted"""
        analysis = self.analyzer.analyze_medical_testing_agreement(self.test_case_id)
        
        findings = analysis.forensic_findings
        assert len(findings) > 0
        
        # Check that all findings have required attributes
        for finding in findings:
            assert isinstance(finding, ForensicFinding)
            assert finding.clause is not None
            assert finding.surface_language is not None
            assert finding.actual_operation is not None
            assert finding.citizenship_impact is not None
            assert finding.evidence_suppression_mechanism is not None
            assert isinstance(finding.legal_capacity_violation, bool)
        
        # Verify that legal capacity violations are identified
        violations = [f for f in findings if f.legal_capacity_violation]
        assert len(violations) > 0, "Should identify legal capacity violations"
    
    def test_evidence_suppression_validation(self):
        """Test that evidence suppression mechanism is properly validated"""
        analysis = self.analyzer.analyze_medical_testing_agreement(self.test_case_id)
        
        # Should confirm evidence suppression for this case
        assert analysis.evidence_suppression_confirmed is True
    
    def test_legal_validity_determination(self):
        """Test that legal validity is properly determined"""
        analysis = self.analyzer.analyze_medical_testing_agreement(self.test_case_id)
        
        # For British citizens, medical testing agreement should be void
        assert "VOID" in analysis.legal_validity
        assert "Exceeds Legal Capacity" in analysis.legal_validity
    
    def test_recommendations_generation(self):
        """Test that appropriate recommendations are generated"""
        analysis = self.analyzer.analyze_medical_testing_agreement(self.test_case_id)
        
        recommendations = analysis.recommendations
        assert len(recommendations) > 0
        
        # Check for key recommendation categories
        recommendation_text = " ".join(recommendations).lower()
        assert "void" in recommendation_text or "legal capacity" in recommendation_text
        assert "evidence" in recommendation_text
        assert "uk" in recommendation_text or "british" in recommendation_text
    
    def test_integration_status_check(self):
        """Test that integration status is properly checked"""
        analysis = self.analyzer.analyze_medical_testing_agreement(self.test_case_id)
        
        integration_status = analysis.integration_status
        
        # Should check for key integration points
        expected_keys = [
            'forensic_linguistic_analysis_exists',
            'legal_capacity_analysis_exists', 
            'comprehensive_summary_exists',
            'citizenship_analyzer_integrated',
            'evidence_suppression_validated',
            'criminal_implications_documented'
        ]
        
        for key in expected_keys:
            assert key in integration_status
            assert isinstance(integration_status[key], bool)
    
    def test_validation_report_generation(self):
        """Test that validation report is properly generated"""
        analysis = self.analyzer.analyze_medical_testing_agreement(self.test_case_id)
        report = self.analyzer.generate_validation_report(analysis)
        
        assert isinstance(report, str)
        assert len(report) > 0
        
        # Check for key report sections
        assert "MEDICAL TESTING AGREEMENT VALIDATION REPORT" in report
        assert "EXECUTIVE SUMMARY" in report
        assert "CITIZENSHIP CAPACITY VALIDATION" in report
        assert "FORENSIC FINDINGS SUMMARY" in report
        assert "INTEGRATION STATUS" in report
        assert "RECOMMENDATIONS" in report
        assert "VALIDATION CONCLUSION" in report
    
    def test_forensic_finding_structure(self):
        """Test that ForensicFinding structure is valid"""
        finding = ForensicFinding(
            clause="Test Clause",
            surface_language="Test surface language",
            actual_operation="Test actual operation",
            citizenship_impact="Test citizenship impact", 
            evidence_suppression_mechanism="Test suppression mechanism",
            legal_capacity_violation=True
        )
        
        assert finding.clause == "Test Clause"
        assert finding.surface_language == "Test surface language"
        assert finding.actual_operation == "Test actual operation"
        assert finding.citizenship_impact == "Test citizenship impact"
        assert finding.evidence_suppression_mechanism == "Test suppression mechanism"
        assert finding.legal_capacity_violation is True
    
    def test_capacity_violation_identification(self):
        """Test that capacity violations are correctly identified for different citizenship scenarios"""
        # Test British citizen (should have no capacity)
        analysis = self.analyzer.analyze_medical_testing_agreement(self.test_case_id)
        medical_capacity = analysis.capacity_assessment['capacity_by_clause_type']['psychological_medical']
        assert medical_capacity['capacity_level'] == 'NO_CAPACITY'
    
    def test_evidence_suppression_indicators(self):
        """Test that evidence suppression indicators are properly evaluated"""
        # The analyzer should identify multiple suppression indicators
        suppression_confirmed = self.analyzer._validate_evidence_suppression()
        assert suppression_confirmed is True
    
    @pytest.mark.integration
    def test_full_analysis_integration(self):
        """Integration test that validates complete analysis workflow"""
        # Perform full analysis
        analysis = self.analyzer.analyze_medical_testing_agreement(self.test_case_id)
        
        # Verify all major components are present and valid
        assert analysis.case_id == self.test_case_id
        assert analysis.citizenship_profile.primary_citizenship == "British"
        assert analysis.evidence_suppression_confirmed is True
        assert "VOID" in analysis.legal_validity
        assert len(analysis.forensic_findings) >= 4  # Should have findings for major clauses
        assert len(analysis.recommendations) >= 5  # Should have comprehensive recommendations
        
        # Verify capacity assessment confirms no capacity for medical testing
        medical_capacity = analysis.capacity_assessment['capacity_by_clause_type']['psychological_medical']
        assert medical_capacity['capacity_level'] == 'NO_CAPACITY'
        
        # Verify that all forensic findings identify legal capacity violations
        violations = [f for f in analysis.forensic_findings if f.legal_capacity_violation]
        assert len(violations) == len(analysis.forensic_findings)
        
        # Generate and validate report
        report = self.analyzer.generate_validation_report(analysis)
        assert "VOID - Exceeds Legal Capacity of British Citizens" in report
        assert "Evidence Suppression Confirmed: ✅ YES" in report


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])