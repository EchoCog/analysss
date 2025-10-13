"""
Professional Evidence Management System
======================================

A comprehensive Content Management System (CMS) for legal evidence and case documentation.
Focuses on professional investigative analysis with clarity and accuracy.
"""

import hashlib
import json
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class EvidenceType(Enum):
    """Types of evidence in the system"""

    DOCUMENT = "document"
    COMMUNICATION = "communication"
    FINANCIAL = "financial"
    TECHNICAL = "technical"
    WITNESS = "witness"
    PHOTOGRAPHIC = "photographic"
    AUDIO = "audio"
    VIDEO = "video"
    DIGITAL = "digital"


class ClassificationLevel(Enum):
    """Security classification levels"""

    PUBLIC = "public"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    PRIVILEGED = "privileged"


class VerificationStatus(Enum):
    """Evidence verification status"""

    VERIFIED = "verified"
    PENDING = "pending_verification"
    DISPUTED = "disputed"
    AUTHENTICATED = "authenticated"
    REQUIRES_EXPERT = "requires_expert_analysis"


@dataclass
class EvidenceItem:
    """Individual evidence item in the management system"""

    evidence_id: str
    title: str
    evidence_type: EvidenceType
    classification: ClassificationLevel
    verification_status: VerificationStatus
    description: str
    source: str
    collection_date: datetime
    file_path: Optional[str] = None
    hash_value: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)
    related_items: Set[str] = field(default_factory=set)
    chain_of_custody: List[Dict[str, str]] = field(default_factory=list)
    analysis_notes: List[str] = field(default_factory=list)


@dataclass
class CaseFile:
    """Case file containing related evidence items"""

    case_id: str
    title: str
    description: str
    created_date: datetime
    updated_date: datetime
    evidence_items: Set[str] = field(default_factory=set)
    investigators: Set[str] = field(default_factory=set)
    keywords: Set[str] = field(default_factory=set)
    status: str = "active"


class EvidenceManagementSystem:
    """
    Professional Evidence Management System

    Provides comprehensive document and evidence filing capabilities
    with professional investigative standards.
    """

    def __init__(self, base_directory: str = None):
        self.base_directory = base_directory or "/tmp/evidence_repository"
        self.evidence_items: Dict[str, EvidenceItem] = {}
        self.case_files: Dict[str, CaseFile] = {}
        self.search_index: Dict[str, Set[str]] = {}
        self._ensure_directory_structure()

    def _ensure_directory_structure(self):
        """Ensure required directory structure exists"""
        directories = self._generate_comprehensive_folder_structure()

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def _generate_comprehensive_folder_structure(self) -> List[str]:
        """Generate comprehensive folder structure for evidence management"""
        base = self.base_directory
        directories = [
            # Root directory
            base,
            # Main evidence categories
            f"{base}/documents",
            f"{base}/documents/contracts",
            f"{base}/documents/legal",
            f"{base}/documents/reports",
            f"{base}/documents/correspondence",
            f"{base}/documents/forms",
            f"{base}/documents/statements",
            f"{base}/communications",
            f"{base}/communications/emails",
            f"{base}/communications/phone_records",
            f"{base}/communications/text_messages",
            f"{base}/communications/social_media",
            f"{base}/communications/instant_messages",
            f"{base}/communications/voicemails",
            f"{base}/financial",
            f"{base}/financial/bank_statements",
            f"{base}/financial/transaction_records",
            f"{base}/financial/invoices",
            f"{base}/financial/receipts",
            f"{base}/financial/tax_documents",
            f"{base}/financial/investment_records",
            f"{base}/technical",
            f"{base}/technical/digital_forensics",
            f"{base}/technical/network_logs",
            f"{base}/technical/system_logs",
            f"{base}/technical/database_exports",
            f"{base}/technical/code_analysis",
            f"{base}/technical/hardware_analysis",
            # Media evidence
            f"{base}/media",
            f"{base}/media/photographs",
            f"{base}/media/photographs/originals",
            f"{base}/media/photographs/processed",
            f"{base}/media/audio",
            f"{base}/media/audio/recordings",
            f"{base}/media/audio/transcriptions",
            f"{base}/media/video",
            f"{base}/media/video/surveillance",
            f"{base}/media/video/interviews",
            # Witness and testimony
            f"{base}/witness",
            f"{base}/witness/statements",
            f"{base}/witness/depositions",
            f"{base}/witness/interviews",
            f"{base}/witness/expert_opinions",
            # Case management
            f"{base}/cases",
            f"{base}/cases/active",
            f"{base}/cases/closed",
            f"{base}/cases/pending",
            # Metadata and system files
            f"{base}/metadata",
            f"{base}/metadata/evidence",
            f"{base}/metadata/cases",
            f"{base}/metadata/chain_of_custody",
            f"{base}/metadata/verification",
            # Analysis and reports
            f"{base}/analysis",
            f"{base}/analysis/timeline",
            f"{base}/analysis/reports",
            f"{base}/analysis/cross_reference",
            f"{base}/analysis/gap_analysis",
            f"{base}/analysis/verification",
            # Archive and backup
            f"{base}/archive",
            f"{base}/archive/completed_cases",
            f"{base}/archive/old_versions",
            f"{base}/backup",
            f"{base}/backup/daily",
            f"{base}/backup/weekly",
            f"{base}/backup/monthly",
            # Working directories
            f"{base}/working",
            f"{base}/working/staging",
            f"{base}/working/processing",
            f"{base}/working/review",
            f"{base}/working/temp",
            # Classification levels
            f"{base}/classified",
            f"{base}/classified/public",
            f"{base}/classified/confidential",
            f"{base}/classified/restricted",
            f"{base}/classified/privileged",
        ]

        return directories

    def add_evidence_item(
        self, evidence: EvidenceItem, file_content: bytes = None
    ) -> str:
        """Add evidence item to the system"""
        if evidence.evidence_id in self.evidence_items:
            raise ValueError(f"Evidence item {evidence.evidence_id} already exists")

        # Generate unique ID if not provided
        if not evidence.evidence_id:
            evidence.evidence_id = str(uuid.uuid4())

        # Store file content if provided
        if file_content:
            file_path = self._store_file(evidence, file_content)
            evidence.file_path = file_path
            evidence.hash_value = self._calculate_hash(file_content)

        # Add to chain of custody
        evidence.chain_of_custody.append(
            {
                "action": "evidence_added",
                "timestamp": datetime.now().isoformat(),
                "user": "system",
                "description": f"Evidence item {evidence.evidence_id} added to system",
            }
        )

        # Store evidence
        self.evidence_items[evidence.evidence_id] = evidence

        # Update search index
        self._update_search_index(evidence)

        # Save metadata
        self._save_evidence_metadata(evidence)

        return evidence.evidence_id

    def _store_file(self, evidence: EvidenceItem, content: bytes) -> str:
        """Store file content in appropriate directory"""
        storage_path = self._determine_storage_path(evidence)
        filename = self._generate_filename(evidence)
        file_path = f"{storage_path}/{filename}"

        # Ensure storage directory exists
        os.makedirs(storage_path, exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(content)

        return file_path

    def _determine_storage_path(self, evidence: EvidenceItem) -> str:
        """Determine appropriate storage path based on evidence type and classification"""
        base = self.base_directory
        evidence_type = evidence.evidence_type.value
        classification = evidence.classification.value

        # Create date-based subfolder
        date_folder = evidence.collection_date.strftime("%Y/%m")

        # Map evidence types to specific subdirectories
        type_mapping = {
            "document": self._get_document_subfolder(evidence),
            "communication": self._get_communication_subfolder(evidence),
            "financial": self._get_financial_subfolder(evidence),
            "technical": self._get_technical_subfolder(evidence),
            "photographic": f"{base}/media/photographs/originals/{date_folder}",
            "audio": f"{base}/media/audio/recordings/{date_folder}",
            "video": f"{base}/media/video/{date_folder}",
            "witness": f"{base}/witness/statements/{date_folder}",
            "digital": f"{base}/technical/digital_forensics/{date_folder}",
        }

        storage_path = type_mapping.get(
            evidence_type, f"{base}/{evidence_type}s/{date_folder}"
        )

        # Add classification level if sensitive
        if classification in ["confidential", "restricted", "privileged"]:
            storage_path = (
                f"{base}/classified/{classification}/{evidence_type}s/{date_folder}"
            )

        return storage_path

    def _get_document_subfolder(self, evidence: EvidenceItem) -> str:
        """Determine document subfolder based on content analysis"""
        base = self.base_directory
        date_folder = evidence.collection_date.strftime("%Y/%m")

        # Simple keyword-based categorization
        title_lower = evidence.title.lower()
        desc_lower = evidence.description.lower()
        content = f"{title_lower} {desc_lower}"

        if any(word in content for word in ["contract", "agreement", "terms"]):
            return f"{base}/documents/contracts/{date_folder}"
        elif any(word in content for word in ["court", "legal", "lawsuit", "motion"]):
            return f"{base}/documents/legal/{date_folder}"
        elif any(word in content for word in ["report", "analysis", "findings"]):
            return f"{base}/documents/reports/{date_folder}"
        elif any(word in content for word in ["letter", "email", "correspondence"]):
            return f"{base}/documents/correspondence/{date_folder}"
        elif any(word in content for word in ["statement", "declaration", "affidavit"]):
            return f"{base}/documents/statements/{date_folder}"
        else:
            return f"{base}/documents/{date_folder}"

    def _get_communication_subfolder(self, evidence: EvidenceItem) -> str:
        """Determine communication subfolder based on type"""
        base = self.base_directory
        date_folder = evidence.collection_date.strftime("%Y/%m")

        title_lower = evidence.title.lower()
        desc_lower = evidence.description.lower()
        content = f"{title_lower} {desc_lower}"

        if any(word in content for word in ["email", "e-mail"]):
            return f"{base}/communications/emails/{date_folder}"
        elif any(word in content for word in ["phone", "call", "telephone"]):
            return f"{base}/communications/phone_records/{date_folder}"
        elif any(word in content for word in ["text", "sms", "message"]):
            return f"{base}/communications/text_messages/{date_folder}"
        elif any(
            word in content for word in ["social", "facebook", "twitter", "instagram"]
        ):
            return f"{base}/communications/social_media/{date_folder}"
        else:
            return f"{base}/communications/{date_folder}"

    def _get_financial_subfolder(self, evidence: EvidenceItem) -> str:
        """Determine financial subfolder based on type"""
        base = self.base_directory
        date_folder = evidence.collection_date.strftime("%Y/%m")

        title_lower = evidence.title.lower()
        desc_lower = evidence.description.lower()
        content = f"{title_lower} {desc_lower}"

        if any(word in content for word in ["bank", "statement", "account"]):
            return f"{base}/financial/bank_statements/{date_folder}"
        elif any(word in content for word in ["transaction", "transfer", "payment"]):
            return f"{base}/financial/transaction_records/{date_folder}"
        elif any(word in content for word in ["invoice", "bill"]):
            return f"{base}/financial/invoices/{date_folder}"
        elif any(word in content for word in ["receipt"]):
            return f"{base}/financial/receipts/{date_folder}"
        elif any(word in content for word in ["tax", "irs"]):
            return f"{base}/financial/tax_documents/{date_folder}"
        else:
            return f"{base}/financial/{date_folder}"

    def _get_technical_subfolder(self, evidence: EvidenceItem) -> str:
        """Determine technical subfolder based on type"""
        base = self.base_directory
        date_folder = evidence.collection_date.strftime("%Y/%m")

        title_lower = evidence.title.lower()
        desc_lower = evidence.description.lower()
        content = f"{title_lower} {desc_lower}"

        if any(word in content for word in ["forensic", "disk", "drive"]):
            return f"{base}/technical/digital_forensics/{date_folder}"
        elif any(word in content for word in ["network", "router", "firewall"]):
            return f"{base}/technical/network_logs/{date_folder}"
        elif any(word in content for word in ["system", "server", "log"]):
            return f"{base}/technical/system_logs/{date_folder}"
        elif any(word in content for word in ["database", "sql", "export"]):
            return f"{base}/technical/database_exports/{date_folder}"
        else:
            return f"{base}/technical/{date_folder}"

    def _generate_filename(self, evidence: EvidenceItem) -> str:
        """Generate filename with proper sanitization and metadata"""
        # Sanitize title for filename
        safe_title = "".join(
            c for c in evidence.title if c.isalnum() or c in (" ", "-", "_")
        ).rstrip()
        safe_title = safe_title.replace(" ", "_")

        # Truncate if too long
        if len(safe_title) > 50:
            safe_title = safe_title[:50]

        # Create filename with evidence ID, date, and title
        date_str = evidence.collection_date.strftime("%Y%m%d")
        filename = f"{evidence.evidence_id}_{date_str}_{safe_title}"

        return filename

    def _calculate_hash(self, content: bytes) -> str:
        """Calculate SHA-256 hash of file content"""
        return hashlib.sha256(content).hexdigest()

    def _update_search_index(self, evidence: EvidenceItem):
        """Update search index with evidence keywords"""
        keywords = set()

        # Add title words
        keywords.update(evidence.title.lower().split())

        # Add description words
        keywords.update(evidence.description.lower().split())

        # Add tags
        keywords.update(tag.lower() for tag in evidence.tags)

        # Add source
        keywords.update(evidence.source.lower().split())

        # Update index
        for keyword in keywords:
            if keyword not in self.search_index:
                self.search_index[keyword] = set()
            self.search_index[keyword].add(evidence.evidence_id)

    def _save_evidence_metadata(self, evidence: EvidenceItem):
        """Save evidence metadata to JSON file"""
        metadata_file = f"{self.base_directory}/metadata/{evidence.evidence_id}.json"

        metadata = {
            "evidence_id": evidence.evidence_id,
            "title": evidence.title,
            "evidence_type": evidence.evidence_type.value,
            "classification": evidence.classification.value,
            "verification_status": evidence.verification_status.value,
            "description": evidence.description,
            "source": evidence.source,
            "collection_date": evidence.collection_date.isoformat(),
            "file_path": evidence.file_path,
            "hash_value": evidence.hash_value,
            "metadata": evidence.metadata,
            "tags": list(evidence.tags),
            "related_items": list(evidence.related_items),
            "chain_of_custody": evidence.chain_of_custody,
            "analysis_notes": evidence.analysis_notes,
        }

        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

    def create_case_file(self, case_id: str, title: str, description: str) -> CaseFile:
        """Create a new case file"""
        if case_id in self.case_files:
            raise ValueError(f"Case file {case_id} already exists")

        case_file = CaseFile(
            case_id=case_id,
            title=title,
            description=description,
            created_date=datetime.now(),
            updated_date=datetime.now(),
        )

        self.case_files[case_id] = case_file
        self._save_case_file_metadata(case_file)

        return case_file

    def add_evidence_to_case(self, case_id: str, evidence_id: str):
        """Link evidence item to case file"""
        if case_id not in self.case_files:
            raise ValueError(f"Case file {case_id} not found")

        if evidence_id not in self.evidence_items:
            raise ValueError(f"Evidence item {evidence_id} not found")

        self.case_files[case_id].evidence_items.add(evidence_id)
        self.case_files[case_id].updated_date = datetime.now()

        # Update evidence with case reference
        self.evidence_items[evidence_id].metadata["case_id"] = case_id

        # Update chain of custody
        self.evidence_items[evidence_id].chain_of_custody.append(
            {
                "action": "linked_to_case",
                "timestamp": datetime.now().isoformat(),
                "user": "system",
                "description": f"Linked to case {case_id}",
            }
        )

        self._save_evidence_metadata(self.evidence_items[evidence_id])
        self._save_case_file_metadata(self.case_files[case_id])

    def _save_case_file_metadata(self, case_file: CaseFile):
        """Save case file metadata to JSON file"""
        metadata_file = f"{self.base_directory}/cases/{case_file.case_id}.json"

        metadata = {
            "case_id": case_file.case_id,
            "title": case_file.title,
            "description": case_file.description,
            "created_date": case_file.created_date.isoformat(),
            "updated_date": case_file.updated_date.isoformat(),
            "evidence_items": list(case_file.evidence_items),
            "investigators": list(case_file.investigators),
            "keywords": list(case_file.keywords),
            "status": case_file.status,
        }

        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

    def search_evidence(self, query: str) -> List[EvidenceItem]:
        """Search for evidence items based on a query"""
        query_words = set(query.lower().split())
        results = set()

        for word in query_words:
            if word in self.search_index:
                results.update(self.search_index[word])

        return [self.evidence_items[eid] for eid in results]

    def get_evidence_item(self, evidence_id: str) -> Optional[EvidenceItem]:
        """Retrieve an evidence item by its ID"""
        return self.evidence_items.get(evidence_id)

    def get_case_file(self, case_id: str) -> Optional[CaseFile]:
        """Retrieve a case file by its ID"""
        return self.case_files.get(case_id)

    def generate_report(self, case_id: str) -> Dict[str, Any]:
        """Generate a comprehensive report for a case"""
        if case_id not in self.case_files:
            raise ValueError(f"Case file {case_id} not found")

        case_file = self.case_files[case_id]
        evidence_details = [
            self.evidence_items[eid] for eid in case_file.evidence_items
        ]

        return {
            "case_summary": case_file,
            "evidence_details": evidence_details,
            "total_evidence": len(evidence_details),
        }

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the evidence in the system."""
        summary = {
            "total_items": len(self.evidence_items),
            "items_by_type": {t.value: 0 for t in EvidenceType},
            "items_by_classification": {c.value: 0 for c in ClassificationLevel},
            "items_by_verification": {v.value: 0 for v in VerificationStatus},
        }
        for item in self.evidence_items.values():
            summary["items_by_type"][item.evidence_type.value] += 1
            summary["items_by_classification"][item.classification.value] += 1
            summary["items_by_verification"][item.verification_status.value] += 1
        return summary
