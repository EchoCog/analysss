import unittest
import os
import shutil
from datetime import datetime
from analysis.frameworks.evidence_management import (
    EvidenceManagementSystem,
    EvidenceItem,
    EvidenceType,
    ClassificationLevel,
    VerificationStatus,
)


class TestEvidenceManagementSystem(unittest.TestCase):

    def setUp(self):
        self.test_dir = "/tmp/test_evidence_management"
        os.makedirs(self.test_dir, exist_ok=True)
        self.ems = EvidenceManagementSystem(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_add_and_get_evidence_item(self):
        evidence_item = EvidenceItem(
            evidence_id="test_evidence_001",
            title="Test Evidence",
            evidence_type=EvidenceType.DOCUMENT,
            classification=ClassificationLevel.CONFIDENTIAL,
            verification_status=VerificationStatus.VERIFIED,
            description="This is a test evidence item.",
            source="Test Case",
            collection_date=datetime.now(),
        )
        self.ems.add_evidence_item(evidence_item)
        retrieved_item = self.ems.get_evidence_item("test_evidence_001")
        self.assertIsNotNone(retrieved_item)
        self.assertEqual(retrieved_item.title, "Test Evidence")


if __name__ == "__main__":
    unittest.main()
