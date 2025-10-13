"""
Communication & Litigation Abuse Verification Tracker (REVISED)

This tool now tracks not only communication interception but also the abuse of legal processes,
identifying patterns of malicious prosecution and witness intimidation.

It tracks:
1.  Communication interception and knowledge verification.
2.  The sequence of legal filings to detect retaliatory patterns.
3.  The use of fabricated claims in court applications.
4.  Acts of witness intimidation through legal channels.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class VerificationStatus(Enum):
    CONFIRMED = "confirmed"
    DISPUTED = "disputed"
    UNVERIFIED = "unverified"
    IMPOSSIBLE = "impossible"
    MALICIOUS = "malicious"  # For legal actions


class EventType(Enum):
    COMMUNICATION = "communication"
    LEGAL_FILING = "legal_filing"


@dataclass
class TrackedEvent:
    event_id: str
    date: datetime
    event_type: EventType
    description: str
    actors: List[str]
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    evidence_ids: List[str] = None


class VerificationTracker:
    """Main verification tracking system, now including litigation abuse."""

    def __init__(self):
        self.events: Dict[str, TrackedEvent] = {}
        self.evidence_repository: Dict[str, str] = {}

    def add_event(self, event: TrackedEvent):
        if event.evidence_ids is None:
            event.evidence_ids = []
        self.events[event.event_id] = event

    def add_evidence(self, evidence_id: str, description: str):
        self.evidence_repository[evidence_id] = description

    def analyze_litigation_pattern(self) -> Optional[Dict]:
        """Analyzes the sequence of legal filings for patterns of abuse."""
        filings = sorted(
            [e for e in self.events.values() if e.event_type == EventType.LEGAL_FILING],
            key=lambda x: x.date
        )

        if len(filings) < 2:
            return None

        # Check for a pattern: Fraudulent filing followed by a malicious one
        first_filing = filings[0]
        second_filing = filings[1]

        is_first_fraudulent = first_filing.verification_status == VerificationStatus.MALICIOUS
        is_second_malicious = second_filing.verification_status == VerificationStatus.MALICIOUS

        # Check for retaliatory timing
        crime_report_event = self.events.get("crime_report_june_10")
        is_retaliatory = False
        if crime_report_event:
            if first_filing.date > crime_report_event.date:
                is_retaliatory = True

        if is_first_fraudulent and is_second_malicious and is_retaliatory:
            return {
                "pattern": "Malicious Prosecution and Witness Intimidation",
                "description": "A pattern of retaliatory and fraudulent litigation following the reporting of a crime, escalating to active witness intimidation.",
                "evidence": {
                    "Initial Crime Report": crime_report_event.event_id,
                    "First Fraudulent Filing": first_filing.event_id,
                    "Second Malicious Filing": second_filing.event_id
                },
                "recommendation": "Submit entire pattern to Hawks as evidence of a continuing criminal enterprise to obstruct justice."
            }

        return None

    def generate_prosecution_summary(self) -> str:
        """Generates a summary for prosecutors."""
        summary = ["# PROSECUTION SUMMARY: Litigation Abuse & Witness Intimidation\n"]
        pattern_analysis = self.analyze_litigation_pattern()

        if pattern_analysis:
            summary.append(f'## Pattern Detected: {pattern_analysis["pattern"]}\n')
            summary.append(f'**Description**: {pattern_analysis["description"]}\n')
            summary.append("### Sequence of Events:")
            summary.append(f'1. **Crime Report**: {pattern_analysis["evidence"]["Initial Crime Report"]}')
            summary.append(f'2. **Retaliation 1 (Perjury)**: {pattern_analysis["evidence"]["First Fraudulent Filing"]}')
            summary.append(f'3. **Retaliation 2 (Intimidation)**: {pattern_analysis["evidence"]["Second Malicious Filing"]}\n')
            summary.append(f'**Recommendation**: {pattern_analysis["recommendation"]}')

        return "\n".join(summary)


# Example Usage:
if __name__ == "__main__":
    tracker = VerificationTracker()

    # Add evidence
    tracker.add_evidence("E01", "Email from Daniel to Bantjies/Peter dated June 10, 2025, reporting murder/fraud.")
    tracker.add_evidence("E02", "First Interdict application, containing perjured statements.")
    tracker.add_evidence("E03", "Second Interdict application, containing fabricated claims for medical testing.")
    tracker.add_evidence("E04", "Bank statements disproving claims in the second interdict.")

    # Add events
    tracker.add_event(TrackedEvent(
        event_id="crime_report_june_10",
        date=datetime(2025, 6, 10),
        event_type=EventType.COMMUNICATION,
        description="Daniel Faucitt reports murder and fraud to Peter Faucitt and Danie Bantjies.",
        actors=["Daniel Faucitt", "Peter Faucitt", "Danie Bantjies"],
        verification_status=VerificationStatus.CONFIRMED,
        evidence_ids=["E01"]
    ))

    tracker.add_event(TrackedEvent(
        event_id="first_interdict_aug_19",
        date=datetime(2025, 8, 19),
        event_type=EventType.LEGAL_FILING,
        description="Peter Faucitt files first interdict based on perjured affidavits.",
        actors=["Peter Faucitt"],
        verification_status=VerificationStatus.MALICIOUS, # Marked as malicious due to perjury
        evidence_ids=["E01", "E02"]
    ))

    tracker.add_event(TrackedEvent(
        event_id="second_interdict_oct_06",
        date=datetime(2025, 10, 6),
        event_type=EventType.LEGAL_FILING,
        description="Peter Faucitt files second interdict to force medical testing.",
        actors=["Peter Faucitt"],
        verification_status=VerificationStatus.MALICIOUS,
        evidence_ids=["E03", "E04"]
    ))

    # Generate the prosecution summary
    prosecution_summary = tracker.generate_prosecution_summary()
    print(prosecution_summary)

    # Save the summary to a file
    with open("/home/ubuntu/analysis/case_2025_137857/analysis/LITIGATION_ABUSE_SUMMARY.md", "w") as f:
        f.write(prosecution_summary)

