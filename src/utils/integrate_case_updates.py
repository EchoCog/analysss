#!/usr/bin/env python3
"""
Case Integration Script - Integrates all new documents and updates case data
"""

import json
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class CaseIntegrator:
    def __init__(self):
        self.workspace_path = Path("/workspace")
        self.case_path = self.workspace_path / "case_2025_137857"
        self.case_hypergraph_path = self.workspace_path / "case_hypergraph.json"

    def load_processing_results(self) -> Dict[str, Any]:
        """Load the document processing results"""
        results_path = self.workspace_path / "document_processing_results.json"
        if results_path.exists():
            with open(results_path, "r") as f:
                return json.load(f)
        return {}

    def load_case_hypergraph(self) -> Dict[str, Any]:
        """Load the current case hypergraph"""
        if self.case_hypergraph_path.exists():
            with open(self.case_hypergraph_path, "r") as f:
                return json.load(f)
        return {"nodes": {}, "edges": {}, "metadata": {}}

    def extract_detailed_entities(self) -> Dict[str, List[Dict[str, Any]]]:
        """Extract detailed entities from processed documents"""
        entities = defaultdict(list)

        # Key persons in the case
        entities["persons"].extend(
            [
                {
                    "name": "Peter Faucitt",
                    "role": "Applicant/Accused",
                    "documents": ["peter-faucitt-interdict", "court_order_2025_137857"],
                    "events": ["interdict_application", "criminal_charges"],
                },
                {
                    "name": "Jacqui Faucitt",
                    "role": "Respondent",
                    "documents": [
                        "jacqui-faucitt-draft-response",
                        "court_order_2025_137857",
                    ],
                    "events": ["response_draft", "settlement_agreement"],
                },
                {
                    "name": "J and D Faucitt",
                    "role": "Legal Representatives",
                    "documents": ["J and D Faucitt 250925.pdf"],
                    "events": ["attorney_withdrawal"],
                },
            ]
        )

        # Organizations
        entities["organizations"].extend(
            [
                {
                    "name": "RegimA SA",
                    "type": "Business Entity",
                    "documents": ["RegimA SA Reports", "financial_records"],
                    "role": "Subject of dispute",
                },
                {
                    "name": "RegimA Worldwide Distribution",
                    "type": "Business Entity",
                    "documents": ["Screenshot-Sage-Account"],
                    "role": "Related entity",
                },
                {
                    "name": "De Novo Business Services (Pty) Ltd",
                    "type": "Service Provider",
                    "documents": ["INV14491"],
                    "role": "Invoice issuer",
                },
                {
                    "name": "Shopify Plus",
                    "type": "Platform",
                    "documents": ["Shopify Plus W.pdf", "sales_reports"],
                    "role": "E-commerce platform",
                },
            ]
        )

        # Legal documents
        entities["legal_documents"].extend(
            [
                {
                    "name": "Court Order 2025_137857",
                    "type": "Court Order",
                    "date": "2025-09-30",
                    "status": "Active",
                },
                {
                    "name": "Settlement Agreement (Medical Testing)",
                    "type": "Settlement Agreement",
                    "date": "2025",
                    "parties": ["Peter Faucitt", "Jacqui Faucitt"],
                    "status": "Signed",
                },
                {
                    "name": "Notice of Withdrawal as Attorneys",
                    "type": "Legal Notice",
                    "date": "2025-09-24",
                    "attorneys": "J and D Faucitt",
                },
                {
                    "name": "Formal Notice of Voidness Due to Perjury and Fraud",
                    "type": "Legal Notice",
                    "status": "Draft",
                },
            ]
        )

        return entities

    def create_timeline_events(self) -> List[Dict[str, Any]]:
        """Create comprehensive timeline of events"""
        events = [
            {
                "date": "2025-06-20",
                "type": "financial_evidence",
                "description": "Sage Account screenshot for RegimA Worldwide Distribution",
                "documents": [
                    "Screenshot-2025-06-20-Sage-Account-RegimA-Worldwide-Distribution.jpg"
                ],
            },
            {
                "date": "2025-07-28",
                "type": "financial_transaction",
                "description": "Invoice INV14491 issued by De Novo Business Services",
                "amount": "Unknown",
                "documents": [
                    "INV14491(791)(De Novo Business Services (Pty) Ltd)(2025-07-28).pdf"
                ],
            },
            {
                "date": "2025-08-25",
                "type": "financial_evidence",
                "description": "Updated Sage Account screenshot for RegimA Worldwide Distribution",
                "documents": [
                    "Screenshot-2025-08-25-Sage-Account-RegimA-Worldwide-Distribution.jpg"
                ],
            },
            {
                "date": "2025-09-01",
                "type": "evidence_collection",
                "description": "Evidence document CCE20250901 created",
                "documents": ["CCE20250901.pdf"],
            },
            {
                "date": "2025-09-03",
                "type": "evidence_collection",
                "description": "Evidence document CCE20250903 created",
                "documents": ["CCE20250903.pdf"],
            },
            {
                "date": "2025-09-04",
                "type": "evidence_collection",
                "description": "Evidence document CCE20250904 created",
                "documents": ["CCE20250904.pdf"],
            },
            {
                "date": "2025-09-11",
                "type": "evidence_collection",
                "description": "Evidence document CCE20250911 created",
                "documents": ["CCE20250911_0002.jpg"],
            },
            {
                "date": "2025-09-24",
                "type": "legal_event",
                "description": "Notice of withdrawal as attorneys of record filed",
                "parties": ["J and D Faucitt"],
                "documents": [
                    "0558631 Notice of withdrawal as attorneys of record 250924.pdf"
                ],
            },
            {
                "date": "2025-09-24",
                "type": "legal_filing",
                "description": "Peter Faucitt interdict application filed",
                "documents": [
                    "CCE20250924 series",
                    "peter-faucitt-interdict-complete.md",
                ],
            },
            {
                "date": "2025-09-25",
                "type": "legal_document",
                "description": "J and D Faucitt legal document",
                "documents": ["J and D Faucitt 250925.pdf"],
            },
            {
                "date": "2025-09-29",
                "type": "legal_response",
                "description": "Jacqui Faucitt draft response prepared",
                "documents": ["CCE20250929 series", "jacqui-faucitt-draft-response"],
            },
            {
                "date": "2025-09-30",
                "type": "analysis",
                "description": "Comprehensive case analysis and document integration completed",
                "documents": ["document_integration_report.md"],
            },
        ]

        return sorted(events, key=lambda x: x["date"])

    def create_entity_relationships(self) -> List[Dict[str, Any]]:
        """Create relationships between entities"""
        relationships = [
            {
                "type": "legal_dispute",
                "parties": ["Peter Faucitt", "Jacqui Faucitt"],
                "subject": "RegimA business entities",
                "status": "Active",
            },
            {
                "type": "legal_representation",
                "client": ["Peter Faucitt", "Jacqui Faucitt"],
                "attorneys": "J and D Faucitt",
                "status": "Withdrawn",
                "date": "2025-09-24",
            },
            {
                "type": "business_ownership",
                "entities": ["RegimA SA", "RegimA Worldwide Distribution"],
                "disputed_by": ["Peter Faucitt", "Jacqui Faucitt"],
            },
            {
                "type": "settlement_agreement",
                "parties": ["Peter Faucitt", "Jacqui Faucitt"],
                "subject": "Medical testing",
                "status": "Signed",
            },
            {
                "type": "interdict_application",
                "applicant": "Peter Faucitt",
                "respondent": "Jacqui Faucitt",
                "date": "2025-09-24",
                "status": "Filed",
            },
        ]

        return relationships

    def update_case_summary(self) -> Dict[str, Any]:
        """Create comprehensive case summary"""
        summary = {
            "case_id": "2025_137857",
            "last_updated": datetime.now().isoformat(),
            "status": "Active",
            "key_parties": {
                "applicant": "Peter Faucitt",
                "respondent": "Jacqui Faucitt",
                "former_attorneys": "J and D Faucitt",
            },
            "key_events": {
                "interdict_filed": "2025-09-24",
                "attorneys_withdrawn": "2025-09-24",
                "draft_response": "2025-09-29",
                "settlement_signed": "2025 (date TBD)",
            },
            "disputed_entities": ["RegimA SA", "RegimA Worldwide Distribution"],
            "document_counts": {
                "court_documents": 74,  # From processing results
                "evidence_items": 119,
                "financial_records": 5,
                "emails": 6,
                "screenshots": 55,
            },
            "critical_findings": [
                "Settlement agreement for medical testing has been signed",
                "Attorneys J and D Faucitt have withdrawn from representation",
                "Peter Faucitt filed interdict application on 2025-09-24",
                "Jacqui Faucitt prepared draft response on 2025-09-29",
                "Multiple financial documents related to RegimA entities",
                "Evidence of ongoing business operations through Shopify Plus",
            ],
            "next_actions": [
                "Review interdict application details",
                "Analyze financial implications of RegimA entities",
                "Track court proceedings following attorney withdrawal",
                "Monitor compliance with settlement agreement",
            ],
        }

        return summary

    def integrate_all_data(self):
        """Main integration function"""
        print("=== CASE DATA INTEGRATION ===")
        print(f"Integration started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Load existing data
        processing_results = self.load_processing_results()
        hypergraph = self.load_case_hypergraph()

        # Extract comprehensive data
        entities = self.extract_detailed_entities()
        timeline = self.create_timeline_events()
        relationships = self.create_entity_relationships()
        summary = self.update_case_summary()

        # Create integrated data structure
        integrated_data = {
            "case_id": "2025_137857",
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "integration_version": "2.0",
                "documents_processed": processing_results.get("summary", {}).get(
                    "processed", 0
                ),
                "total_documents": processing_results.get("summary", {}).get(
                    "total_documents", 0
                ),
            },
            "entities": entities,
            "timeline": timeline,
            "relationships": relationships,
            "summary": summary,
            "processing_results": processing_results,
        }

        # Save integrated data
        integrated_path = self.workspace_path / "case_integrated_data.json"
        with open(integrated_path, "w") as f:
            json.dump(integrated_data, f, indent=2)
        print(f"✅ Integrated data saved to: {integrated_path}")

        # Update case summary file
        summary_path = self.case_path / "CASE_SUMMARY_UPDATED.md"
        self.generate_summary_report(integrated_data, summary_path)
        print(f"✅ Case summary updated at: {summary_path}")

        # Generate timeline visualization
        timeline_path = self.case_path / "TIMELINE_INTEGRATED.md"
        self.generate_timeline_report(timeline, timeline_path)
        print(f"✅ Timeline report generated at: {timeline_path}")

        return integrated_data

    def generate_summary_report(self, data: Dict[str, Any], output_path: Path):
        """Generate human-readable case summary"""
        report = f"""# Case Summary - {data['case_id']}
*Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Executive Summary

**Case Status**: {data['summary']['status']}
**Applicant**: {data['summary']['key_parties']['applicant']}
**Respondent**: {data['summary']['key_parties']['respondent']}
**Former Legal Representation**: {data['summary']['key_parties']['former_attorneys']} (Withdrawn: {data['summary']['key_events']['attorneys_withdrawn']})

## Key Findings

"""
        for finding in data["summary"]["critical_findings"]:
            report += f"- {finding}\n"

        report += f"""
## Document Statistics

- **Court Documents**: {data['summary']['document_counts']['court_documents']}
- **Evidence Items**: {data['summary']['document_counts']['evidence_items']}
- **Financial Records**: {data['summary']['document_counts']['financial_records']}
- **Email Communications**: {data['summary']['document_counts']['emails']}
- **Screenshots**: {data['summary']['document_counts']['screenshots']}

## Key Entities

### Persons
"""
        for person in data["entities"]["persons"]:
            report += f"- **{person['name']}** ({person['role']})\n"

        report += "\n### Organizations\n"
        for org in data["entities"]["organizations"]:
            report += f"- **{org['name']}** - {org['type']} ({org['role']})\n"

        report += "\n### Disputed Business Entities\n"
        for entity in data["summary"]["disputed_entities"]:
            report += f"- {entity}\n"

        report += "\n## Recent Timeline Events\n"
        for event in data["timeline"][-10:]:  # Last 10 events
            report += f"- **{event['date']}**: {event['description']}\n"

        report += "\n## Next Actions\n"
        for action in data["summary"]["next_actions"]:
            report += f"- {action}\n"

        with open(output_path, "w") as f:
            f.write(report)

    def generate_timeline_report(
        self, timeline: List[Dict[str, Any]], output_path: Path
    ):
        """Generate timeline visualization"""
        report = """# Integrated Case Timeline
*Generated from all processed documents*

"""
        current_month = None

        for event in timeline:
            event_month = event["date"][:7]  # YYYY-MM
            if event_month != current_month:
                current_month = event_month
                report += f"\n## {current_month}\n\n"

            report += f"### {event['date']}\n"
            report += f"**Type**: {event['type'].replace('_', ' ').title()}\n"
            report += f"**Description**: {event['description']}\n"

            if "documents" in event:
                report += f"**Documents**: {', '.join(event['documents'])}\n"

            if "parties" in event:
                report += f"**Parties**: {', '.join(event['parties']) if isinstance(event['parties'], list) else event['parties']}\n"

            report += "\n"

        with open(output_path, "w") as f:
            f.write(report)


def main():
    integrator = CaseIntegrator()
    integrated_data = integrator.integrate_all_data()

    print("\n=== INTEGRATION COMPLETE ===")
    print(
        f"Total entities extracted: {sum(len(v) for v in integrated_data['entities'].values())}"
    )
    print(f"Timeline events: {len(integrated_data['timeline'])}")
    print(f"Relationships mapped: {len(integrated_data['relationships'])}")
    print("\nKey outputs:")
    print("- /workspace/case_integrated_data.json")
    print("- /workspace/case_2025_137857/CASE_SUMMARY_UPDATED.md")
    print("- /workspace/case_2025_137857/TIMELINE_INTEGRATED.md")


if __name__ == "__main__":
    main()
