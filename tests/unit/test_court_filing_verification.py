#!/usr/bin/env python3
"""
Test suite for Court Filing Verification System

Tests the impersonation protection functionality to ensure Rynette Farrar
cannot impersonate Peter in court filings using the same email hijacking method.
"""

import unittest
from datetime import datetime
import sys
from pathlib import Path

# Add tools directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / "tools"))

from court_filing_verification import (
    CourtFilingVerificationSystem,
    CourtFiling,
    EmailControlEvidence,
    ImpersonationAlert,
    FilingAuthenticityLevel,
    FilingChannel
)


class TestCourtFilingVerificationSystem(unittest.TestCase):
    """Test cases for court filing verification system"""

    def setUp(self):
        """Set up test fixtures"""
        self.verifier = CourtFilingVerificationSystem("TEST-2025-001")
    
    def test_ocr_email_evidence_loaded(self):
        """Test that OCR email control evidence is properly loaded"""
        # Pete@regima.com should be loaded with Rynette as controller
        self.assertIn("pete@regima.com", self.verifier.email_control_evidence)
        
        pete_evidence = self.verifier.email_control_evidence["pete@regima.com"]
        self.assertEqual(pete_evidence.nominal_owner, "Peter Faucitt")
        self.assertEqual(pete_evidence.actual_controller, "Rynette Farrar")
        self.assertTrue(pete_evidence.ocr_verified)
        self.assertEqual(pete_evidence.reliability_score, 0.95)
    
    def test_authentic_filing_verification(self):
        """Test verification of authentic filing with legitimate email"""
        authentic_filing = CourtFiling(
            filing_id="test_authentic_001",
            case_number="TEST-2025-001",
            filing_date=datetime(2025, 10, 1),
            filing_channel=FilingChannel.PHYSICAL_FILING,
            submitter_name="John Smith",
            submitter_email="john.smith@lawfirm.com",
            document_type="Motion",
            document_hash="hash_authentic_001"
        )
        
        self.verifier.add_court_filing(authentic_filing)
        
        # Should be marked as authentic
        stored_filing = self.verifier.court_filings["test_authentic_001"]
        self.assertEqual(stored_filing.authenticity_level, FilingAuthenticityLevel.AUTHENTIC)
        self.assertEqual(len(stored_filing.impersonation_indicators), 0)
    
    def test_confirmed_impersonation_detection(self):
        """Test detection of confirmed impersonation using hijacked email"""
        impersonation_filing = CourtFiling(
            filing_id="test_impersonation_001",
            case_number="TEST-2025-001",
            filing_date=datetime(2025, 10, 1),
            filing_channel=FilingChannel.COURT_ONLINE,
            submitter_name="Peter Faucitt",  # Claims to be Peter
            submitter_email="pete@regima.com",  # But using Rynette's controlled email
            document_type="Interdict Application",
            document_hash="hash_impersonation_001"
        )
        
        self.verifier.add_court_filing(impersonation_filing)
        
        # Should be flagged as confirmed impersonation
        stored_filing = self.verifier.court_filings["test_impersonation_001"]
        self.assertEqual(stored_filing.authenticity_level, FilingAuthenticityLevel.CONFIRMED_IMPERSONATION)
        self.assertGreater(len(stored_filing.impersonation_indicators), 0)
        
        # Should contain specific indicators
        indicators_text = " ".join(stored_filing.impersonation_indicators)
        self.assertIn("Rynette Farrar", indicators_text)
        self.assertIn("OCR evidence", indicators_text)
        self.assertIn("controlled by different person", indicators_text)
    
    def test_za_court_services_impersonation(self):
        """Test specific detection for ZA court services (Court Online & Caselines)"""
        za_filing = CourtFiling(
            filing_id="test_za_services_001", 
            case_number="TEST-2025-001",
            filing_date=datetime(2025, 10, 1),
            filing_channel=FilingChannel.CASELINES,
            submitter_name="Peter Faucitt",
            submitter_email="pete@regima.com",
            document_type="Court Application",
            document_hash="hash_za_001"
        )
        
        self.verifier.add_court_filing(za_filing)
        
        stored_filing = self.verifier.court_filings["test_za_services_001"]
        indicators_text = " ".join(stored_filing.impersonation_indicators)
        
        # Should include ZA-specific warnings
        self.assertIn("ZA court service", indicators_text)
        self.assertIn("Same method used for account/bank impersonation", indicators_text)
        self.assertIn("Electronic signature authenticity cannot be verified", indicators_text)
    
    def test_impersonation_alert_creation(self):
        """Test that impersonation alerts are created for suspicious filings"""
        suspicious_filing = CourtFiling(
            filing_id="test_alert_001",
            case_number="TEST-2025-001", 
            filing_date=datetime(2025, 10, 1),
            filing_channel=FilingChannel.COURT_ONLINE,
            submitter_name="Peter Faucitt",
            submitter_email="pete@regima.com",
            document_type="Emergency Application",
            document_hash="hash_alert_001"
        )
        
        self.verifier.add_court_filing(suspicious_filing)
        
        # Alert should be created
        self.assertEqual(len(self.verifier.impersonation_alerts), 1)
        
        alert = list(self.verifier.impersonation_alerts.values())[0]
        self.assertEqual(alert.filing_id, "test_alert_001")
        self.assertEqual(alert.alert_level, "high")
        
        # Should have recommended actions
        actions_text = " ".join(alert.recommended_actions)
        self.assertIn("verify filer identity", actions_text)
        self.assertIn("OCR evidence", actions_text)
        self.assertIn("Challenge filing authenticity", actions_text)
        self.assertIn("ZA court services", actions_text)
    
    def test_electronic_signature_verification(self):
        """Test electronic signature authenticity verification"""
        # Add filing with compromised email
        compromised_filing = CourtFiling(
            filing_id="test_signature_001",
            case_number="TEST-2025-001",
            filing_date=datetime(2025, 10, 1),
            filing_channel=FilingChannel.EMAIL_SUBMISSION,
            submitter_name="Peter Faucitt",
            submitter_email="pete@regima.com",
            document_type="Affidavit",
            document_hash="hash_signature_001"
        )
        
        self.verifier.add_court_filing(compromised_filing)
        
        # Verify signature authenticity
        result = self.verifier.verify_electronic_signature_authenticity("test_signature_001")
        
        self.assertEqual(result["signature_authenticity"], "compromised")
        self.assertGreater(len(result["verification_issues"]), 0)
        self.assertGreater(len(result["legal_implications"]), 0)
        
        # Check specific issues
        issues_text = " ".join(result["verification_issues"])
        self.assertIn("controlled by Rynette Farrar", issues_text)
        self.assertIn("cannot be attributed to Peter Faucitt", issues_text)
        
        # Check legal implications
        implications_text = " ".join(result["legal_implications"])
        self.assertIn("Electronic signature invalid", implications_text)
        self.assertIn("identity theft and fraud", implications_text)
        self.assertIn("perjury", implications_text)
    
    def test_protection_report_generation(self):
        """Test generation of comprehensive protection report"""
        # Add some test filings
        authentic_filing = CourtFiling(
            filing_id="report_authentic",
            case_number="TEST-2025-001",
            filing_date=datetime(2025, 10, 1),
            filing_channel=FilingChannel.PHYSICAL_FILING,
            submitter_name="Legitimate User",
            submitter_email="real@example.com",
            document_type="Motion",
            document_hash="hash_real"
        )
        
        impersonation_filing = CourtFiling(
            filing_id="report_impersonation",
            case_number="TEST-2025-001", 
            filing_date=datetime(2025, 10, 2),
            filing_channel=FilingChannel.COURT_ONLINE,
            submitter_name="Peter Faucitt",
            submitter_email="pete@regima.com",
            document_type="Interdict",
            document_hash="hash_fake"
        )
        
        self.verifier.add_court_filing(authentic_filing)
        self.verifier.add_court_filing(impersonation_filing)
        
        # Generate report
        report = self.verifier.generate_impersonation_protection_report()
        
        # Check report content
        self.assertIn("Court Filing Impersonation Protection Report", report)
        self.assertIn("OCR-Verified Email Control Evidence", report)
        self.assertIn("CONFIRMED IMPERSONATION FILINGS", report)
        self.assertIn("pete@regima.com", report)
        self.assertIn("Rynette Farrar", report)
        self.assertIn("Legal Protection Recommendations", report)
        self.assertIn("Challenge All Electronic Filings", report)
    
    def test_data_export_functionality(self):
        """Test export of verification data for integration"""
        # Add test filing
        test_filing = CourtFiling(
            filing_id="export_test",
            case_number="TEST-2025-001",
            filing_date=datetime(2025, 10, 1),
            filing_channel=FilingChannel.EMAIL_SUBMISSION,
            submitter_name="Test User",
            submitter_email="test@example.com",
            document_type="Test Document",
            document_hash="hash_export_test"
        )
        
        self.verifier.add_court_filing(test_filing)
        
        # Export data
        exported_data = self.verifier.export_verification_data()
        
        # Check export structure
        self.assertIn("case_number", exported_data)
        self.assertIn("email_control_evidence", exported_data)
        self.assertIn("court_filings", exported_data)
        self.assertIn("impersonation_alerts", exported_data)
        self.assertIn("export_date", exported_data)
        
        # Check specific data
        self.assertEqual(exported_data["case_number"], "TEST-2025-001")
        self.assertIn("pete@regima.com", exported_data["email_control_evidence"])
        self.assertIn("export_test", exported_data["court_filings"])


class TestEmailControlEvidence(unittest.TestCase):
    """Test cases for email control evidence functionality"""
    
    def test_email_control_evidence_creation(self):
        """Test creation of email control evidence"""
        evidence = EmailControlEvidence(
            email_address="test@example.com",
            nominal_owner="Test Owner",
            actual_controller="Test Controller",
            evidence_source="Test Source",
            evidence_date=datetime(2025, 1, 1),
            ocr_verified=True,
            reliability_score=0.9
        )
        
        self.assertEqual(evidence.email_address, "test@example.com")
        self.assertEqual(evidence.nominal_owner, "Test Owner") 
        self.assertEqual(evidence.actual_controller, "Test Controller")
        self.assertTrue(evidence.ocr_verified)
        self.assertEqual(evidence.reliability_score, 0.9)


if __name__ == "__main__":
    unittest.main()