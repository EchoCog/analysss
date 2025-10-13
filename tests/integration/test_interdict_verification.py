#!/usr/bin/env python3
"""
Test suite for Interdict Verification System

Validates the verification system functionality without requiring
external dependencies like numpy.
"""

import unittest
from datetime import datetime
import sys
from pathlib import Path

# Add tools directory to path
sys.path.append(str(Path(__file__).parent / "tools"))

from interdict_verification_system import (
    InterdictVerificationSystem,
    InterdictClaim,
    EvidenceItem,
    CourtOrderMetadata,
    VerificationLevel,
    ClaimType,
)


class TestInterdictVerificationSystem(unittest.TestCase):
    """Test cases for the interdict verification system"""

    def setUp(self):
        """Set up test fixtures"""
        self.verifier = InterdictVerificationSystem("TEST-2025-001")

        # Create test metadata
        self.test_metadata = CourtOrderMetadata(
            case_number="TEST-2025-001",
            court_name="Test High Court",
            judge_name="Test Judge J",
            order_date=datetime(2025, 1, 1),
            document_hash="test_hash_123",
            filing_verified=True,
            service_verified=False,
        )

        # Create test claim
        self.test_claim = InterdicClaim(
            claim_id="test_claim_1",
            claim_type=ClaimType.FINANCIAL,
            section_reference="2.1",
            claim_text="Test financial misconduct claim",
            alleged_amount=100000.0,
            alleged_date=datetime(2024, 12, 1),
        )

        # Create test evidence
        self.test_evidence = EvidenceItem(
            evidence_id="test_evidence_1",
            source_document="test_document.md",
            page_reference="Page 1",
            content_summary="Test evidence supporting the claim",
            reliability_score=0.8,
            verification_date=datetime.now(),
            verifier="Test System",
        )

    def test_system_initialization(self):
        """Test system initializes correctly"""
        self.assertEqual(self.verifier.case_number, "TEST-2025-001")
        self.assertEqual(len(self.verifier.claims), 0)
        self.assertEqual(len(self.verifier.evidence_repository), 0)
        self.assertIsNone(self.verifier.court_metadata)

    def test_court_metadata_setting(self):
        """Test setting court metadata"""
        self.verifier.set_court_metadata(self.test_metadata)
        self.assertEqual(self.verifier.court_metadata.case_number, "TEST-2025-001")
        self.assertEqual(self.verifier.court_metadata.judge_name, "Test Judge J")
        self.assertTrue(self.verifier.court_metadata.filing_verified)
        self.assertFalse(self.verifier.court_metadata.service_verified)

    def test_add_claim(self):
        """Test adding claims to the system"""
        self.verifier.add_claim(self.test_claim)
        self.assertEqual(len(self.verifier.claims), 1)
        self.assertIn("test_claim_1", self.verifier.claims)

        claim = self.verifier.claims["test_claim_1"]
        self.assertEqual(claim.claim_type, ClaimType.FINANCIAL)
        self.assertEqual(claim.section_reference, "2.1")
        self.assertEqual(claim.alleged_amount, 100000.0)
        self.assertEqual(claim.verification_level, VerificationLevel.UNVERIFIED)

    def test_add_evidence(self):
        """Test adding evidence to the system"""
        self.verifier.add_evidence(self.test_evidence)
        self.assertEqual(len(self.verifier.evidence_repository), 1)
        self.assertIn("test_evidence_1", self.verifier.evidence_repository)

        evidence = self.verifier.evidence_repository["test_evidence_1"]
        self.assertEqual(evidence.source_document, "test_document.md")
        self.assertEqual(evidence.reliability_score, 0.8)

    def test_link_evidence_to_claim(self):
        """Test linking evidence to claims"""
        # Add claim and evidence first
        self.verifier.add_claim(self.test_claim)
        self.verifier.add_evidence(self.test_evidence)

        # Link them
        self.verifier.link_evidence_to_claim(
            "test_claim_1", "test_evidence_1", supports=True
        )

        claim = self.verifier.claims["test_claim_1"]
        self.assertEqual(len(claim.supporting_evidence), 1)
        self.assertEqual(len(claim.contradicting_evidence), 0)
        self.assertEqual(claim.supporting_evidence[0].evidence_id, "test_evidence_1")

        # Verification level should be updated
        self.assertNotEqual(claim.verification_level, VerificationLevel.UNVERIFIED)

    def test_verification_level_updates(self):
        """Test that verification levels update correctly based on evidence"""
        self.verifier.add_claim(self.test_claim)
        self.verifier.add_evidence(self.test_evidence)

        # Initially unverified
        claim = self.verifier.claims["test_claim_1"]
        self.assertEqual(claim.verification_level, VerificationLevel.UNVERIFIED)

        # Add supporting evidence - should become partial or verified
        self.verifier.link_evidence_to_claim(
            "test_claim_1", "test_evidence_1", supports=True
        )
        self.assertIn(
            claim.verification_level,
            [VerificationLevel.PARTIAL, VerificationLevel.VERIFIED],
        )

        # Create contradicting evidence
        contradicting_evidence = EvidenceItem(
            evidence_id="test_evidence_2",
            source_document="contradicting_doc.md",
            page_reference="Page 2",
            content_summary="Evidence contradicting the claim",
            reliability_score=0.9,
            verification_date=datetime.now(),
            verifier="Test System",
        )

        self.verifier.add_evidence(contradicting_evidence)
        self.verifier.link_evidence_to_claim(
            "test_claim_1", "test_evidence_2", supports=False
        )

        # Should be partial or contradicted now
        self.assertIn(
            claim.verification_level,
            [VerificationLevel.PARTIAL, VerificationLevel.CONTRADICTED],
        )

    def test_flag_impossible_claim(self):
        """Test flagging impossible claims"""
        self.verifier.add_claim(self.test_claim)

        reason = "Test reason for impossibility"
        self.verifier.flag_impossible_claim("test_claim_1", reason)

        claim = self.verifier.claims["test_claim_1"]
        self.assertEqual(claim.verification_level, VerificationLevel.IMPOSSIBLE)
        self.assertTrue(any("IMPOSSIBLE" in note for note in claim.verification_notes))

        # Should add verification requirement
        impossible_reqs = [
            req
            for req in self.verifier.verification_requirements
            if req["type"] == "impossible_claim"
        ]
        self.assertEqual(len(impossible_reqs), 1)
        self.assertEqual(impossible_reqs[0]["claim_id"], "test_claim_1")

    def test_procedural_and_legal_verification(self):
        """Test procedural and legal basis verification"""
        self.verifier.add_claim(self.test_claim)

        # Test procedural compliance
        self.verifier.verify_procedural_compliance(
            "test_claim_1", True, "Met all procedural requirements"
        )
        claim = self.verifier.claims["test_claim_1"]
        self.assertTrue(claim.procedural_compliance)
        self.assertTrue(any("PROCEDURAL" in note for note in claim.verification_notes))

        # Test legal basis verification
        self.verifier.verify_legal_basis(
            "test_claim_1", True, "Section 123 of Test Act"
        )
        self.assertTrue(claim.legal_basis_verified)
        self.assertTrue(any("LEGAL BASIS" in note for note in claim.verification_notes))

    def test_verification_report_generation(self):
        """Test verification report generation"""
        # Set up test data
        self.verifier.set_court_metadata(self.test_metadata)
        self.verifier.add_claim(self.test_claim)
        self.verifier.add_evidence(self.test_evidence)
        self.verifier.link_evidence_to_claim(
            "test_claim_1", "test_evidence_1", supports=True
        )

        # Generate report
        report = self.verifier.generate_verification_report()

        # Check report content
        self.assertIn("Interdict Verification Report", report)
        self.assertIn("TEST-2025-001", report)
        self.assertIn("Test High Court", report)
        self.assertIn("Test Judge J", report)
        self.assertIn("**Total Claims**: 1", report)
        self.assertIn("Section 2.1", report)

    def test_verification_checklist_generation(self):
        """Test verification checklist generation"""
        # Add test claim
        self.verifier.add_claim(self.test_claim)

        # Generate checklist
        checklist = self.verifier.generate_verification_checklist()

        # Check checklist content
        self.assertIn("Interdict Verification Checklist", checklist)
        self.assertIn("COURT ORDER AUTHENTICITY", checklist)
        self.assertIn("FINANCIAL CLAIMS VERIFICATION", checklist)
        self.assertIn("Section 2.1", checklist)
        self.assertIn("Test financial misconduct claim", checklist)
        self.assertIn("R100,000.00", checklist)

    def test_document_hash_calculation(self):
        """Test document hash calculation"""
        # Test with non-existent file
        hash_result = self.verifier.calculate_document_hash("nonexistent_file.txt")
        self.assertEqual(hash_result, "FILE_NOT_FOUND")

        # Test with this test file itself
        test_file_path = __file__
        hash_result = self.verifier.calculate_document_hash(test_file_path)
        self.assertNotEqual(hash_result, "FILE_NOT_FOUND")
        self.assertEqual(len(hash_result), 64)  # SHA256 hash length


class TestCase2025137857Integration(unittest.TestCase):
    """Integration tests with actual case data"""

    def setUp(self):
        """Set up integration test fixtures"""
        self.verifier = InterdictVerificationSystem("2025-137857")

        # Real court metadata
        self.court_metadata = CourtOrderMetadata(
            case_number="2025-137857",
            court_name="High Court of South Africa, Gauteng Division, Pretoria",
            judge_name="Justice Kumalo J",
            order_date=datetime(2025, 8, 19),
            document_hash="placeholder_hash",
            filing_verified=False,
            service_verified=False,
            legal_representation_verified=True,
            jurisdiction_verified=True,
        )

    def test_case_metadata_setup(self):
        """Test setting up real case metadata"""
        self.verifier.set_court_metadata(self.court_metadata)

        metadata = self.verifier.court_metadata
        self.assertEqual(metadata.case_number, "2025-137857")
        self.assertEqual(metadata.judge_name, "Justice Kumalo J")
        self.assertTrue(metadata.legal_representation_verified)
        self.assertFalse(metadata.filing_verified)  # Still needs verification

    def test_financial_claims_setup(self):
        """Test setting up key financial claims from the case"""
        # Banking restrictions claim
        banking_claim = InterdicClaim(
            claim_id="banking_restrictions_21",
            claim_type=ClaimType.FINANCIAL,
            section_reference="2.1",
            claim_text="First and Second Respondents are interdicted and directed to surrender forthwith to the Applicant their banking credit, and/or cheque, and/or debit cards",
            legal_basis_verified=False,
            procedural_compliance=False,
        )

        self.verifier.add_claim(banking_claim)

        # R500K transfer claim
        transfer_claim = InterdicClaim(
            claim_id="unauthorized_transfer",
            claim_type=ClaimType.FINANCIAL,
            section_reference="allegations",
            claim_text="Unauthorized R500,000 birthday gift transfer",
            alleged_amount=500000.0,
            alleged_date=datetime(2025, 7, 16),
        )

        self.verifier.add_claim(transfer_claim)

        # Verify claims were added
        self.assertEqual(len(self.verifier.claims), 2)
        self.assertIn("banking_restrictions_21", self.verifier.claims)
        self.assertIn("unauthorized_transfer", self.verifier.claims)

        transfer = self.verifier.claims["unauthorized_transfer"]
        self.assertEqual(transfer.alleged_amount, 500000.0)

    def test_evidence_integration(self):
        """Test integrating forensic analysis evidence"""
        # Add the R8.8M evidence from forensic analysis
        forensic_evidence = EvidenceItem(
            evidence_id="forensic_r8_8m",
            source_document="interdict_forensic_analysis.md",
            page_reference="Executive Summary",
            content_summary="R6,738,007.47 (2024) + R2,116,159.47 (2025) in unexplained IT expenses",
            reliability_score=0.9,
            verification_date=datetime.now(),
            verifier="Forensic Analysis System",
        )

        self.verifier.add_evidence(forensic_evidence)

        # Add a banking claim to link it to
        banking_claim = InterdicClaim(
            claim_id="it_expenses",
            claim_type=ClaimType.FINANCIAL,
            section_reference="allegations",
            claim_text="Unauthorized IT expenses totaling R8.8 million",
            alleged_amount=8854166.94,
        )

        self.verifier.add_claim(banking_claim)
        self.verifier.link_evidence_to_claim(
            "it_expenses", "forensic_r8_8m", supports=True
        )

        # Verify the linking worked
        claim = self.verifier.claims["it_expenses"]
        self.assertEqual(len(claim.supporting_evidence), 1)
        self.assertEqual(claim.supporting_evidence[0].evidence_id, "forensic_r8_8m")

        # Should improve verification level
        self.assertNotEqual(claim.verification_level, VerificationLevel.UNVERIFIED)


def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTest(unittest.makeSuite(TestInterdictVerificationSystem))
    suite.addTest(unittest.makeSuite(TestCase2025137857Integration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
