#!/usr/bin/env python3
"""
HyperGNN Case Integration Script
==============================

Integrates extracted case data with the HyperGNN framework, creating agents,
events, and evidence items with proper verification status tracking.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from hypergnn_framework_improved import (
    AnalysisConfiguration,
    AnalysisScope,
    ComplexityLevel,
)

from case_data_loader import CaseDataLoader, InformationStatus
from frameworks.evidence_management import (
    ClassificationLevel,
    EvidenceItem,
    EvidenceType,
    VerificationStatus,
)
from frameworks.hypergnn_core import HyperGNNFramework


class HyperGNNCaseIntegrator:
    """Integrates case data with HyperGNN framework"""

    def __init__(self, case_id: str):
        self.case_id = case_id

        # Initialize HyperGNN framework
        config = AnalysisConfiguration(
            case_id=case_id,
            scope=AnalysisScope.COMPREHENSIVE,
        )

        self.framework = HyperGNNFramework(config)
        self.integration_stats = {
            "agents_added": 0,
            "events_added": 0,
            "evidence_items_added": 0,
            "relationships_added": 0,
            "verification_statuses": {},
        }

    def integrate_case_data(
        self, case_data_file: str = "/tmp/case_data_extracted.json"
    ) -> Dict[str, Any]:
        """Integrate extracted case data into HyperGNN framework"""
        print("=== HYPERGNN CASE INTEGRATION ===")

        # Load extracted case data
        with open(case_data_file, "r") as f:
            case_data = json.load(f)

        print(f"Loading case data for: {case_data['case_id']}")
        print(f"Entities: {len(case_data['entities'])}")
        print(f"Events: {len(case_data['events'])}")
        print(f"Evidence items: {len(case_data['evidence_items'])}")

        # Filter and integrate key entities (people and organizations)
        self._integrate_key_entities(case_data["entities"])

        # Integrate events with verification status
        self._integrate_events(case_data["events"])

        # Integrate evidence items
        self._integrate_evidence_items(case_data["evidence_items"])

        # Process OCR revelations specially
        self._integrate_ocr_revelations(case_data)

        # Generate comprehensive analysis
        analysis = self.framework.export_comprehensive_analysis()

        return {
            "integration_stats": self.integration_stats,
            "hypergnn_analysis": analysis,
            "case_summary": self._generate_case_summary(case_data),
        }

    def _integrate_key_entities(self, entities: Dict[str, Any]):
        """Integrate key entities (filter out false positives)"""
        print("\n=== INTEGRATING KEY ENTITIES ===")

        # Known key entities from the case
        key_people = [
            "peter_andrew_faucitt",
            "peter_faucitt",
            "daniel_james_faucitt",
            "daniel_faucitt",
            "rynette_farrar",
            "kayla_pretorius",
        ]

        key_organizations = ["regima_group", "regima_worldwide", "sage_account"]

        for entity_data in entities:
            entity_id = entity_data["entity_id"]
            # Filter for actual people and organizations
            if entity_data["entity_type"] == "person" and any(
                key in entity_id.lower() for key in key_people
            ):

                success = self.framework.add_agent(
                    agent_id=entity_id,
                    name=entity_data["name"],
                    agent_type="individual",
                    attributes={
                        "roles": entity_data["roles"],
                        "verification_status": entity_data["verification_status"],
                        "evidence_references": entity_data["evidence_references"],
                    },
                )

                if success:
                    self.integration_stats["agents_added"] += 1
                    self._track_verification_status(entity_data["verification_status"])
                    print(
                        f"✅ Added agent: {entity_data['name']} ({entity_data['verification_status']})"
                    )

            elif entity_data["entity_type"] == "organization" and any(
                key in entity_id.lower() for key in key_organizations
            ):

                success = self.framework.add_agent(
                    agent_id=entity_id,
                    name=entity_data["name"],
                    agent_type="organization",
                    attributes={
                        "roles": entity_data["roles"],
                        "verification_status": entity_data["verification_status"],
                        "evidence_references": entity_data["evidence_references"],
                    },
                )

                if success:
                    self.integration_stats["agents_added"] += 1
                    self._track_verification_status(entity_data["verification_status"])
                    print(
                        f"✅ Added organization: {entity_data['name']} ({entity_data['verification_status']})"
                    )

            elif entity_data["entity_type"] == "email_address":
                # Add email addresses as communication channels
                success = self.framework.add_agent(
                    agent_id=entity_id,
                    name=entity_data["name"],
                    agent_type="system",
                    attributes={
                        "type": "communication_channel",
                        "verification_status": entity_data["verification_status"],
                        "evidence_references": entity_data["evidence_references"],
                    },
                )

                if success:
                    self.integration_stats["agents_added"] += 1
                    self._track_verification_status(entity_data["verification_status"])
                    print(
                        f"✅ Added email channel: {entity_data['name']} ({entity_data['verification_status']})"
                    )

    def _integrate_events(self, events: List[Dict[str, Any]]):
        """Integrate timeline events with verification status"""
        print(f"\n=== INTEGRATING {len(events)} EVENTS ===")

        for event_data in events:
            try:
                # Parse date
                event_date = (
                    datetime.fromisoformat(event_data["date"])
                    if event_data["date"]
                    else datetime.now()
                )

                # Add event to framework components
                if "dynamics" in self.framework.components:
                    # Add as system flow if financial or material
                    if event_data["event_type"] in [
                        "financial_crime",
                        "criminal_homicide",
                    ]:
                        flow_type = (
                            "financial"
                            if "financial" in event_data["event_type"]
                            else "deception"
                        )

                        # Extract source and target from participants
                        source = (
                            event_data["participants"][0]
                            if event_data["participants"]
                            else "unknown"
                        )
                        target = (
                            event_data["participants"][1]
                            if len(event_data["participants"]) > 1
                            else "system"
                        )

                        from frameworks.system_dynamics import Flow, FlowType

                        # Map string to FlowType
                        flow_type_mapping = {
                            "financial": FlowType.FINANCIAL_EXCHANGE,
                            "deception": FlowType.DECEPTION_DEPLOYMENT,
                        }

                        flow = Flow(
                            flow_id=event_data["event_id"],
                            flow_type=flow_type_mapping.get(
                                flow_type, FlowType.INFORMATION_TRANSFER
                            ),
                            source_stock=source,
                            target_stock=target,
                            rate=1.0,
                            timestamp=event_date,
                            description=event_data["description"],
                            evidence_refs=event_data["evidence_references"],
                        )

                        self.framework.components["dynamics"].add_flow(flow)

                if "verification" in self.framework.components:
                    # Add to verification tracker
                    try:
                        # Create communication event if applicable
                        if event_data["event_type"] == "communication":
                            self.framework.components[
                                "verification"
                            ].add_communication_event(
                                event_id=event_data["event_id"],
                                date=event_date,
                                description=event_data["description"],
                                participants=event_data["participants"],
                                verification_status=event_data["verification_status"],
                            )
                    except:
                        pass  # Skip if method doesn't exist

                self.integration_stats["events_added"] += 1
                self._track_verification_status(event_data["verification_status"])

                if event_data["event_type"] in [
                    "criminal_homicide",
                    "financial_crime",
                    "legal_proceeding",
                ]:
                    print(
                        f"✅ Added {event_data['event_type']}: {event_data['description'][:50]}... ({event_data['verification_status']})"
                    )

            except Exception as e:
                print(f"⚠️  Error processing event {event_data['event_id']}: {str(e)}")

    def _integrate_evidence_items(self, evidence_items: List[Dict[str, Any]]):
        """Integrate evidence items into evidence management system"""
        print(f"\n=== INTEGRATING {len(evidence_items)} EVIDENCE ITEMS ===")

        if "evidence" not in self.framework.components:
            print("⚠️  Evidence management system not available")
            return

        evidence_system = self.framework.components["evidence"]

        for evidence_data in evidence_items:
            try:
                evidence_item = EvidenceItem(
                    evidence_id=evidence_data["evidence_id"],
                    title=evidence_data["title"],
                    evidence_type=EvidenceType(evidence_data["evidence_type"]),
                    classification=ClassificationLevel(
                        evidence_data["classification_level"]
                    ),
                    verification_status=VerificationStatus(
                        evidence_data["verification_status"]
                    ),
                    description=evidence_data["description"],
                    source=evidence_data["source_file"],
                    collection_date=datetime.fromisoformat(
                        evidence_data["creation_date"]
                    ),
                    metadata={
                        "keywords": evidence_data["keywords"],
                        "content_length": evidence_data["content_length"],
                    },
                    chain_of_custody=[],
                )

                # Add to evidence system
                evidence_id = evidence_system.add_evidence_item(evidence_item)
                self.integration_stats["evidence_items_added"] += 1
                self._track_verification_status(
                    evidence_data["verification_status"].value
                )

                print(
                    f"✅ Added evidence: {evidence_data['title']} ({evidence_data['verification_status'].value})"
                )

            except Exception as e:
                print(
                    f"⚠️  Error processing evidence {evidence_data['evidence_id']}: {str(e)}"
                )

    def _integrate_ocr_revelations(self, case_data: Dict[str, Any]):
        """Special integration for OCR revelations about email control"""
        print("\n=== INTEGRATING OCR REVELATIONS ===")

        # Key OCR revelation: Pete@regima.com is controlled by Rynette Farrar
        ocr_revelations = [
            {
                "finding": "Pete@regima.com controlled by Rynette Farrar, not Peter Faucitt",
                "evidence_type": "technical",
                "verification_status": "verified",
                "impact": "All email communications to Pete@regima.com go to Rynette Farrar",
                "legal_implications": [
                    "Identity theft",
                    "Information warfare",
                    "Perjury potential",
                ],
            },
            {
                "finding": "Email CC fields can be completely deceptive about actual recipients",
                "evidence_type": "technical",
                "verification_status": "verified",
                "impact": "Cannot trust email CC fields for information flow analysis",
                "legal_implications": [
                    "Fraud charges",
                    "Evidence tampering",
                    "Conspiracy charges",
                ],
            },
        ]

        for i, revelation in enumerate(ocr_revelations):
            try:
                # Add as high-priority evidence
                evidence_item = EvidenceItem(
                    evidence_id=f"ocr_revelation_{i+1}",
                    title=f"OCR Revelation {i+1}: {revelation['finding'][:50]}",
                    evidence_type=EvidenceType.TECHNICAL,
                    classification=ClassificationLevel.CONFIDENTIAL,
                    verification_status=VerificationStatus.VERIFIED,
                    description=revelation["finding"],
                    source="OCR Analysis Screenshots",
                    collection_date=datetime.now(),
                    metadata={
                        "keywords": ["ocr", "email", "control", "deception"],
                        "legal_implications": revelation["legal_implications"],
                    },
                    chain_of_custody=[],
                )

                if "evidence" in self.framework.components:
                    evidence_id = self.framework.components[
                        "evidence"
                    ].add_evidence_item(evidence_item)
                    print(f"✅ Added OCR revelation: {revelation['finding'][:50]}...")

                # Add to knowledge matrix if available
                if "knowledge" in self.framework.components:
                    try:
                        self.framework.components["knowledge"].log_assumption(
                            {
                                "type": "ocr_revelation",
                                "finding": revelation["finding"],
                                "verification_status": "verified",
                                "impact": revelation["impact"],
                                "legal_implications": revelation["legal_implications"],
                            }
                        )
                    except:
                        pass  # Skip if method doesn't exist

            except Exception as e:
                print(f"⚠️  Error processing OCR revelation: {str(e)}")

    def _track_verification_status(self, status: str):
        """Track verification status statistics"""
        if status not in self.integration_stats["verification_statuses"]:
            self.integration_stats["verification_statuses"][status] = 0
        self.integration_stats["verification_statuses"][status] += 1

    def _generate_case_summary(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive case summary with status indicators"""
        return {
            "case_id": case_data["case_id"],
            "extraction_timestamp": case_data["extraction_timestamp"],
            "integration_timestamp": datetime.now().isoformat(),
            "data_status_summary": case_data["status_summary"],
            "integration_summary": self.integration_stats,
            "key_findings": {
                "pete_email_control": {
                    "finding": "Pete@regima.com controlled by Rynette Farrar",
                    "status": "VERIFIED",
                    "impact": "HIGH",
                    "source": "OCR Screenshots",
                },
                "email_cc_deception": {
                    "finding": "Email CC fields can be completely deceptive",
                    "status": "VERIFIED",
                    "impact": "HIGH",
                    "source": "System Analysis",
                },
                "legal_weaponization": {
                    "finding": "Courts used by perpetrator against victim",
                    "status": "CIRCUMSTANTIAL",
                    "impact": "CRITICAL",
                    "source": "Timeline Analysis",
                },
            },
            "status_indicators": {
                "saved": f"{self.integration_stats['verification_statuses'].get('saved', 0)} items documented with evidence",
                "verified": f"{self.integration_stats['verification_statuses'].get('verified', 0)} items independently confirmed",
                "partial": f"{self.integration_stats['verification_statuses'].get('partial', 0)} items with incomplete information",
                "circumstantial": f"{self.integration_stats['verification_statuses'].get('circumstantial', 0)} items with indirect evidence",
                "speculative": f"{self.integration_stats['verification_statuses'].get('speculative', 0)} unconfirmed theories",
                "missing": f"{self.integration_stats['verification_statuses'].get('missing', 0)} required but unavailable items",
            },
        }

    def generate_professional_report(self) -> str:
        """Generate professional case analysis report"""
        print("\n=== GENERATING PROFESSIONAL REPORT ===")

        # Generate framework report
        framework_report = self.framework.generate_professional_report(
            include_recommendations=True, include_technical_details=True
        )

        # Add case-specific sections
        case_specific_sections = [
            "\n## Case-Specific Analysis",
            "",
            f"**Case ID:** {self.case_id}",
            f"**Integration Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "### Status Indicators Summary",
            "",
        ]

        # Add status breakdown
        for status, count in self.integration_stats["verification_statuses"].items():
            case_specific_sections.append(f"- **{status.upper()}**: {count} items")

        case_specific_sections.extend(
            [
                "",
                "### Key OCR Revelations",
                "",
                "1. **Pete@regima.com Email Control**",
                "   - Status: VERIFIED",
                "   - Finding: Controlled by Rynette Farrar, not Peter Faucitt",
                "   - Impact: All email communications intercepted",
                "",
                "2. **Email CC Field Deception**",
                "   - Status: VERIFIED",
                "   - Finding: CC fields do not indicate actual recipients",
                "   - Impact: Information flow analysis requires verification",
                "",
                "### Recommendations",
                "",
                "1. Verify control of all email addresses mentioned in case",
                "2. Implement address vs actual recipient tracking",
                "3. Add confirmation tracking for all email-based communications",
                "4. Flag potential perjury where direct email receipt is claimed",
            ]
        )

        # Combine reports
        full_report = framework_report + "\n".join(case_specific_sections)

        return full_report

    def save_integration_results(self, output_dir: str = "/tmp") -> Dict[str, str]:
        """Save all integration results to files"""
        output_paths = {}

        # Save case summary
        case_summary = self._generate_case_summary(
            {
                "case_id": self.case_id,
                "extraction_timestamp": datetime.now().isoformat(),
                "status_summary": {"verification_percentage": 0},
            }
        )

        summary_path = Path(output_dir) / f"{self.case_id}_integration_summary.json"
        with open(summary_path, "w") as f:
            json.dump(case_summary, f, indent=2, default=str)
        output_paths["summary"] = str(summary_path)

        # Save professional report
        report = self.generate_professional_report()
        report_path = Path(output_dir) / f"{self.case_id}_analysis_report.md"
        with open(report_path, "w") as f:
            f.write(report)
        output_paths["report"] = str(report_path)

        # Save comprehensive analysis
        analysis = self.framework.export_comprehensive_analysis()
        analysis_path = Path(output_dir) / f"{self.case_id}_hypergnn_analysis.json"
        with open(analysis_path, "w") as f:
            json.dump(analysis, f, indent=2, default=str)
        output_paths["analysis"] = str(analysis_path)

        return output_paths


def main():
    """Main function to test case integration"""
    print("=== HYPERGNN CASE INTEGRATION TEST ===")

    # Load case data first
    loader = CaseDataLoader("case_2025_137857")
    print("Loading case documents...")
    results = loader.load_case_documents()

    # Export case data
    case_data = loader.export_case_data()
    with open("/tmp/case_data_extracted.json", "w") as f:
        json.dump(case_data, f, indent=2, default=str)

    # Integrate with HyperGNN
    integrator = HyperGNNCaseIntegrator("case_2025_137857")
    integration_results = integrator.integrate_case_data()

    print(f"\n=== INTEGRATION RESULTS ===")
    print(f"Agents added: {integration_results['integration_stats']['agents_added']}")
    print(f"Events added: {integration_results['integration_stats']['events_added']}")
    print(
        f"Evidence items added: {integration_results['integration_stats']['evidence_items_added']}"
    )

    print(f"\n=== VERIFICATION STATUS DISTRIBUTION ===")
    for status, count in integration_results["integration_stats"][
        "verification_statuses"
    ].items():
        print(f"{status.upper()}: {count}")

    # Save results
    output_paths = integrator.save_integration_results()

    print(f"\n=== FILES SAVED ===")
    for file_type, path in output_paths.items():
        print(f"{file_type.upper()}: {path}")

    return integration_results


if __name__ == "__main__":
    main()
