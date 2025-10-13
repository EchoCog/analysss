#!/usr/bin/env python3
"""
Tests for CitizenshipSettlementAnalyzer

Tests the functionality of analyzing citizenship status impacts on settlement agreements.
"""

import pytest
import json
from pathlib import Path
import tempfile
import os
import sys

# Add the tools directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../tools'))

from citizenship_settlement_analyzer import (
    CitizenshipSettlementAnalyzer,
    CitizenshipProfile,
    CitizenshipStatus,
    SettlementType,
    EnforcementComplexity,
    SettlementImpactAssessment,
    create_sample_profiles
)


class TestCitizenshipProfile:
    """Test the CitizenshipProfile dataclass"""
    
    def test_citizenship_profile_creation(self):
        """Test basic citizenship profile creation"""
        profile = CitizenshipProfile(
            primary_citizenship="US",
            residency_status=CitizenshipStatus.FULL_CITIZEN,
            tax_residence="US",
            language_preferences=["English"]
        )
        
        assert profile.primary_citizenship == "US"
        assert profile.residency_status == CitizenshipStatus.FULL_CITIZEN
        assert profile.tax_residence == "US"
        assert profile.language_preferences == ["English"]
    
    def test_citizenship_profile_defaults(self):
        """Test default values in citizenship profile"""
        profile = CitizenshipProfile(primary_citizenship="UK")
        
        assert profile.secondary_citizenship is None
        assert profile.residency_status == CitizenshipStatus.FULL_CITIZEN
        assert profile.tax_residence == ""
        assert profile.language_preferences == []
        assert profile.years_of_residence == 0
    
    def test_dual_citizenship_profile(self):
        """Test dual citizenship profile creation"""
        profile = CitizenshipProfile(
            primary_citizenship="US",
            secondary_citizenship="Canada",
            residency_status=CitizenshipStatus.DUAL_CITIZEN
        )
        
        assert profile.primary_citizenship == "US"
        assert profile.secondary_citizenship == "Canada"
        assert profile.residency_status == CitizenshipStatus.DUAL_CITIZEN


class TestCitizenshipSettlementAnalyzer:
    """Test the main CitizenshipSettlementAnalyzer class"""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance for testing"""
        return CitizenshipSettlementAnalyzer()
    
    @pytest.fixture
    def sample_profiles(self):
        """Create sample profiles for testing"""
        return create_sample_profiles()
    
    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization"""
        assert analyzer.impact_matrix is not None
        assert analyzer.enforcement_rules is not None
        assert len(analyzer.impact_matrix) > 0
        assert len(analyzer.enforcement_rules) > 0
    
    def test_impact_matrix_structure(self, analyzer):
        """Test impact matrix has required structure"""
        # Check all settlement types are covered
        expected_settlement_types = [
            SettlementType.PSYCHOLOGICAL,
            SettlementType.CIVIL_PERSONAL,
            SettlementType.COMMERCIAL,
            SettlementType.PROPERTY
        ]
        
        for settlement_type in expected_settlement_types:
            assert settlement_type in analyzer.impact_matrix
        
        # Check all citizenship statuses are covered for psychological settlements
        psychological_impacts = analyzer.impact_matrix[SettlementType.PSYCHOLOGICAL]
        expected_citizenship_statuses = [
            CitizenshipStatus.FULL_CITIZEN,
            CitizenshipStatus.PERMANENT_RESIDENT,
            CitizenshipStatus.TEMPORARY_RESIDENT,
            CitizenshipStatus.VISA_HOLDER,
            CitizenshipStatus.DUAL_CITIZEN,
            CitizenshipStatus.STATELESS
        ]
        
        for status in expected_citizenship_statuses:
            assert status in psychological_impacts
    
    def test_british_permanent_resident_psychological_analysis(self, analyzer, sample_profiles):
        """Test analysis of British permanent resident in psychological settlement"""
        profile = sample_profiles["british_permanent_resident"]
        assessment = analyzer.analyze_citizenship_impact(profile, SettlementType.PSYCHOLOGICAL)
        
        assert isinstance(assessment, SettlementImpactAssessment)
        assert assessment.settlement_type == SettlementType.PSYCHOLOGICAL
        assert assessment.citizenship_impact_level == "CRITICAL"
        assert assessment.enforcement_complexity in [
            EnforcementComplexity.VERY_HIGH, 
            EnforcementComplexity.CRITICAL
        ]
        
        # Check that enforceable elements include medical compliance
        assert any("medical" in element.lower() or "treatment" in element.lower() 
                  for element in assessment.enforceable_elements)
        
        # Check that unenforceable elements exist
        assert len(assessment.unenforceable_elements) > 0
    
    def test_dual_citizen_commercial_analysis(self, analyzer, sample_profiles):
        """Test analysis of dual citizen in commercial settlement"""
        profile = sample_profiles["dual_citizen_us_canada"]
        assessment = analyzer.analyze_citizenship_impact(profile, SettlementType.COMMERCIAL)
        
        assert assessment.settlement_type == SettlementType.COMMERCIAL
        assert assessment.citizenship_impact_level == "MODERATE"
        
        # Dual citizenship should increase enforcement complexity
        assert assessment.enforcement_complexity in [
            EnforcementComplexity.MODERATE,
            EnforcementComplexity.HIGH,
            EnforcementComplexity.VERY_HIGH
        ]
        
        # Should have multiple jurisdictions due to dual citizenship
        assert len(assessment.required_jurisdictions) >= 2
    
    def test_temporary_resident_civil_analysis(self, analyzer, sample_profiles):
        """Test analysis of temporary resident in civil settlement"""
        profile = sample_profiles["temporary_resident"]
        assessment = analyzer.analyze_citizenship_impact(profile, SettlementType.CIVIL_PERSONAL)
        
        assert assessment.settlement_type == SettlementType.CIVIL_PERSONAL
        
        # Temporary status should create risk factors
        assert len(assessment.risk_factors) > 0
        assert any("status" in risk.lower() or "residency" in risk.lower() 
                  for risk in assessment.risk_factors)
    
    def test_enforcement_complexity_calculation(self, analyzer):
        """Test enforcement complexity calculation logic"""
        # Full citizen should have lower complexity than dual citizen
        full_citizen = CitizenshipProfile(
            primary_citizenship="US",
            residency_status=CitizenshipStatus.FULL_CITIZEN
        )
        
        dual_citizen = CitizenshipProfile(
            primary_citizenship="US",
            secondary_citizenship="Canada",
            residency_status=CitizenshipStatus.DUAL_CITIZEN
        )
        
        full_assessment = analyzer.analyze_citizenship_impact(full_citizen, SettlementType.COMMERCIAL)
        dual_assessment = analyzer.analyze_citizenship_impact(dual_citizen, SettlementType.COMMERCIAL)
        
        complexity_order = [
            EnforcementComplexity.LOW,
            EnforcementComplexity.MODERATE, 
            EnforcementComplexity.HIGH,
            EnforcementComplexity.VERY_HIGH,
            EnforcementComplexity.CRITICAL
        ]
        
        full_index = complexity_order.index(full_assessment.enforcement_complexity)
        dual_index = complexity_order.index(dual_assessment.enforcement_complexity)
        
        # Dual citizenship should not decrease complexity
        assert dual_index >= full_index
    
    def test_jurisdictional_identification(self, analyzer):
        """Test jurisdiction identification logic"""
        profile = CitizenshipProfile(
            primary_citizenship="US",
            secondary_citizenship="UK",
            tax_residence="Canada",
            legal_domicile="Australia",
            residency_status=CitizenshipStatus.DUAL_CITIZEN
        )
        
        jurisdictions = analyzer._identify_jurisdictions(profile)
        
        # Should include all relevant jurisdictions
        expected_jurisdictions = ["US", "UK", "Canada", "Australia"]
        for jurisdiction in expected_jurisdictions:
            assert jurisdiction in jurisdictions
        
        # Should not have duplicates
        assert len(jurisdictions) == len(set(jurisdictions))
    
    def test_british_tax_vote_disconnect_rule(self, analyzer):
        """Test the specific British tax-vote disconnect rule"""
        british_permanent_resident = CitizenshipProfile(
            primary_citizenship="British",
            residency_status=CitizenshipStatus.PERMANENT_RESIDENT,
            tax_residence="UK"
        )
        
        assessment = analyzer.analyze_citizenship_impact(
            british_permanent_resident, SettlementType.CIVIL_PERSONAL
        )
        
        # Should have tax obligations as enforceable
        enforceable_str = " ".join(assessment.enforceable_elements).lower()
        assert "tax" in enforceable_str
        
        # Should have voting restrictions as unenforceable
        unenforceable_str = " ".join(assessment.unenforceable_elements).lower()
        assert "voting" in unenforceable_str or "political" in unenforceable_str
    
    def test_cultural_considerations_psychological(self, analyzer):
        """Test cultural considerations for psychological settlements"""
        multicultural_profile = CitizenshipProfile(
            primary_citizenship="India",
            residency_status=CitizenshipStatus.TEMPORARY_RESIDENT,
            language_preferences=["Hindi", "English", "Tamil"],
            cultural_background="South Asian"
        )
        
        assessment = analyzer.analyze_citizenship_impact(
            multicultural_profile, SettlementType.PSYCHOLOGICAL
        )
        
        # Should have cultural considerations
        assert len(assessment.cultural_considerations) > 0
        
        # Should mention language services
        cultural_str = " ".join(assessment.cultural_considerations).lower()
        assert "language" in cultural_str or "cultural" in cultural_str
    
    def test_appeal_mechanisms_by_status(self, analyzer):
        """Test appeal mechanisms vary by citizenship status"""
        full_citizen = CitizenshipProfile(
            primary_citizenship="US",
            residency_status=CitizenshipStatus.FULL_CITIZEN
        )
        
        temporary_resident = CitizenshipProfile(
            primary_citizenship="India",
            residency_status=CitizenshipStatus.TEMPORARY_RESIDENT
        )
        
        full_assessment = analyzer.analyze_citizenship_impact(full_citizen, SettlementType.CIVIL_PERSONAL)
        temp_assessment = analyzer.analyze_citizenship_impact(temporary_resident, SettlementType.CIVIL_PERSONAL)
        
        # Full citizen should have more appeal mechanisms
        assert len(full_assessment.appeal_mechanisms) >= len(temp_assessment.appeal_mechanisms)
        
        # Full citizen should have domestic court access
        full_appeals_str = " ".join(full_assessment.appeal_mechanisms).lower()
        assert "domestic court" in full_appeals_str or "full" in full_appeals_str
    
    def test_generate_citizenship_settlement_report(self, analyzer, sample_profiles):
        """Test comprehensive report generation"""
        profile = sample_profiles["british_permanent_resident"]
        
        report = analyzer.generate_citizenship_settlement_report(
            profile, SettlementType.PSYCHOLOGICAL, "test_case_123"
        )
        
        # Check report structure
        required_keys = [
            "analysis_metadata",
            "citizenship_profile", 
            "settlement_assessment",
            "recommendations",
            "applicable_enforcement_rules",
            "compliance_checklist"
        ]
        
        for key in required_keys:
            assert key in report
        
        # Check metadata
        assert report["analysis_metadata"]["case_id"] == "test_case_123"
        assert "analysis_date" in report["analysis_metadata"]
        
        # Check recommendations exist
        assert len(report["recommendations"]) > 0
        
        # Check compliance checklist exists
        assert len(report["compliance_checklist"]) > 0
    
    def test_report_json_serializable(self, analyzer, sample_profiles):
        """Test that generated reports are JSON serializable"""
        profile = sample_profiles["dual_citizen_us_canada"]
        
        report = analyzer.generate_citizenship_settlement_report(
            profile, SettlementType.COMMERCIAL
        )
        
        # Should be able to serialize to JSON without errors
        json_str = json.dumps(report, indent=2)
        assert len(json_str) > 0
        
        # Should be able to deserialize back
        deserialized = json.loads(json_str)
        assert deserialized == report
    
    def test_settlement_element_categorization(self, analyzer):
        """Test settlement element categorization logic"""
        profile = CitizenshipProfile(
            primary_citizenship="British",
            residency_status=CitizenshipStatus.PERMANENT_RESIDENT
        )
        
        # Test psychological settlement categorization
        enforceable, unenforceable = analyzer._categorize_settlement_elements(
            profile, SettlementType.PSYCHOLOGICAL
        )
        
        # Should have both categories
        assert len(enforceable) > 0
        assert len(unenforceable) > 0
        
        # Medical compliance should be enforceable
        enforceable_str = " ".join(enforceable).lower()
        assert "medical" in enforceable_str or "treatment" in enforceable_str
        
        # Cross-border enforcement should be challenging
        unenforceable_str = " ".join(unenforceable).lower()
        assert "cross" in unenforceable_str or "border" in unenforceable_str or "treaty" in unenforceable_str


class TestSampleProfiles:
    """Test the sample profile creation function"""
    
    def test_sample_profiles_creation(self):
        """Test that sample profiles are created correctly"""
        profiles = create_sample_profiles()
        
        expected_profiles = [
            "british_permanent_resident",
            "dual_citizen_us_canada", 
            "temporary_resident"
        ]
        
        for profile_name in expected_profiles:
            assert profile_name in profiles
            assert isinstance(profiles[profile_name], CitizenshipProfile)
    
    def test_british_permanent_resident_profile(self):
        """Test specific British permanent resident profile"""
        profiles = create_sample_profiles()
        british_profile = profiles["british_permanent_resident"]
        
        assert british_profile.primary_citizenship == "British"
        assert british_profile.residency_status == CitizenshipStatus.PERMANENT_RESIDENT
        assert british_profile.tax_residence == "UK"
        assert "English" in british_profile.language_preferences
    
    def test_dual_citizen_profile(self):
        """Test dual citizen profile"""
        profiles = create_sample_profiles()
        dual_profile = profiles["dual_citizen_us_canada"]
        
        assert dual_profile.primary_citizenship == "US"
        assert dual_profile.secondary_citizenship == "Canada"
        assert dual_profile.residency_status == CitizenshipStatus.DUAL_CITIZEN
        assert len(dual_profile.language_preferences) >= 2


class TestIntegrationScenarios:
    """Test integration scenarios combining multiple features"""
    
    @pytest.fixture
    def analyzer(self):
        return CitizenshipSettlementAnalyzer()
    
    def test_case_2025_137857_scenario(self, analyzer):
        """Test scenario specific to case 2025_137857"""
        # Create a profile that might be relevant to the case
        case_profile = CitizenshipProfile(
            primary_citizenship="South African",
            residency_status=CitizenshipStatus.FULL_CITIZEN,
            tax_residence="South Africa",
            legal_domicile="South Africa",
            language_preferences=["English", "Afrikaans"],
            cultural_background="South African"
        )
        
        # Test psychological settlement (relevant to medical testing in case)
        assessment = analyzer.analyze_citizenship_impact(
            case_profile, SettlementType.PSYCHOLOGICAL
        )
        
        assert assessment.settlement_type == SettlementType.PSYCHOLOGICAL
        assert len(assessment.cultural_considerations) > 0
        assert len(assessment.enforceable_elements) > 0
        
        # Generate report for the case
        report = analyzer.generate_citizenship_settlement_report(
            case_profile, SettlementType.PSYCHOLOGICAL, "case_2025_137857"
        )
        
        assert report["analysis_metadata"]["case_id"] == "case_2025_137857"
        assert len(report["compliance_checklist"]) > 0
    
    def test_complex_multi_jurisdiction_scenario(self, analyzer):
        """Test complex scenario with multiple jurisdictions"""
        complex_profile = CitizenshipProfile(
            primary_citizenship="US",
            secondary_citizenship="UK", 
            residency_status=CitizenshipStatus.DUAL_CITIZEN,
            tax_residence="Singapore",
            legal_domicile="Hong Kong",
            language_preferences=["English", "Mandarin"],
            cultural_background="Multicultural"
        )
        
        assessment = analyzer.analyze_citizenship_impact(
            complex_profile, SettlementType.COMMERCIAL
        )
        
        # Should have high enforcement complexity due to multiple jurisdictions
        assert assessment.enforcement_complexity in [
            EnforcementComplexity.HIGH,
            EnforcementComplexity.VERY_HIGH,
            EnforcementComplexity.CRITICAL
        ]
        
        # Should have multiple jurisdictions
        assert len(assessment.required_jurisdictions) >= 3
        
        # Should have jurisdictional conflict risks
        risk_str = " ".join(assessment.risk_factors).lower()
        assert "jurisdiction" in risk_str or "conflict" in risk_str


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])