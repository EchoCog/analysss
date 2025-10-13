#!/usr/bin/env python3
"""
Document Processing and Integration System for Case 2025_137857
Processes new documents in docs folder and integrates them into case structure
"""

import hashlib
import json
import os
import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class DocumentProcessor:
    """Processes and categorizes documents for case integration"""

    def __init__(self, workspace_path: str = None):
        if workspace_path is None:
            # Auto-detect workspace path - use current working directory if it contains docs/
            current_path = Path.cwd()
            if (current_path / "docs").exists():
                workspace_path = str(current_path)
            else:
                workspace_path = "/workspace"  # fallback to original default

        self.workspace_path = Path(workspace_path)
        self.docs_path = self.workspace_path / "docs"
        self.case_path = self.workspace_path / "case_2025_137857"
        self.processed_log_path = self.workspace_path / "processed_documents.json"
        self.processed_docs = self._load_processed_log()

        # Document type mappings
        self.doc_type_mappings = {
            "court_documents": {
                "path": "01_court_documents",
                "patterns": [
                    r"court.*order",
                    r"notice.*withdrawal",
                    r"settlement.*agreement",
                    r"interdict",
                    r"formal.*notice",
                    r"J.*and.*D.*Faucitt",
                ],
                "extensions": [".pdf", ".docx", ".md"],
            },
            "evidence": {
                "path": "02_evidence",
                "subfolders": {
                    "emails": [".eml", ".msg"],
                    "pdfs": [".pdf"],
                    "screenshots": [".jpg", ".png"],
                },
                "patterns": [r"CCE\d+", r"screenshot", r"Re:.*", r"Fw:.*", r"eviden"],
            },
            "financial_records": {
                "path": "02_evidence/financial",
                "patterns": [
                    r"INV\d+",
                    r"expense",
                    r"sales.*report",
                    r"shopify",
                    r"sage.*account",
                    r"regima.*group",
                ],
                "extensions": [".pdf", ".xlsx", ".jpg"],
            },
            "medical_records": {
                "path": "05_medical_records",
                "patterns": [r"MED-", r"medical", r"coercive"],
                "extensions": [".md", ".pdf"],
            },
            "analysis": {
                "path": "03_analysis",
                "subfolders": {
                    "ocr_analysis": [r"ocr-", r"comprehensive-ocr"],
                    "party_analysis": [r"party-knowledge"],
                    "timeline_analysis": [r"timeline", r"APR-SEP"],
                },
            },
            "case_notes": {
                "path": "08_case_notes",
                "patterns": [r"current-state-summary", r"draft-response"],
                "extensions": [".md"],
            },
        }

    def _load_processed_log(self) -> Dict[str, Any]:
        """Load the log of previously processed documents"""
        if self.processed_log_path.exists():
            with open(self.processed_log_path, "r") as f:
                return json.load(f)
        return {"processed": {}, "metadata": {}}

    def _save_processed_log(self):
        """Save the processed documents log"""
        with open(self.processed_log_path, "w") as f:
            json.dump(self.processed_docs, f, indent=2)

    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _categorize_document(self, file_path: Path) -> Tuple[str, str]:
        """Categorize a document based on filename and extension"""
        filename = file_path.name.lower()
        extension = file_path.suffix.lower()

        # Check each document type
        for doc_type, config in self.doc_type_mappings.items():
            # Check patterns
            if "patterns" in config:
                for pattern in config["patterns"]:
                    if re.search(pattern, filename, re.IGNORECASE):
                        # Determine subfolder if needed
                        if "subfolders" in config:
                            for subfolder, criteria in config["subfolders"].items():
                                if extension in criteria or any(
                                    re.search(p, filename, re.IGNORECASE)
                                    for p in criteria
                                    if isinstance(p, str)
                                ):
                                    return doc_type, f"{config['path']}/{subfolder}"
                        return doc_type, config["path"]

            # Check extensions
            if "extensions" in config and extension in config["extensions"]:
                return doc_type, config["path"]

        # Default to evidence/misc
        return "evidence", "02_evidence/misc"

    def _extract_entities_from_filename(self, filename: str) -> Dict[str, List[str]]:
        """Extract entities from filename"""
        entities = {
            "persons": [],
            "organizations": [],
            "dates": [],
            "case_numbers": [],
            "document_types": [],
        }

        # Extract persons
        person_patterns = [
            r"Peter\s*Faucitt",
            r"Jacqui\s*Faucitt",
            r"J\s*and\s*D\s*Faucitt",
        ]
        for pattern in person_patterns:
            if re.search(pattern, filename, re.IGNORECASE):
                entities["persons"].append(
                    re.search(pattern, filename, re.IGNORECASE).group()
                )

        # Extract organizations
        org_patterns = [
            r"RegimA(?:\s+(?:SA|WW|Group|Worldwide))?",
            r"De\s*Novo\s*Business\s*Services",
            r"Shopify\s*Plus",
        ]
        for pattern in org_patterns:
            if re.search(pattern, filename, re.IGNORECASE):
                entities["organizations"].append(
                    re.search(pattern, filename, re.IGNORECASE).group()
                )

        # Extract dates
        date_patterns = [
            r"\d{6,8}",  # CCE20250901 format
            r"\d{4}-\d{2}-\d{2}",  # ISO date
            r"\d{2}[-/]\d{2}[-/]\d{2,4}",  # Various date formats
            r"(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[A-Z]*[-\s]*\d{4}",
        ]
        for pattern in date_patterns:
            matches = re.findall(pattern, filename, re.IGNORECASE)
            entities["dates"].extend(matches)

        # Extract case numbers
        case_patterns = [r"2025[_-]137857", r"0558631", r"INV\d+", r"CCE\d+"]
        for pattern in case_patterns:
            matches = re.findall(pattern, filename, re.IGNORECASE)
            entities["case_numbers"].extend(matches)

        # Extract document types
        doc_type_patterns = [
            r"notice",
            r"settlement",
            r"agreement",
            r"court\s*order",
            r"formal\s*notice",
            r"withdrawal",
            r"interdict",
        ]
        for pattern in doc_type_patterns:
            if re.search(pattern, filename, re.IGNORECASE):
                entities["document_types"].append(
                    re.search(pattern, filename, re.IGNORECASE).group()
                )

        return entities

    def _extract_timeline_events(self, file_path: Path) -> List[Dict[str, Any]]:
        """Extract timeline events from document metadata and filename"""
        events = []
        filename = file_path.name

        # Extract dates from filename
        date_patterns = [
            (r"(\d{4})(\d{2})(\d{2})", "%Y%m%d"),  # CCE20250901
            (r"(\d{2})(\d{2})(\d{2})", "%y%m%d"),  # 250924
            (r"(\d{4})-(\d{2})-(\d{2})", "%Y-%m-%d"),  # 2025-07-28
            (r"(\d{2})/(\d{2})/(\d{4})", "%d/%m/%Y"),  # 25/09/2025
        ]

        for pattern, date_format in date_patterns:
            matches = re.findall(pattern, filename)
            for match in matches:
                try:
                    if len(match) == 3:
                        if date_format == "%Y%m%d":
                            date_str = f"{match[0]}-{match[1]}-{match[2]}"
                        elif date_format == "%y%m%d":
                            year = (
                                f"20{match[0]}"
                                if int(match[0]) < 50
                                else f"19{match[0]}"
                            )
                            date_str = f"{year}-{match[1]}-{match[2]}"
                        else:
                            date_str = "-".join(match)

                        events.append(
                            {
                                "date": date_str,
                                "type": "document_created",
                                "document": filename,
                                "description": f"Document '{filename}' dated {date_str}",
                            }
                        )
                except:
                    continue

        # Special handling for specific document types
        if "notice of withdrawal" in filename.lower():
            events.append(
                {
                    "type": "legal_event",
                    "category": "attorney_withdrawal",
                    "document": filename,
                    "description": "Notice of withdrawal as attorneys of record",
                }
            )

        if "settlement agreement" in filename.lower():
            events.append(
                {
                    "type": "legal_event",
                    "category": "settlement",
                    "document": filename,
                    "description": "Settlement agreement signed",
                }
            )

        return events

    def process_new_documents(self) -> Dict[str, Any]:
        """Process all new documents in the docs folder"""
        results = {
            "processed": [],
            "skipped": [],
            "errors": [],
            "entities": defaultdict(list),
            "timeline_events": [],
            "summary": {},
        }

        # Get all files in docs folder (including subdirectories)
        doc_files = []
        for item in self.docs_path.rglob("*"):
            if (
                item.is_file()
                and not item.name.startswith(".")
                and item.suffix.lower() not in [".backup"]
            ):
                # Skip backup files and README files in subdirectories
                if item.parent != self.docs_path and item.name == "README.md":
                    continue
                doc_files.append(item)

        print(f"Found {len(doc_files)} documents in docs folder")

        for doc_file in doc_files:
            try:
                # Check if already processed
                file_hash = self._get_file_hash(doc_file)
                file_key = str(doc_file.relative_to(self.docs_path))
                if file_key in self.processed_docs.get("processed", {}):
                    if (
                        self.processed_docs["processed"][file_key].get("hash")
                        == file_hash
                    ):
                        results["skipped"].append(file_key)
                        continue

                # Categorize document
                doc_type, dest_folder = self._categorize_document(doc_file)

                # Extract entities
                entities = self._extract_entities_from_filename(doc_file.name)
                for entity_type, values in entities.items():
                    results["entities"][entity_type].extend(values)

                # Extract timeline events
                events = self._extract_timeline_events(doc_file)
                results["timeline_events"].extend(events)

                # Create destination path
                dest_path = self.case_path / dest_folder
                dest_path.mkdir(parents=True, exist_ok=True)

                # Copy file to destination
                dest_file = dest_path / doc_file.name
                shutil.copy2(doc_file, dest_file)

                # Log processed document
                process_info = {
                    "hash": file_hash,
                    "processed_date": datetime.now().isoformat(),
                    "category": doc_type,
                    "destination": str(dest_folder),
                    "entities": entities,
                    "events": events,
                }

                self.processed_docs["processed"][file_key] = process_info
                results["processed"].append(
                    {
                        "file": file_key,
                        "category": doc_type,
                        "destination": str(dest_folder),
                    }
                )

                print(f"Processed: {doc_file.name} -> {dest_folder}")

            except Exception as e:
                results["errors"].append({"file": doc_file.name, "error": str(e)})
                print(f"Error processing {doc_file.name}: {e}")

        # Save processed log
        self._save_processed_log()

        # Deduplicate entities
        for entity_type in results["entities"]:
            results["entities"][entity_type] = list(
                set(results["entities"][entity_type])
            )

        # Create summary
        results["summary"] = {
            "total_documents": len(doc_files),
            "processed": len(results["processed"]),
            "skipped": len(results["skipped"]),
            "errors": len(results["errors"]),
            "entities_extracted": {k: len(v) for k, v in results["entities"].items()},
            "timeline_events": len(results["timeline_events"]),
        }

        return results

    def update_case_hypergraph(self, results: Dict[str, Any]):
        """Update the case hypergraph with new entities and relations"""
        hypergraph_path = self.workspace_path / "case_hypergraph.json"

        # Load existing hypergraph
        if hypergraph_path.exists():
            with open(hypergraph_path, "r") as f:
                hypergraph = json.load(f)
                # Ensure required keys exist
                if "nodes" not in hypergraph:
                    hypergraph["nodes"] = {}
                if "edges" not in hypergraph:
                    hypergraph["edges"] = {}
                if "metadata" not in hypergraph:
                    hypergraph["metadata"] = {}
        else:
            hypergraph = {"nodes": {}, "edges": {}, "metadata": {}}

        # Add new entities as nodes
        for entity_type, entities in results["entities"].items():
            for entity in entities:
                node_id = f"{entity_type}_{entity.lower().replace(' ', '_')}"
                if node_id not in hypergraph["nodes"]:
                    hypergraph["nodes"][node_id] = {
                        "type": entity_type,
                        "name": entity,
                        "properties": {
                            "first_seen": datetime.now().isoformat(),
                            "documents": [],
                        },
                    }

                # Add document references
                for doc_info in results["processed"]:
                    if entity in str(doc_info):
                        hypergraph["nodes"][node_id]["properties"]["documents"].append(
                            doc_info["file"]
                        )

        # Create edges for document-entity relations
        for doc_info in results["processed"]:
            doc_id = f"document_{doc_info['file'].lower().replace(' ', '_')}"

            # Add document as node if not exists
            if doc_id not in hypergraph["nodes"]:
                hypergraph["nodes"][doc_id] = {
                    "type": "document",
                    "name": doc_info["file"],
                    "properties": {
                        "category": doc_info["category"],
                        "location": doc_info["destination"],
                        "processed_date": datetime.now().isoformat(),
                    },
                }

            # Create edges to entities
            edge_id = f"edge_{len(hypergraph['edges'])}"
            connected_nodes = [doc_id]

            # Find all entities connected to this document
            for entity_type, entities in results["entities"].items():
                for entity in entities:
                    if entity.lower() in doc_info["file"].lower():
                        node_id = f"{entity_type}_{entity.lower().replace(' ', '_')}"
                        if node_id in hypergraph["nodes"]:
                            connected_nodes.append(node_id)

            if len(connected_nodes) > 1:
                hypergraph["edges"][edge_id] = {
                    "type": "document_contains",
                    "nodes": connected_nodes,
                    "properties": {"created": datetime.now().isoformat()},
                }

        # Update metadata
        hypergraph["metadata"]["last_updated"] = datetime.now().isoformat()
        hypergraph["metadata"]["total_nodes"] = len(hypergraph["nodes"])
        hypergraph["metadata"]["total_edges"] = len(hypergraph["edges"])

        # Save updated hypergraph
        with open(hypergraph_path, "w") as f:
            json.dump(hypergraph, f, indent=2)

        return hypergraph

    def generate_integration_report(self, results: Dict[str, Any]) -> str:
        """Generate a comprehensive integration report"""
        report_path = self.workspace_path / "document_integration_report.md"

        report = f"""# Document Integration Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- **Total Documents Processed**: {results['summary']['processed']}
- **Documents Skipped** (already processed): {results['summary']['skipped']}
- **Processing Errors**: {results['summary']['errors']}

## Document Categories
"""

        # Group processed documents by category
        by_category = defaultdict(list)
        for doc in results["processed"]:
            by_category[doc["category"]].append(doc)

        for category, docs in by_category.items():
            report += f"\n### {category.replace('_', ' ').title()}\n"
            for doc in docs:
                report += f"- **{doc['file']}** → `{doc['destination']}`\n"

        # Add entities section
        report += "\n## Extracted Entities\n"
        for entity_type, entities in results["entities"].items():
            if entities:
                report += f"\n### {entity_type.title()}\n"
                for entity in sorted(set(entities)):
                    report += f"- {entity}\n"

        # Add timeline events
        if results["timeline_events"]:
            report += "\n## Timeline Events\n"
            for event in sorted(
                results["timeline_events"], key=lambda x: x.get("date", "")
            ):
                report += f"\n### {event.get('date', 'Undated')}\n"
                report += f"- **Type**: {event.get('type', 'Unknown')}\n"
                report += f"- **Document**: {event.get('document', 'N/A')}\n"
                report += f"- **Description**: {event.get('description', 'N/A')}\n"

        # Add errors if any
        if results["errors"]:
            report += "\n## Processing Errors\n"
            for error in results["errors"]:
                report += f"- **{error['file']}**: {error['error']}\n"

        # Add recommendations
        report += """
## Recommendations

1. **Review Court Documents**: New court documents have been filed in `01_court_documents/`
2. **Update Timeline**: New timeline events have been extracted and should be integrated
3. **Entity Analysis**: Review extracted entities for accuracy and completeness
4. **Evidence Chain**: Verify the evidence chain for new documents in `02_evidence/`

## Next Steps

1. Run comprehensive case analysis to update all case relationships
2. Review and validate extracted entities
3. Update case timeline with new events
4. Generate updated case summary report
"""

        with open(report_path, "w") as f:
            f.write(report)

        return str(report_path)


def main():
    """Main execution function"""
    processor = DocumentProcessor()

    print("Starting document processing...")

    # Process new documents
    results = processor.process_new_documents()

    print(f"\nProcessing complete!")
    print(f"- Processed: {len(results['processed'])} documents")
    print(f"- Skipped: {len(results['skipped'])} documents")
    print(f"- Errors: {len(results['errors'])} documents")

    # Update case hypergraph
    print("\nUpdating case hypergraph...")
    processor.update_case_hypergraph(results)

    # Generate report
    print("\nGenerating integration report...")
    report_path = processor.generate_integration_report(results)
    print(f"Report saved to: {report_path}")

    # Save results
    results_path = processor.workspace_path / "document_processing_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Detailed results saved to: {results_path}")


if __name__ == "__main__":
    main()
