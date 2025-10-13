#!/usr/bin/env python3
"""
Integration tests for Court Filing Impersonation Protection

Tests the integration between the interdict verification system and 
court filing verification to protect against impersonation attacks.
"""

import unittest
from datetime import datetime
import sys
from pathlib import Path

# Add tools directory to path  
sys.path.append(str(Path(__file__).parent.parent.parent / "tools"))

from interdict_verification_system import (
    InterdictVerificationSystem,
    InterdictClaim,
    EvidenceItem,
    CourtOrderMetadata,
    VerificationLevel,
    ClaimType
)


class TestCourtImpersonationProtectionIntegration(unittest.TestCase):
    """Integration tests for court impersonation protection"""

    def setUp(self):
        """Set up integration test fixtures"""
        self.verifier = InterdictVerificationSystem("2025-137857")
        
        # Set up court metadata
        self.court_metadata = CourtOrderMetadata(
            case_number="2025-137857",
            order_date=datetime(2025, 8, 19),
            document_hash="test_hash_137857",
            is_second_interdict=False
        )
        
        self.verifier.add_court_order(self.court_metadata)

    def test_legitimate_filing_verification(self):
        """Test verification of legitimate court filing"""
        legitimate_filing = {
            "filing_id": "legitimate_001",
            "filing_date": datetime(2025, 10, 1),
            "filing_channel": "physical_filing",
            "submitter_name": "Attorney Smith",
            "submitter_email": "attorney.smith@lawfirm.co.za",
            "document_type": "Motion to Dismiss",
            "document_hash": "hash_legitimate_001"
        }
        
        result = self.verifier.verify_court_filing_authenticity(legitimate_filing)
        
        # Should pass verification
        self.assertEqual(result["authenticity_level"], "authentic")
        self.assertEqual(len(result["impersonation_indicators"]), 0)
        
    def test_pete_email_impersonation_detection(self):
        """Test detection of impersonation using Pete@regima.com (OCR verified hijacked email)"""
        impersonation_filing = {
            "filing_id": "impersonation_pete_001",
            "filing_date": datetime(2025, 10, 1), 
            "filing_channel": "court_online",
            "submitter_name": "Peter Faucitt",  # Claims to be Peter
            "submitter_email": "pete@regima.com",  # But using hijacked email
            "document_type": "Interdict Application", 
            "document_hash": "hash_impersonation_001"
        }
        
        result = self.verifier.verify_court_filing_authenticity(impersonation_filing)
        
        # Should detect confirmed impersonation
        self.assertEqual(result["authenticity_level"], "confirmed_impersonation")
        self.assertGreater(len(result["impersonation_indicators"]), 0)
        
        # Should reference OCR evidence and Rynette's control
        indicators_text = " ".join(result["impersonation_indicators"])
        self.assertIn("Rynette Farrar", indicators_text)
        self.assertIn("OCR evidence", indicators_text)
        
    def test_caselines_impersonation_detection(self):
        """Test detection of impersonation through Caselines system"""
        caselines_filing = {
            "filing_id": "caselines_impersonation_001",
            "filing_date": datetime(2025, 10, 2),
            "filing_channel": "caselines", 
            "submitter_name": "Peter Faucitt",
            "submitter_email": "pete@regima.com",
            "document_type": "Emergency Application",
            "document_hash": "hash_caselines_001"
        }
        
        result = self.verifier.verify_court_filing_authenticity(caselines_filing)
        
        # Should detect impersonation with ZA-specific warnings
        self.assertEqual(result["authenticity_level"], "confirmed_impersonation")
        
        indicators_text = " ".join(result["impersonation_indicators"])
        self.assertIn("ZA court service", indicators_text)
        self.assertIn("Same method used for account/bank impersonation", indicators_text)
        
    def test_prosecution_memo_with_impersonation_evidence(self):
        """Test that prosecution memo includes impersonation evidence"""
        # Add malicious claim to trigger memo generation
        malicious_claim = InterdictClaim(
            claim_id="malicious_test_001", 
            claim_type=ClaimType.WITNESS_INTIMIDATION,
            claim_text="Compel Daniel to undergo medical testing based on fabricated gambling claims"
        )
        malicious_claim.verification_level = VerificationLevel.MALICIOUS
        malicious_claim.verification_notes = ["No evidence of gambling addiction", "Medical records contradict claim"]
        
        self.verifier.add_claim(malicious_claim)
        
        # Add impersonation filing
        impersonation_filing = {
            "filing_id": "memo_impersonation_001",
            "filing_date": datetime(2025, 10, 1),
            "filing_channel": "court_online",
            "submitter_name": "Peter Faucitt", 
            "submitter_email": "pete@regima.com",
            "document_type": "Supporting Affidavit",
            "document_hash": "hash_memo_001"
        }
        
        self.verifier.verify_court_filing_authenticity(impersonation_filing)
        
        # Generate prosecution memo
        memo = self.verifier.generate_prosecution_memo()
        
        # Should include impersonation evidence
        self.assertIn("Court Filing Impersonation Evidence", memo)
        self.assertIn("pete@regima.com", memo)
        self.assertIn("Rynette Farrar", memo)
        # Should show the alert
        self.assertIn("HIGH", memo)
        self.assertIn("controlled by Rynette Farrar", memo)
        
    def test_multiple_impersonation_filings_tracking(self):
        """Test tracking multiple impersonation attempts"""
        # Add multiple suspicious filings
        filings = [
            {
                "filing_id": "multi_001",
                "filing_date": datetime(2025, 10, 1),
                "filing_channel": "court_online", 
                "submitter_name": "Peter Faucitt",
                "submitter_email": "pete@regima.com",
                "document_type": "Application",
                "document_hash": "hash_multi_001"
            },
            {
                "filing_id": "multi_002",
                "filing_date": datetime(2025, 10, 2),
                "filing_channel": "caselines",
                "submitter_name": "Peter Faucitt", 
                "submitter_email": "pete@regima.com",
                "document_type": "Affidavit",
                "document_hash": "hash_multi_002"
            }
        ]
        
        results = []
        for filing in filings:
            result = self.verifier.verify_court_filing_authenticity(filing)
            results.append(result)
        
        # Both should be flagged
        for result in results:
            self.assertEqual(result["authenticity_level"], "confirmed_impersonation")
        
        # Should have multiple alerts
        self.assertGreaterEqual(len(self.verifier.court_filing_verifier.impersonation_alerts), 2)
        
    def test_cross_reference_with_existing_evidence(self):
        """Test that court filing verification cross-references with existing evidence"""
        # Add evidence about email hijacking 
        email_hijacking_evidence = EvidenceItem(
            evidence_id="email_hijacking_ocr_001",
            source_document="OCR Screenshot 2025-06-20 Sage Account system",
            content_summary="OCR shows Pete@regima.com controlled by Rynette Farrar, not Peter Faucitt",
            reliability_score=0.95
        )
        
        self.verifier.add_evidence(email_hijacking_evidence)
        
        # Add filing using hijacked email
        filing = {
            "filing_id": "cross_ref_001",
            "filing_date": datetime(2025, 10, 1),
            "filing_channel": "email_submission",
            "submitter_name": "Peter Faucitt",
            "submitter_email": "pete@regima.com", 
            "document_type": "Notice",
            "document_hash": "hash_cross_ref_001"
        }
        
        result = self.verifier.verify_court_filing_authenticity(filing)
        
        # Should flag as impersonation and reference existing evidence
        self.assertEqual(result["authenticity_level"], "confirmed_impersonation")
        
        # Check that alert references OCR evidence
        alerts = self.verifier.court_filing_verifier.impersonation_alerts
        alert = list(alerts.values())[0]  # Get first alert
        
        evidence_refs = " ".join(alert.evidence_references)
        self.assertIn("OCR Screenshot", evidence_refs)
        
    def test_protection_against_za_services_attack_vector(self):
        """Test comprehensive protection against ZA services attack vector"""
        # Simulate multiple attack vectors through ZA services
        attack_vectors = [
            ("court_online", "Court Online Portal"),
            ("caselines", "Caselines System"),
            ("email_submission", "Email to Court")
        ]
        
        detected_attacks = []
        
        for i, (channel, description) in enumerate(attack_vectors):
            filing = {
                "filing_id": f"za_attack_{i+1:03d}",
                "filing_date": datetime(2025, 10, i+1),
                "filing_channel": channel,
                "submitter_name": "Peter Faucitt",  # Rynette impersonating Peter
                "submitter_email": "pete@regima.com",  # Using hijacked email
                "document_type": f"Document via {description}",
                "document_hash": f"hash_za_attack_{i+1:03d}"
            }
            
            result = self.verifier.verify_court_filing_authenticity(filing)
            
            if result["authenticity_level"] == "confirmed_impersonation":
                detected_attacks.append((channel, result))
        
        # All attack vectors should be detected  
        self.assertEqual(len(detected_attacks), len(attack_vectors))
        
        # Each should have appropriate warnings
        for channel, result in detected_attacks:
            indicators = " ".join(result["impersonation_indicators"])
            
            if channel in ["court_online", "caselines"]:
                self.assertIn("ZA court service", indicators)
            
            # All should reference email hijacking
            self.assertIn("controlled by Rynette Farrar", indicators)


class TestEmergencyProtectionScenarios(unittest.TestCase):
    """Test emergency scenarios where rapid protection is needed"""
    
    def setUp(self):
        self.verifier = InterdictVerificationSystem("EMERGENCY-2025-001")
    
    def test_urgent_interdict_impersonation_protection(self):
        """Test protection against urgent/emergency interdict filings using impersonation"""
        urgent_filing = {
            "filing_id": "urgent_emergency_001",
            "filing_date": datetime.now(),  # Filed right now
            "filing_channel": "court_online",
            "submitter_name": "Peter Faucitt",
            "submitter_email": "pete@regima.com",
            "document_type": "Urgent Interdict Application",
            "document_hash": "hash_urgent_001"
        }
        
        # Should be detected immediately
        result = self.verifier.verify_court_filing_authenticity(urgent_filing)
        
        self.assertEqual(result["authenticity_level"], "confirmed_impersonation")
        
        # Should have high-priority alert
        alerts = self.verifier.court_filing_verifier.impersonation_alerts
        alert = list(alerts.values())[0]
        self.assertEqual(alert.alert_level, "high")
        
        # Should recommend immediate action
        actions_text = " ".join(alert.recommended_actions)
        self.assertIn("immediately verify filer identity", actions_text.lower())


if __name__ == "__main__":
    unittest.main()