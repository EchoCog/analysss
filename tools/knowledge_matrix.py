#!/usr/bin/env python3
"""
Knowledge Matrix Tool for Criminal Case Analysis

This tool implements the enhanced knowledge matrix that separates:
1. Address/Channel ownership vs actual recipient control
2. Confirmed vs assumed knowledge
3. Direct vs intermediary information flow
4. Verification status of all communications

Based on OCR revelations showing email CC deception patterns.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class KnowledgeLevel(Enum):
    """Knowledge certainty levels"""

    DIRECT = "direct"  # First-hand knowledge
    CONFIRMED = "confirmed"  # Third-party but verified
    REPORTED = "reported"  # Third-party, unverified
    ASSUMED = "assumed"  # Inferred/assumed
    DISPUTED = "disputed"  # Contradictory evidence


class ChannelType(Enum):
    """Communication channel types"""

    EMAIL = "email"
    PHONE = "phone"
    PHYSICAL = "physical"
    SYSTEM = "system"
    PROXY = "proxy"
    UNKNOWN = "unknown"


@dataclass
class CommunicationChannel:
    """Represents a communication channel with separation of address vs control"""

    address: str  # The visible address/number
    channel_type: ChannelType  # Type of communication
    nominal_owner: str  # Who the address appears to belong to
    actual_controller: str  # Who actually controls/receives
    verified_controller: bool  # Whether actual control is verified
    access_method: str  # How the controller accesses (direct/proxy/etc)
    verification_source: str  # Source of verification info
    last_verified: Optional[datetime] = None


@dataclass
class KnowledgeEntry:
    """Individual knowledge entry with verification status"""

    person: str  # Person who has the knowledge
    event: str  # What they know about
    knowledge_level: KnowledgeLevel  # How certain the knowledge is
    information_source: str  # Where the info came from
    verification_status: str  # Confirmed/Unconfirmed/Disputed
    date: datetime  # When they gained knowledge
    intermediaries: List[str]  # Who was between source and person
    channel_used: Optional[str] = None  # Communication channel if applicable


class KnowledgeMatrix:
    """Enhanced knowledge matrix tracking address vs recipient separation"""

    def __init__(self):
        self.communication_channels: Dict[str, CommunicationChannel] = {}
        self.knowledge_entries: List[KnowledgeEntry] = []
        self.assumptions_log: List[Dict] = []  # Log of assumptions that need updating
        self.verification_requirements: List[Dict] = []  # What needs verification

    def register_channel(self, channel: CommunicationChannel):
        """Register a communication channel with ownership details"""
        self.communication_channels[channel.address] = channel

        # Log assumption if controller different from nominal owner
        if channel.nominal_owner != channel.actual_controller:
            self.log_assumption(
                {
                    "type": "address_control_discrepancy",
                    "address": channel.address,
                    "nominal_owner": channel.nominal_owner,
                    "actual_controller": channel.actual_controller,
                    "verified": channel.verified_controller,
                    "implications": "All communications to this address go to different person",
                }
            )

    def add_knowledge_entry(self, entry: KnowledgeEntry):
        """Add a knowledge entry with verification tracking"""
        self.knowledge_entries.append(entry)

        # Check if this involves a controlled channel
        if entry.channel_used and entry.channel_used in self.communication_channels:
            channel = self.communication_channels[entry.channel_used]
            if channel.nominal_owner != channel.actual_controller:
                # Flag for verification - did the person actually receive the info?
                self.add_verification_requirement(
                    {
                        "person": entry.person,
                        "event": entry.event,
                        "channel": entry.channel_used,
                        "issue": f"Channel {entry.channel_used} controlled by {channel.actual_controller}, not {channel.nominal_owner}",
                        "verification_needed": "Confirm if person actually received information or only filtered version",
                    }
                )

    def log_assumption(self, assumption: Dict):
        """Log an assumption that may need updating based on new evidence"""
        assumption["logged_at"] = datetime.now().isoformat()
        self.assumptions_log.append(assumption)

    def add_verification_requirement(self, requirement: Dict):
        """Add something that needs verification"""
        requirement["added_at"] = datetime.now().isoformat()
        requirement["status"] = "pending"
        self.verification_requirements.append(requirement)

    def analyze_ocr_implications(self, ocr_findings: Dict) -> List[Dict]:
        """Analyze OCR findings for knowledge matrix implications"""
        implications = []

        # Check for email address control revelations
        if "email_control" in ocr_findings:
            for address, controller_info in ocr_findings["email_control"].items():
                nominal_owner = controller_info.get("nominal_owner")
                actual_controller = controller_info.get("actual_controller")

                if nominal_owner != actual_controller:
                    implications.append(
                        {
                            "type": "email_hijacking",
                            "address": address,
                            "nominal_owner": nominal_owner,
                            "actual_controller": actual_controller,
                            "impact": "All knowledge attributed to nominal owner may be filtered/controlled",
                            "action_required": "Review all communications to this address and verify actual recipient",
                        }
                    )

                    # Register the channel
                    channel = CommunicationChannel(
                        address=address,
                        channel_type=ChannelType.EMAIL,
                        nominal_owner=nominal_owner,
                        actual_controller=actual_controller,
                        verified_controller=True,  # OCR provides verification
                        access_method="direct_system_access",
                        verification_source="OCR_system_screenshot",
                    )
                    self.register_channel(channel)

        return implications

    def get_person_knowledge_timeline(self, person: str) -> List[KnowledgeEntry]:
        """Get all knowledge entries for a specific person"""
        return [entry for entry in self.knowledge_entries if entry.person == person]

    def get_channel_analysis(self, address: str) -> Dict:
        """Get analysis of who actually receives communications to an address"""
        if address not in self.communication_channels:
            return {"status": "unknown", "warning": "Channel not registered"}

        channel = self.communication_channels[address]
        related_entries = [
            e for e in self.knowledge_entries if e.channel_used == address
        ]

        return {
            "address": address,
            "nominal_owner": channel.nominal_owner,
            "actual_controller": channel.actual_controller,
            "verified_controller": channel.verified_controller,
            "access_method": channel.access_method,
            "total_communications": len(related_entries),
            "knowledge_entries": related_entries,
            "risk_level": (
                "HIGH" if channel.nominal_owner != channel.actual_controller else "LOW"
            ),
        }

    def generate_assumptions_report(self) -> str:
        """Generate report of assumptions that need updating"""
        report = ["# Assumptions Requiring Update Based on OCR Revelations\n"]

        if not self.assumptions_log:
            report.append("No assumptions logged yet.\n")
            return "\n".join(report)

        report.append("## Address Control Discrepancies\n")
        for assumption in self.assumptions_log:
            if assumption["type"] == "address_control_discrepancy":
                report.append(f"### {assumption['address']}")
                report.append(f"- **Nominal Owner**: {assumption['nominal_owner']}")
                report.append(
                    f"- **Actual Controller**: {assumption['actual_controller']}"
                )
                report.append(f"- **Verified**: {assumption['verified']}")
                report.append(f"- **Implications**: {assumption['implications']}\n")

        report.append("## Verification Requirements\n")
        for req in self.verification_requirements:
            if req["status"] == "pending":
                report.append(f"### {req['person']} - {req['event']}")
                report.append(f"- **Channel**: {req['channel']}")
                report.append(f"- **Issue**: {req['issue']}")
                report.append(
                    f"- **Verification Needed**: {req['verification_needed']}\n"
                )

        return "\n".join(report)

    def export_for_hypergraph(self) -> Dict:
        """Export data in format suitable for hypergraph analysis"""
        return {
            "nodes": {
                "persons": list(
                    set([entry.person for entry in self.knowledge_entries])
                ),
                "events": list(set([entry.event for entry in self.knowledge_entries])),
                "channels": list(self.communication_channels.keys()),
                "intermediaries": list(
                    set(
                        [
                            i
                            for entry in self.knowledge_entries
                            for i in entry.intermediaries
                        ]
                    )
                ),
            },
            "edges": {
                "knowledge_flows": [
                    {
                        "from": entry.information_source,
                        "to": entry.person,
                        "event": entry.event,
                        "intermediaries": entry.intermediaries,
                        "channel": entry.channel_used,
                        "knowledge_level": entry.knowledge_level.value,
                    }
                    for entry in self.knowledge_entries
                ],
                "channel_controls": [
                    {
                        "address": addr,
                        "nominal_owner": channel.nominal_owner,
                        "actual_controller": channel.actual_controller,
                        "verified": channel.verified_controller,
                    }
                    for addr, channel in self.communication_channels.items()
                ],
            },
            "metadata": {
                "total_knowledge_entries": len(self.knowledge_entries),
                "total_channels": len(self.communication_channels),
                "pending_verifications": len(
                    [
                        r
                        for r in self.verification_requirements
                        if r["status"] == "pending"
                    ]
                ),
                "generated_at": datetime.now().isoformat(),
            },
        }


def main():
    """Example usage and testing"""
    matrix = KnowledgeMatrix()

    # Example: Register the Pete@regima.com revelation from OCR
    pete_channel = CommunicationChannel(
        address="Pete@regima.com",
        channel_type=ChannelType.EMAIL,
        nominal_owner="Peter Faucitt",
        actual_controller="Rynette Farrar",
        verified_controller=True,
        access_method="system_administrator_access",
        verification_source="OCR_Screenshot_2025-06-20_Sage_Account",
        last_verified=datetime(2025, 6, 20),
    )
    matrix.register_channel(pete_channel)

    # Example knowledge entry that needs verification
    knowledge = KnowledgeEntry(
        person="Peter Faucitt",
        event="June 10 crime report email",
        knowledge_level=KnowledgeLevel.REPORTED,
        information_source="Email via Rynette",
        verification_status="UNCONFIRMED - OCR shows channel controlled by intermediary",
        date=datetime(2025, 6, 10),
        intermediaries=["Rynette Farrar"],
        channel_used="Pete@regima.com",
    )
    matrix.add_knowledge_entry(knowledge)

    # Generate report
    print("=== ASSUMPTIONS REQUIRING UPDATE ===")
    print(matrix.generate_assumptions_report())

    print("\n=== CHANNEL ANALYSIS ===")
    analysis = matrix.get_channel_analysis("Pete@regima.com")
    print(json.dumps(analysis, indent=2, default=str))


if __name__ == "__main__":
    main()
