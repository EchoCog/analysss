#!/usr/bin/env python3
"""
Enhanced Timeline Processor for HyperGNN Framework
================================================

Processes timeline data with detailed status indicators and integrates
with the HyperGNN multi-model architecture.
"""

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from case_data_loader import InformationStatus
from frameworks.hypergnn_core import HyperGNNFramework
from src.models.hypergnn_framework_improved import (
    AnalysisConfiguration,
    AnalysisScope,
    ComplexityLevel,
)


class TimelineEntryType(Enum):
    """Types of timeline entries"""

    CRIMINAL_EVENT = "criminal_event"
    LEGAL_ACTION = "legal_action"
    COMMUNICATION = "communication"
    FINANCIAL_TRANSACTION = "financial_transaction"
    EVIDENCE_DISCOVERY = "evidence_discovery"
    SYSTEM_EVENT = "system_event"
    ADMINISTRATIVE = "administrative"


class VerificationLevel(Enum):
    """Levels of verification for timeline entries"""

    DOCUMENTED = "documented"  # Has supporting documentation
    WITNESSED = "witnessed"  # Has witness confirmation
    RECORDED = "recorded"  # Has digital/system record
    CORROBORATED = "corroborated"  # Multiple independent sources
    DISPUTED = "disputed"  # Conflicting evidence exists
    ALLEGED = "alleged"  # Single source, unverified


@dataclass
class TimelineEntry:
    """Enhanced timeline entry with status indicators"""

    entry_id: str
    date: datetime
    title: str
    description: str
    entry_type: TimelineEntryType
    participants: List[str] = field(default_factory=list)

    # Status indicators
    information_status: InformationStatus = InformationStatus.PARTIAL
    verification_level: VerificationLevel = VerificationLevel.ALLEGED
    evidence_references: List[str] = field(default_factory=list)
    source_reliability: float = 0.5  # 0.0 - 1.0 scale

    # Relationship data
    related_entries: List[str] = field(default_factory=list)
    impact_assessment: str = "unknown"
    legal_significance: str = "under_review"

    # Metadata
    creation_timestamp: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    tags: Set[str] = field(default_factory=set)
    analyst_notes: List[str] = field(default_factory=list)


class EnhancedTimelineProcessor:
    """Enhanced timeline processor with HyperGNN integration"""

    def __init__(self, case_id: str):
        self.case_id = case_id
        self.timeline_entries: Dict[str, TimelineEntry] = {}
        self.timeline_stats = {
            "total_entries": 0,
            "by_type": {},
            "by_status": {},
            "by_verification": {},
            "date_range": {"earliest": None, "latest": None},
        }

    def load_case_timeline(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Load timeline from case data and enhance with status indicators"""
        print("=== ENHANCED TIMELINE PROCESSING ===")

        # Process events from case data
        for event_data in case_data.get("events", []):
            self._process_case_event(event_data)

        # Add key case-specific events
        self._add_key_case_events()

        # Analyze timeline patterns
        self._analyze_timeline_patterns()

        return {
            "timeline_entries": len(self.timeline_entries),
            "statistics": self.timeline_stats,
            "key_patterns": self._identify_key_patterns(),
        }

    def _process_case_event(self, event_data: Dict[str, Any]):
        """Process a single event from case data"""
        try:
            event_date = (
                datetime.fromisoformat(event_data["date"])
                if event_data["date"]
                else None
            )
            if not event_date:
                return

            # Map event type
            event_type = self._map_event_type(event_data.get("event_type", "general"))

            # Determine verification level
            verification = self._determine_verification_level(event_data)

            # Determine information status
            info_status = InformationStatus(
                event_data.get("verification_status", "partial")
            )

            # Calculate source reliability
            reliability = self._calculate_source_reliability(event_data)

            entry = TimelineEntry(
                entry_id=event_data["event_id"],
                date=event_date,
                title=self._generate_title(event_data["description"]),
                description=event_data["description"],
                entry_type=event_type,
                participants=event_data.get("participants", []),
                information_status=info_status,
                verification_level=verification,
                evidence_references=event_data.get("evidence_references", []),
                source_reliability=reliability,
                impact_assessment=self._assess_impact(event_data),
                legal_significance=self._assess_legal_significance(event_data),
                tags=set(self._extract_tags(event_data)),
            )

            self.timeline_entries[entry.entry_id] = entry
            self._update_statistics(entry)

        except Exception as e:
            print(
                f"⚠️  Error processing event {event_data.get('event_id', 'unknown')}: {str(e)}"
            )

    def _add_key_case_events(self):
        """Add key case-specific events with detailed status tracking"""
        key_events = [
            {
                "entry_id": "kayla_murder_2023",
                "date": datetime(2023, 8, 1),  # Approximate date
                "title": "Kayla Pretorius Murder",
                "description": "Kayla Pretorius murdered, triggering subsequent financial activities",
                "entry_type": TimelineEntryType.CRIMINAL_EVENT,
                "participants": ["kayla_pretorius", "unknown_perpetrator"],
                "information_status": InformationStatus.CIRCUMSTANTIAL,
                "verification_level": VerificationLevel.ALLEGED,
                "source_reliability": 0.6,
                "impact_assessment": "CRITICAL - Trigger event for financial crimes",
                "legal_significance": "HOMICIDE - Primary criminal charge",
                "tags": {"murder", "trigger_event", "criminal_homicide"},
            },
            {
                "entry_id": "pete_email_hijacking",
                "date": datetime(2023, 8, 15),  # Estimated after murder
                "title": "Pete@regima.com Email Hijacking",
                "description": "Rynette Farrar gains control of Pete@regima.com email address",
                "entry_type": TimelineEntryType.SYSTEM_EVENT,
                "participants": ["rynette_farrar", "peter_faucitt"],
                "information_status": InformationStatus.VERIFIED,
                "verification_level": VerificationLevel.RECORDED,
                "source_reliability": 0.95,
                "impact_assessment": "HIGH - Enables information interception",
                "legal_significance": "IDENTITY_THEFT - Unauthorized use of identity",
                "tags": {"email_hijacking", "identity_theft", "ocr_verified"},
                "evidence_references": ["OCR_Screenshot_2025-06-20_Sage_Account"],
            },
            {
                "entry_id": "daniel_crime_report_june_10",
                "date": datetime(2025, 6, 10),
                "title": "Daniel Reports Peter for Murder-Linked Theft",
                "description": "Daniel Faucitt reports Peter for stealing funds after murder",
                "entry_type": TimelineEntryType.LEGAL_ACTION,
                "participants": ["daniel_faucitt", "peter_faucitt"],
                "information_status": InformationStatus.SAVED,
                "verification_level": VerificationLevel.DOCUMENTED,
                "source_reliability": 0.9,
                "impact_assessment": "HIGH - Victim exposes perpetrator",
                "legal_significance": "COMPLAINT - Official crime report",
                "tags": {"crime_report", "victim_report", "theft_after_murder"},
            },
            {
                "entry_id": "peter_court_order_august_19",
                "date": datetime(2025, 8, 19),
                "title": "Peter Files Court Order Against Daniel",
                "description": "Peter files court order 2025-137857 against Daniel (legal weaponization)",
                "entry_type": TimelineEntryType.LEGAL_ACTION,
                "participants": ["peter_faucitt", "daniel_faucitt"],
                "information_status": InformationStatus.SAVED,
                "verification_level": VerificationLevel.DOCUMENTED,
                "source_reliability": 0.95,
                "impact_assessment": "CRITICAL - Perpetrator attacks victim via courts",
                "legal_significance": "LEGAL_WEAPONIZATION - Abuse of legal process",
                "tags": {"court_order", "legal_weaponization", "perpetrator_vs_victim"},
                "evidence_references": ["Court_Order_2025-137857"],
            },
        ]

        for event_data in key_events:
            entry = TimelineEntry(
                entry_id=event_data["entry_id"],
                date=event_data["date"],
                title=event_data["title"],
                description=event_data["description"],
                entry_type=event_data["entry_type"],
                participants=event_data["participants"],
                information_status=event_data["information_status"],
                verification_level=event_data["verification_level"],
                evidence_references=event_data.get("evidence_references", []),
                source_reliability=event_data["source_reliability"],
                impact_assessment=event_data["impact_assessment"],
                legal_significance=event_data["legal_significance"],
                tags=set(event_data["tags"]),
            )

            self.timeline_entries[entry.entry_id] = entry
            self._update_statistics(entry)
            print(
                f"✅ Added key event: {entry.title} ({entry.information_status.value})"
            )

    def _map_event_type(self, event_type_str: str) -> TimelineEntryType:
        """Map string event type to enum"""
        type_mapping = {
            "criminal_homicide": TimelineEntryType.CRIMINAL_EVENT,
            "financial_crime": TimelineEntryType.FINANCIAL_TRANSACTION,
            "legal_proceeding": TimelineEntryType.LEGAL_ACTION,
            "communication": TimelineEntryType.COMMUNICATION,
            "report": TimelineEntryType.ADMINISTRATIVE,
            "general": TimelineEntryType.ADMINISTRATIVE,
        }
        return type_mapping.get(event_type_str, TimelineEntryType.ADMINISTRATIVE)

    def _determine_verification_level(
        self, event_data: Dict[str, Any]
    ) -> VerificationLevel:
        """Determine verification level based on event data"""
        description = event_data.get("description", "").lower()
        evidence_refs = event_data.get("evidence_references", [])

        if "ocr" in str(evidence_refs).lower() or "screenshot" in description:
            return VerificationLevel.RECORDED
        elif "court" in description or "filed" in description:
            return VerificationLevel.DOCUMENTED
        elif "reported" in description or "complaint" in description:
            return VerificationLevel.DOCUMENTED
        elif "alleged" in description or "claimed" in description:
            return VerificationLevel.ALLEGED
        elif len(evidence_refs) > 1:
            return VerificationLevel.CORROBORATED
        else:
            return VerificationLevel.ALLEGED

    def _calculate_source_reliability(self, event_data: Dict[str, Any]) -> float:
        """Calculate source reliability score"""
        base_score = 0.5
        evidence_refs = event_data.get("evidence_references", [])
        description = event_data.get("description", "").lower()

        # Increase for OCR/system evidence
        if "ocr" in str(evidence_refs).lower():
            base_score += 0.3

        # Increase for court documents
        if "court" in description:
            base_score += 0.2

        # Increase for multiple sources
        if len(evidence_refs) > 1:
            base_score += 0.15

        # Decrease for disputed/alleged items
        if "alleged" in description:
            base_score -= 0.2

        return min(1.0, max(0.0, base_score))

    def _assess_impact(self, event_data: Dict[str, Any]) -> str:
        """Assess the impact level of an event"""
        description = event_data.get("description", "").lower()
        event_type = event_data.get("event_type", "")

        if "murder" in description or event_type == "criminal_homicide":
            return "CRITICAL - Life and death matter"
        elif "court" in description or "legal" in description:
            return "HIGH - Legal consequences"
        elif "financial" in description or "money" in description:
            return "MODERATE - Financial impact"
        elif "email" in description or "communication" in description:
            return "MODERATE - Information flow impact"
        else:
            return "LOW - Administrative impact"

    def _assess_legal_significance(self, event_data: Dict[str, Any]) -> str:
        """Assess legal significance of an event"""
        description = event_data.get("description", "").lower()
        event_type = event_data.get("event_type", "")

        if "murder" in description:
            return "HOMICIDE - Capital crime"
        elif "theft" in description or "fraud" in description:
            return "FINANCIAL_CRIME - Felony level"
        elif "court" in description and "order" in description:
            return "CIVIL_PROCEEDING - Court action"
        elif "report" in description and "crime" in description:
            return "COMPLAINT - Official report"
        elif "email" in description and "control" in description:
            return "IDENTITY_THEFT - Unauthorized access"
        else:
            return "ADMINISTRATIVE - Under review"

    def _extract_tags(self, event_data: Dict[str, Any]) -> List[str]:
        """Extract relevant tags from event data"""
        tags = []
        description = event_data.get("description", "").lower()
        event_type = event_data.get("event_type", "")

        # Add type-based tags
        tags.append(event_type)

        # Add content-based tags
        if "murder" in description:
            tags.extend(["murder", "criminal", "homicide"])
        if "theft" in description or "stolen" in description:
            tags.extend(["theft", "financial_crime"])
        if "court" in description:
            tags.extend(["legal", "court_action"])
        if "email" in description:
            tags.extend(["communication", "email"])
        if "ocr" in str(event_data.get("evidence_references", [])).lower():
            tags.extend(["ocr_verified", "technical_evidence"])

        return tags

    def _generate_title(self, description: str) -> str:
        """Generate a concise title from description"""
        # Take first 50 characters and clean up
        title = description[:50].strip()
        if len(description) > 50:
            title += "..."
        return title

    def _update_statistics(self, entry: TimelineEntry):
        """Update timeline statistics"""
        self.timeline_stats["total_entries"] += 1

        # Update by type
        type_key = entry.entry_type.value
        if type_key not in self.timeline_stats["by_type"]:
            self.timeline_stats["by_type"][type_key] = 0
        self.timeline_stats["by_type"][type_key] += 1

        # Update by status
        status_key = entry.information_status.value
        if status_key not in self.timeline_stats["by_status"]:
            self.timeline_stats["by_status"][status_key] = 0
        self.timeline_stats["by_status"][status_key] += 1

        # Update by verification
        verif_key = entry.verification_level.value
        if verif_key not in self.timeline_stats["by_verification"]:
            self.timeline_stats["by_verification"][verif_key] = 0
        self.timeline_stats["by_verification"][verif_key] += 1

        # Update date range
        if (
            self.timeline_stats["date_range"]["earliest"] is None
            or entry.date < self.timeline_stats["date_range"]["earliest"]
        ):
            self.timeline_stats["date_range"]["earliest"] = entry.date

        if (
            self.timeline_stats["date_range"]["latest"] is None
            or entry.date > self.timeline_stats["date_range"]["latest"]
        ):
            self.timeline_stats["date_range"]["latest"] = entry.date

    def _analyze_timeline_patterns(self):
        """Analyze patterns in the timeline"""
        print(f"\n=== TIMELINE PATTERN ANALYSIS ===")

        # Sort entries by date
        sorted_entries = sorted(self.timeline_entries.values(), key=lambda x: x.date)

        # Identify key patterns
        patterns = {
            "victim_to_perpetrator_timeline": self._analyze_victim_perpetrator_pattern(
                sorted_entries
            ),
            "legal_weaponization_gap": self._analyze_legal_gap(sorted_entries),
            "evidence_tampering_window": self._analyze_evidence_tampering(
                sorted_entries
            ),
        }

        self.timeline_stats["patterns"] = patterns

        for pattern_name, pattern_data in patterns.items():
            if pattern_data:
                print(f"✅ Pattern identified: {pattern_name}")
                print(f"   {pattern_data.get('description', 'No description')}")

    def _analyze_victim_perpetrator_pattern(
        self, sorted_entries: List[TimelineEntry]
    ) -> Dict:
        """Analyze the victim reporting -> perpetrator legal attack pattern"""
        crime_report = None
        court_attack = None

        for entry in sorted_entries:
            if (
                "crime_report" in entry.tags
                and "daniel" in str(entry.participants).lower()
            ):
                crime_report = entry
            elif (
                "court_order" in entry.tags
                and "peter" in str(entry.participants).lower()
            ):
                court_attack = entry

        if crime_report and court_attack:
            gap_days = (court_attack.date - crime_report.date).days
            return {
                "description": f"Victim reported crime on {crime_report.date.date()}, perpetrator attacked via courts {gap_days} days later",
                "gap_days": gap_days,
                "crime_report_date": crime_report.date,
                "court_attack_date": court_attack.date,
                "pattern_type": "legal_weaponization",
            }

        return {}

    def _analyze_legal_gap(self, sorted_entries: List[TimelineEntry]) -> Dict:
        """Analyze gaps in legal proceedings"""
        legal_entries = [
            e for e in sorted_entries if e.entry_type == TimelineEntryType.LEGAL_ACTION
        ]

        if len(legal_entries) >= 2:
            first = legal_entries[0]
            last = legal_entries[-1]
            gap_days = (last.date - first.date).days

            return {
                "description": f"Legal activity span: {gap_days} days from first to last action",
                "first_action": first.title,
                "last_action": last.title,
                "gap_days": gap_days,
            }

        return {}

    def _analyze_evidence_tampering(self, sorted_entries: List[TimelineEntry]) -> Dict:
        """Analyze potential evidence tampering windows"""
        evidence_events = [
            e for e in sorted_entries if "evidence" in str(e.tags).lower()
        ]
        communication_events = [
            e for e in sorted_entries if e.entry_type == TimelineEntryType.COMMUNICATION
        ]

        if evidence_events and communication_events:
            return {
                "description": f"Evidence tampering window identified: {len(evidence_events)} evidence events and {len(communication_events)} communications",
                "evidence_count": len(evidence_events),
                "communication_count": len(communication_events),
            }

        return {}

    def _identify_key_patterns(self) -> Dict[str, Any]:
        """Identify key patterns in the timeline"""
        return {
            "total_timeline_span": self._calculate_timeline_span(),
            "critical_events": self._identify_critical_events(),
            "verification_reliability": self._calculate_verification_reliability(),
            "legal_action_concentration": self._analyze_legal_concentration(),
        }

    def _calculate_timeline_span(self) -> Dict[str, Any]:
        """Calculate total timeline span"""
        if not self.timeline_entries:
            return {}

        dates = [entry.date for entry in self.timeline_entries.values()]
        earliest = min(dates)
        latest = max(dates)
        span_days = (latest - earliest).days

        return {
            "earliest_date": earliest.date(),
            "latest_date": latest.date(),
            "total_days": span_days,
            "years_span": round(span_days / 365.25, 2),
        }

    def _identify_critical_events(self) -> List[Dict[str, Any]]:
        """Identify critical events in the timeline"""
        critical_events = []

        for entry in self.timeline_entries.values():
            if (
                entry.impact_assessment.startswith("CRITICAL")
                or "murder" in entry.tags
                or "legal_weaponization" in entry.tags
            ):

                critical_events.append(
                    {
                        "entry_id": entry.entry_id,
                        "date": entry.date.date(),
                        "title": entry.title,
                        "impact": entry.impact_assessment,
                        "legal_significance": entry.legal_significance,
                        "verification_status": entry.information_status.value,
                    }
                )

        return sorted(critical_events, key=lambda x: x["date"])

    def _calculate_verification_reliability(self) -> Dict[str, Any]:
        """Calculate overall verification reliability"""
        if not self.timeline_entries:
            return {}

        total_reliability = sum(
            entry.source_reliability for entry in self.timeline_entries.values()
        )
        avg_reliability = total_reliability / len(self.timeline_entries)

        high_reliability = len(
            [e for e in self.timeline_entries.values() if e.source_reliability >= 0.8]
        )
        low_reliability = len(
            [e for e in self.timeline_entries.values() if e.source_reliability < 0.5]
        )

        return {
            "average_reliability": round(avg_reliability, 2),
            "high_reliability_count": high_reliability,
            "low_reliability_count": low_reliability,
            "reliability_percentage": round(avg_reliability * 100, 1),
        }

    def _analyze_legal_concentration(self) -> Dict[str, Any]:
        """Analyze concentration of legal actions"""
        legal_entries = [
            e
            for e in self.timeline_entries.values()
            if e.entry_type == TimelineEntryType.LEGAL_ACTION
        ]

        if not legal_entries:
            return {}

        # Group by month
        monthly_counts = {}
        for entry in legal_entries:
            month_key = entry.date.strftime("%Y-%m")
            if month_key not in monthly_counts:
                monthly_counts[month_key] = 0
            monthly_counts[month_key] += 1

        peak_month = max(monthly_counts.items(), key=lambda x: x[1])

        return {
            "total_legal_actions": len(legal_entries),
            "peak_month": peak_month[0],
            "peak_month_count": peak_month[1],
            "monthly_distribution": monthly_counts,
        }

    def export_enhanced_timeline(self) -> Dict[str, Any]:
        """Export enhanced timeline with all status indicators"""
        return {
            "case_id": self.case_id,
            "export_timestamp": datetime.now().isoformat(),
            "timeline_entries": {
                entry_id: {
                    "entry_id": entry.entry_id,
                    "date": entry.date.isoformat(),
                    "title": entry.title,
                    "description": entry.description,
                    "entry_type": entry.entry_type.value,
                    "participants": entry.participants,
                    "information_status": entry.information_status.value,
                    "verification_level": entry.verification_level.value,
                    "evidence_references": entry.evidence_references,
                    "source_reliability": entry.source_reliability,
                    "impact_assessment": entry.impact_assessment,
                    "legal_significance": entry.legal_significance,
                    "tags": list(entry.tags),
                    "related_entries": entry.related_entries,
                    "analyst_notes": entry.analyst_notes,
                }
                for entry_id, entry in self.timeline_entries.items()
            },
            "statistics": self.timeline_stats,
            "status_summary": self._generate_status_summary(),
        }

    def _generate_status_summary(self) -> Dict[str, Any]:
        """Generate comprehensive status summary"""
        return {
            "total_entries": len(self.timeline_entries),
            "information_status_distribution": self.timeline_stats.get("by_status", {}),
            "verification_level_distribution": self.timeline_stats.get(
                "by_verification", {}
            ),
            "entry_type_distribution": self.timeline_stats.get("by_type", {}),
            "reliability_metrics": self._calculate_verification_reliability(),
            "critical_events_count": len(self._identify_critical_events()),
            "timeline_span": self._calculate_timeline_span(),
        }

    def generate_timeline_report(self) -> str:
        """Generate detailed timeline report"""
        report_lines = [
            f"# Enhanced Timeline Analysis Report - {self.case_id}",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total Entries:** {len(self.timeline_entries)}",
            "",
            "## Status Distribution",
            "",
        ]

        # Status breakdown
        for status, count in self.timeline_stats.get("by_status", {}).items():
            report_lines.append(f"- **{status.upper()}**: {count} entries")

        report_lines.extend(["", "## Verification Levels", ""])

        for level, count in self.timeline_stats.get("by_verification", {}).items():
            report_lines.append(f"- **{level.upper()}**: {count} entries")

        # Critical events
        critical_events = self._identify_critical_events()
        if critical_events:
            report_lines.extend(["", "## Critical Events", ""])

            for event in critical_events:
                report_lines.extend(
                    [
                        f"### {event['title']}",
                        f"- **Date:** {event['date']}",
                        f"- **Impact:** {event['impact']}",
                        f"- **Legal Significance:** {event['legal_significance']}",
                        f"- **Status:** {event['verification_status']}",
                        "",
                    ]
                )

        # Key patterns
        patterns = self.timeline_stats.get("patterns", {})
        if patterns:
            report_lines.extend(["## Key Patterns Identified", ""])

            for pattern_name, pattern_data in patterns.items():
                if pattern_data:
                    report_lines.extend(
                        [
                            f"### {pattern_name.replace('_', ' ').title()}",
                            f"- {pattern_data.get('description', 'No description available')}",
                            "",
                        ]
                    )

        return "\n".join(report_lines)

    def integrate_ocr_revelations(self):
        """Integrate OCR revelations into timeline analysis

        Updates timeline entries to reflect that Pete@regima.com is controlled
        by Rynette Farrar, not Peter Faucitt
        """
        print("=== INTEGRATING OCR REVELATIONS INTO TIMELINE ===")

        # Add OCR revelation as a critical timeline entry
        ocr_revelation_entry = TimelineEntry(
            entry_id="ocr_revelation_pete_email_hijacking",
            date=datetime(2025, 6, 20),
            title="OCR Revelation: Pete@regima.com Email Hijacking Discovered",
            description="OCR analysis of Sage Account system screenshots reveals that Pete@regima.com is controlled by Rynette Farrar, not Peter Faucitt. This finding invalidates all assumptions about Peter receiving emails directly.",
            entry_type=TimelineEntryType.EVIDENCE_DISCOVERY,
            participants=["peter_faucitt", "rynette_farrar"],
            information_status=InformationStatus.VERIFIED,
            verification_level=VerificationLevel.RECORDED,
            evidence_references=["OCR Screenshot 2025-06-20 Sage Account system"],
            source_reliability=1.0,  # Highest reliability - system screenshot
            impact_assessment="CRITICAL - Invalidates all direct email receipt claims",
            legal_significance="CRITICAL - Provides perjury evidence",
            attributes={
                "revelation_type": "email_hijacking_evidence",
                "legal_implications": [
                    "identity_theft",
                    "perjury_evidence",
                    "information_warfare",
                ],
                "affected_communications": "All emails to Pete@regima.com",
                "impossibility_claims": "Any Peter claims of direct email receipt",
            },
        )

        self.timeline_entries["ocr_revelation_pete_email_hijacking"] = (
            ocr_revelation_entry
        )

        # Update existing timeline entries that involve email communications
        email_entries_updated = 0
        for entry_id, entry in self.timeline_entries.items():
            # Look for entries that might involve Peter receiving emails
            if (
                "email" in entry.description.lower()
                or "pete@regima.com" in entry.description.lower()
                or (
                    "peter" in entry.description.lower()
                    and "receiv" in entry.description.lower()
                )
            ):

                # Add OCR context to the entry
                if "ocr_context" not in entry.attributes:
                    entry.attributes["ocr_context"] = {
                        "email_control_revelation": "Pete@regima.com controlled by Rynette Farrar",
                        "direct_receipt_impossible": True,
                        "actual_recipient": "Rynette Farrar",
                        "verification_required": "Check if Peter actually knew content vs claimed knowledge",
                    }

                    # Downgrade verification level if it was based on direct email receipt
                    if entry.verification_level in [
                        VerificationLevel.DOCUMENTED,
                        VerificationLevel.RECORDED,
                    ]:
                        entry.verification_level = VerificationLevel.DISPUTED
                        entry.attributes["verification_downgrade_reason"] = (
                            "OCR reveals email hijacking"
                        )

                    email_entries_updated += 1

        print(f"✅ Added OCR revelation entry")
        print(
            f"✅ Updated {email_entries_updated} existing email-related entries with OCR context"
        )

        # Update timeline statistics
        self._update_statistics_after_ocr()

    def _update_statistics_after_ocr(self):
        """Update timeline statistics after OCR integration"""
        # Recalculate statistics to include OCR updates
        self.timeline_stats["total_entries"] = len(self.timeline_entries)

        # Add OCR-specific statistics
        ocr_affected_entries = sum(
            1
            for entry in self.timeline_entries.values()
            if "ocr_context" in entry.attributes
        )

        self.timeline_stats["ocr_integration"] = {
            "affected_entries": ocr_affected_entries,
            "revelation_date": "2025-06-20",
            "critical_finding": "Pete@regima.com email hijacking by Rynette Farrar",
            "verification_impact": "Multiple entries downgraded from DOCUMENTED/RECORDED to DISPUTED",
        }

    def export_ocr_timeline_corrections(self) -> Dict[str, Any]:
        """Export timeline corrections based on OCR revelations

        Returns:
            Dictionary containing corrected timeline information
        """
        corrections = {
            "ocr_revelation": {
                "date": "2025-06-20",
                "finding": "Pete@regima.com controlled by Rynette Farrar, not Peter Faucitt",
                "evidence": "OCR Screenshot Sage Account system",
            },
            "affected_entries": [],
            "verification_downgrades": [],
            "impossibility_claims": [],
        }

        for entry_id, entry in self.timeline_entries.items():
            if "ocr_context" in entry.attributes:
                corrections["affected_entries"].append(
                    {
                        "entry_id": entry_id,
                        "date": entry.date.isoformat(),
                        "title": entry.title,
                        "ocr_impact": entry.attributes["ocr_context"],
                    }
                )

                if entry.verification_level == VerificationLevel.DISPUTED:
                    corrections["verification_downgrades"].append(
                        {
                            "entry_id": entry_id,
                            "reason": entry.attributes.get(
                                "verification_downgrade_reason"
                            ),
                            "new_verification_level": "DISPUTED",
                        }
                    )

                if entry.attributes["ocr_context"].get("direct_receipt_impossible"):
                    corrections["impossibility_claims"].append(
                        {
                            "entry_id": entry_id,
                            "legal_implication": "Any direct email receipt claim is impossible (perjury evidence)",
                        }
                    )

        return corrections


def main():
    """Main function to test enhanced timeline processor"""
    print("=== ENHANCED TIMELINE PROCESSOR TEST ===")

    # Load case data
    case_data_file = "/tmp/case_data_extracted.json"
    if Path(case_data_file).exists():
        with open(case_data_file, "r") as f:
            case_data = json.load(f)
    else:
        print("Case data file not found. Running case data loader first...")
        from case_data_loader import CaseDataLoader

        loader = CaseDataLoader("case_2025_137857")
        loader.load_case_documents()
        case_data = loader.export_case_data()

    # Process timeline
    processor = EnhancedTimelineProcessor("case_2025_137857")
    results = processor.load_case_timeline(case_data)

    print(f"\n=== TIMELINE PROCESSING RESULTS ===")
    print(f"Timeline entries: {results['timeline_entries']}")
    print(f"Statistics: {json.dumps(results['statistics'], indent=2, default=str)}")

    # Generate enhanced timeline export
    enhanced_timeline = processor.export_enhanced_timeline()

    # Save enhanced timeline
    output_file = "/tmp/enhanced_timeline_case_2025_137857.json"
    with open(output_file, "w") as f:
        json.dump(enhanced_timeline, f, indent=2, default=str)

    # Generate report
    report = processor.generate_timeline_report()
    report_file = "/tmp/enhanced_timeline_report.md"
    with open(report_file, "w") as f:
        f.write(report)

    print(f"\n✅ Enhanced timeline saved to: {output_file}")
    print(f"✅ Timeline report saved to: {report_file}")

    return enhanced_timeline


if __name__ == "__main__":
    main()
