"""
Improved Case Data Loader for HyperGNN Framework

This version of the data loader includes dynamic document discovery, enhanced entity and event extraction using spaCy, and a configuration-driven approach.
"""

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import spacy
from dateutil.parser import parse as parse_date

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


class InformationStatus(Enum):
    SAVED = "saved"
    VERIFIED = "verified"
    PARTIAL = "partial"
    CIRCUMSTANTIAL = "circumstantial"
    SPECULATIVE = "speculative"
    MISSING = "missing"


@dataclass
class CaseEntity:
    entity_id: str
    name: str
    entity_type: str
    roles: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    evidence_references: List[str] = field(default_factory=list)
    verification_status: InformationStatus = InformationStatus.PARTIAL


@dataclass
class CaseEvent:
    event_id: str
    date: datetime
    description: str
    participants: List[str] = field(default_factory=list)
    evidence_references: List[str] = field(default_factory=list)
    verification_status: InformationStatus = InformationStatus.PARTIAL
    event_type: str = "general"


class ImprovedDocumentLoader:
    def __init__(self, base_directory: str):
        self.base_directory = Path(base_directory)

    def discover_and_load_documents(
        self, doc_extensions: List[str] = [".md", ".txt"]
    ) -> Dict[str, str]:
        loaded_docs = {}
        for extension in doc_extensions:
            for doc_path in self.base_directory.rglob(f"*{extension}"):
                try:
                    with open(doc_path, "r", encoding="utf-8") as f:
                        loaded_docs[str(doc_path)] = f.read()
                except Exception as e:
                    print(f"Error loading {doc_path}: {e}")
        return loaded_docs


class ImprovedEntityExtractor:
    def extract_entities(self, content: str, source_file: str) -> Dict[str, CaseEntity]:
        entities = {}
        doc = nlp(content)
        for ent in doc.ents:
            entity_id = ent.text.lower().replace(" ", "_")
            if entity_id not in entities:
                entities[entity_id] = CaseEntity(
                    entity_id=entity_id,
                    name=ent.text,
                    entity_type=ent.label_,
                    roles=[],
                    evidence_references=[source_file],
                    verification_status=InformationStatus.PARTIAL,
                )
        return entities


class ImprovedEventExtractor:
    def extract_events(self, content: str, source_file: str) -> List[CaseEvent]:
        events = []
        # A more sophisticated event extraction logic would be needed here.
        # This is a placeholder for a more advanced implementation.
        return events


class ImprovedCaseDataLoader:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.doc_loader = ImprovedDocumentLoader(config["base_directory"])
        self.entity_extractor = ImprovedEntityExtractor()
        self.event_extractor = ImprovedEventExtractor()
        self.entities: Dict[str, CaseEntity] = {}
        self.events: List[CaseEvent] = []

    def load_and_process_case(self) -> Dict[str, Any]:
        documents = self.doc_loader.discover_and_load_documents(
            self.config.get("doc_extensions", [".md", ".txt"])
        )
        for doc_path, content in documents.items():
            self.entities.update(
                self.entity_extractor.extract_entities(content, doc_path)
            )
            self.events.extend(self.event_extractor.extract_events(content, doc_path))

        return {
            "total_documents_processed": len(documents),
            "entities_found": len(self.entities),
            "events_found": len(self.events),
        }


if __name__ == "__main__":
    # Example usage with a configuration dictionary
    config = {
        "case_id": "rzonedevops_analysis_improved",
        "base_directory": ".",
        "doc_extensions": [".md", ".txt"],
    }

    data_loader = ImprovedCaseDataLoader(config)
    results = data_loader.load_and_process_case()
    print(json.dumps(results, indent=4))
