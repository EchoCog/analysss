"""
Evidence Analyzers

Analysis classes for extracting structured information from evidence content,
including entities, timeline events, and legal violations.
"""

import json
import re
from datetime import datetime
from typing import Any, Dict, List, Optional


class BaseAnalyzer:
    """Base class for content analyzers."""

    def analyze(self, content: str) -> List[Dict[str, Any]]:
        """Analyze content and return structured results."""
        raise NotImplementedError("Subclasses must implement analyze method")


class EntityAnalyzer(BaseAnalyzer):
    """Analyzer for extracting entities from evidence content."""

    def __init__(self):
        # Define entity patterns
        self.entity_patterns = {
            "person": [
                r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b",  # First Last name
                r"\b([A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+)\b",  # First M. Last
            ],
            "email": [r"\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b"],
            "company": [
                r"\b([A-Z][a-zA-Z\s&]+(?:Pty|Ltd|CC|Inc|Corp|Company|Group)\.?)\b",
                r"\b([A-Z][a-zA-Z\s&]+ (?:Pty|Ltd|CC|Inc|Corp|Company|Group))\b",
            ],
            "phone": [
                r"\b(\+?27\s?\d{2}\s?\d{3}\s?\d{4})\b",  # South African format
                r"\b(\d{3}\s?\d{3}\s?\d{4})\b",  # General format
            ],
            "amount": [
                r"\bR\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\b",  # South African Rand
                r"\b(\d{1,3}(?:,\d{3})*(?:\.\d{2})?) rand\b",
            ],
            "legal_reference": [
                r"\b(Section \d+[a-z]?)\b",
                r"\b([A-Z][a-zA-Z\s]+ Act)\b",
                r"\b(Case \d+[/_]\d+)\b",
            ],
        }

    def extract_entities(self, content: str) -> List[Dict[str, Any]]:
        """Extract entities from content."""
        entities = []

        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    entity = {
                        "type": entity_type,
                        "name": match.group(1) if match.groups() else match.group(0),
                        "context": self._get_context(
                            content, match.start(), match.end()
                        ),
                        "position": {"start": match.start(), "end": match.end()},
                    }

                    # Add specific processing for different entity types
                    if entity_type == "person":
                        entity["description"] = self._analyze_person_context(
                            entity["context"]
                        )
                    elif entity_type == "company":
                        entity["description"] = self._analyze_company_context(
                            entity["context"]
                        )
                    elif entity_type == "email":
                        entity["description"] = f"Email address: {entity['name']}"
                    elif entity_type == "amount":
                        entity["description"] = f"Financial amount: R{entity['name']}"
                    elif entity_type == "legal_reference":
                        entity["description"] = f"Legal reference: {entity['name']}"
                    else:
                        entity["description"] = (
                            f"{entity_type.title()}: {entity['name']}"
                        )

                    entities.append(entity)

        # Remove duplicates and sort by position
        entities = self._deduplicate_entities(entities)
        entities.sort(key=lambda x: x["position"]["start"])

        return entities

    def _get_context(
        self, content: str, start: int, end: int, window: int = 100
    ) -> str:
        """Get context around an entity match."""
        context_start = max(0, start - window)
        context_end = min(len(content), end + window)
        return content[context_start:context_end].strip()

    def _analyze_person_context(self, context: str) -> str:
        """Analyze context to determine person's role."""
        context_lower = context.lower()

        if "director" in context_lower:
            return "Director"
        elif "attorney" in context_lower or "lawyer" in context_lower:
            return "Legal counsel"
        elif "manager" in context_lower:
            return "Manager"
        elif "employee" in context_lower:
            return "Employee"
        elif "@" in context:
            return "Contact person"
        else:
            return "Individual"

    def _analyze_company_context(self, context: str) -> str:
        """Analyze context to determine company's role."""
        context_lower = context.lower()

        if "client" in context_lower or "customer" in context_lower:
            return "Client company"
        elif "service provider" in context_lower or "provider" in context_lower:
            return "Service provider"
        elif "subsidiary" in context_lower or "related" in context_lower:
            return "Related entity"
        elif "regulatory" in context_lower or "authority" in context_lower:
            return "Regulatory body"
        else:
            return "Corporate entity"

    def _deduplicate_entities(
        self, entities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Remove duplicate entities based on name and type."""
        seen = set()
        unique_entities = []

        for entity in entities:
            key = (entity["type"], entity["name"].lower())
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)

        return unique_entities


class TimelineAnalyzer(BaseAnalyzer):
    """Analyzer for extracting timeline events from evidence content."""

    def __init__(self):
        # Define date patterns
        self.date_patterns = [
            r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b",  # MM/DD/YYYY or DD/MM/YYYY
            r"\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b",  # YYYY/MM/DD
            r"\b([A-Z][a-z]+ \d{1,2},? \d{4})\b",  # Month DD, YYYY
            r"\b(\d{1,2} [A-Z][a-z]+ \d{4})\b",  # DD Month YYYY
            r"\b([A-Z][a-z]+ \d{4})\b",  # Month YYYY
        ]

        # Define time patterns
        self.time_patterns = [r"\b(\d{1,2}:\d{2}(?::\d{2})?\s?(?:AM|PM|am|pm)?)\b"]

        # Define event significance keywords
        self.significance_keywords = {
            "critical": [
                "criminal",
                "violation",
                "fraud",
                "illegal",
                "breach",
                "notice",
            ],
            "high": ["deadline", "formal", "legal", "court", "evidence"],
            "medium": ["payment", "instruction", "communication", "meeting"],
            "low": ["email", "correspondence", "routine"],
        }

    def extract_timeline_events(self, content: str) -> List[Dict[str, Any]]:
        """Extract timeline events from content."""
        events = []

        # Find all date matches
        for pattern in self.date_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                date_str = match.group(1)
                context = self._get_context(content, match.start(), match.end(), 200)

                # Try to find associated time
                time_str = self._find_associated_time(
                    content, match.start(), match.end()
                )

                # Extract event description from context
                description = self._extract_event_description(context, date_str)

                # Determine event significance
                significance = self._determine_significance(context)

                event = {
                    "date": self._normalize_date(date_str),
                    "time": time_str,
                    "description": description,
                    "significance": significance,
                    "context": context,
                    "raw_date": date_str,
                }

                events.append(event)

        # Remove duplicates and sort by date
        events = self._deduplicate_events(events)
        events.sort(key=lambda x: self._parse_date_for_sorting(x["date"]))

        return events

    def _get_context(
        self, content: str, start: int, end: int, window: int = 200
    ) -> str:
        """Get context around a date match."""
        context_start = max(0, start - window)
        context_end = min(len(content), end + window)
        return content[context_start:context_end].strip()

    def _find_associated_time(
        self, content: str, date_start: int, date_end: int
    ) -> Optional[str]:
        """Find time associated with a date."""
        # Look for time within 50 characters of the date
        search_start = max(0, date_start - 50)
        search_end = min(len(content), date_end + 50)
        search_area = content[search_start:search_end]

        for pattern in self.time_patterns:
            match = re.search(pattern, search_area)
            if match:
                return match.group(1)

        return None

    def _extract_event_description(self, context: str, date_str: str) -> str:
        """Extract event description from context."""
        # Split context into sentences
        sentences = re.split(r"[.!?]+", context)

        # Find sentence containing the date
        for sentence in sentences:
            if date_str in sentence:
                # Clean and return the sentence
                description = sentence.strip()
                # Remove the date from the description
                description = re.sub(re.escape(date_str), "", description).strip()
                # Clean up extra whitespace and punctuation
                description = re.sub(r"\s+", " ", description)
                description = description.strip(" ,-:")

                if description:
                    return description

        # Fallback: return first meaningful sentence
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:
                return sentence

        return "Event occurred"

    def _determine_significance(self, context: str) -> str:
        """Determine event significance based on context keywords."""
        context_lower = context.lower()

        for significance, keywords in self.significance_keywords.items():
            for keyword in keywords:
                if keyword in context_lower:
                    return significance.title()

        return "Standard"

    def _normalize_date(self, date_str: str) -> str:
        """Normalize date string to a standard format."""
        # Try to parse various date formats
        date_formats = [
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y/%m/%d",
            "%m-%d-%Y",
            "%d-%m-%Y",
            "%Y-%m-%d",
            "%B %d, %Y",
            "%B %d %Y",
            "%d %B %Y",
            "%B %Y",
        ]

        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                continue

        # If parsing fails, return original string
        return date_str

    def _parse_date_for_sorting(self, date_str: str) -> datetime:
        """Parse date string for sorting purposes."""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            # Return a default date for unparseable dates
            return datetime(1900, 1, 1)

    def _deduplicate_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate events based on date and description."""
        seen = set()
        unique_events = []

        for event in events:
            key = (
                event["date"],
                event["description"][:50],
            )  # Use first 50 chars of description
            if key not in seen:
                seen.add(key)
                unique_events.append(event)

        return unique_events


class LegalAnalyzer(BaseAnalyzer):
    """Analyzer for identifying legal violations and issues."""

    def __init__(self):
        # Define legal violation patterns
        self.violation_patterns = {
            "popi_act": [
                r"POPI Act",
                r"Protection of Personal Information",
                r"unauthorized data access",
                r"data protection violation",
            ],
            "companies_act": [
                r"Companies Act",
                r"Section 76",
                r"fiduciary duty",
                r"director.*breach",
            ],
            "fraud": [
                r"fraud",
                r"misrepresentation",
                r"criminal.*instruction",
                r"unauthorized.*transaction",
            ],
            "criminal": [
                r"criminal.*charge",
                r"criminal.*conduct",
                r"criminal.*instruction",
                r"conspiracy",
            ],
        }

        # Define penalty patterns
        self.penalty_patterns = [
            r"R(\d{1,3}(?:,\d{3})*) (?:million )?fine",
            r"(\d+) years? imprisonment",
            r"maximum.*penalty.*R(\d{1,3}(?:,\d{3})*)",
            r"fine.*(\d+) years",
        ]

    def analyze_legal_violations(self, content: str) -> List[Dict[str, Any]]:
        """Analyze content for legal violations."""
        violations = []

        for category, patterns in self.violation_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    context = self._get_context(
                        content, match.start(), match.end(), 300
                    )

                    # Extract penalties if mentioned
                    penalties = self._extract_penalties(context)

                    # Determine severity
                    severity = self._determine_severity(category, context)

                    violation = {
                        "category": category.replace("_", " ").title(),
                        "description": self._extract_violation_description(
                            context, match.group(0)
                        ),
                        "severity": severity,
                        "penalties": penalties,
                        "context": context,
                        "matched_text": match.group(0),
                    }

                    violations.append(violation)

        # Remove duplicates and sort by severity
        violations = self._deduplicate_violations(violations)
        severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        violations.sort(key=lambda x: severity_order.get(x["severity"], 4))

        return violations

    def _get_context(
        self, content: str, start: int, end: int, window: int = 300
    ) -> str:
        """Get context around a violation match."""
        context_start = max(0, start - window)
        context_end = min(len(content), end + window)
        return content[context_start:context_end].strip()

    def _extract_penalties(self, context: str) -> List[str]:
        """Extract penalty information from context."""
        penalties = []

        for pattern in self.penalty_patterns:
            matches = re.finditer(pattern, context, re.IGNORECASE)
            for match in matches:
                penalties.append(match.group(0))

        return penalties

    def _determine_severity(self, category: str, context: str) -> str:
        """Determine violation severity."""
        context_lower = context.lower()

        # Critical severity indicators
        if any(
            word in context_lower
            for word in ["criminal", "imprisonment", "fraud", "conspiracy"]
        ):
            return "Critical"

        # High severity indicators
        if any(
            word in context_lower
            for word in ["breach", "violation", "unauthorized", "illegal"]
        ):
            return "High"

        # Medium severity indicators
        if any(
            word in context_lower for word in ["non-compliance", "failure", "improper"]
        ):
            return "Medium"

        # Default based on category
        category_severity = {
            "popi_act": "High",
            "companies_act": "High",
            "fraud": "Critical",
            "criminal": "Critical",
        }

        return category_severity.get(category, "Medium")

    def _extract_violation_description(self, context: str, matched_text: str) -> str:
        """Extract violation description from context."""
        # Split context into sentences
        sentences = re.split(r"[.!?]+", context)

        # Find sentence containing the matched text
        for sentence in sentences:
            if matched_text.lower() in sentence.lower():
                description = sentence.strip()
                if len(description) > 10:
                    return description

        # Fallback: return first meaningful sentence
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:
                return sentence

        return f"Violation related to {matched_text}"

    def _deduplicate_violations(
        self, violations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Remove duplicate violations."""
        seen = set()
        unique_violations = []

        for violation in violations:
            key = (violation["category"], violation["description"][:100])
            if key not in seen:
                seen.add(key)
                unique_violations.append(violation)

        return unique_violations
