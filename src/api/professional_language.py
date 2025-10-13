#!/usr/bin/env python3
"""
Professional Language Processor
==============================

Processes documents to replace emotional or subjective language with
professional investigative terminology focused on facts, evidence,
and logical relationships.

Removes "scare language" and implements professional presentation standards.
"""

import json
import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple


class LanguageType(Enum):
    """Types of language patterns to process"""

    EMOTIONAL = "emotional"
    SUBJECTIVE = "subjective"
    URGENT = "urgent"
    PROFESSIONAL = "professional"
    FACTUAL = "factual"


@dataclass
class LanguagePattern:
    """Pattern for language replacement"""

    pattern: str
    replacement: str
    pattern_type: LanguageType
    description: str
    confidence: float = 1.0


class ProfessionalLanguageProcessor:
    """
    Professional Language Processor

    Converts documents from emotional/urgent language to professional
    investigative terminology with focus on clarity and accuracy.
    """

    def __init__(self):
        self.replacement_patterns = self._initialize_patterns()
        self.processed_documents = {}
        self.statistics = {
            "documents_processed": 0,
            "replacements_made": 0,
            "patterns_matched": {},
        }

    def _initialize_patterns(self) -> List[LanguagePattern]:
        """Initialize professional language replacement patterns"""
        patterns = [
            # Urgent/Emergency language
            LanguagePattern(
                r"🚨\s*(CRITICAL|EMERGENCY|URGENT|ALERT)",
                "Analysis indicates",
                LanguageType.URGENT,
                "Replace urgent indicators with professional assessment",
            ),
            LanguagePattern(
                r"GET TO SAFETY NOW!!",
                "Risk assessment recommends appropriate protective measures",
                LanguageType.URGENT,
                "Replace safety commands with professional recommendations",
            ),
            LanguagePattern(
                r"CRITICAL WARNING FIRST",
                "Primary consideration:",
                LanguageType.URGENT,
                "Replace warning language with structured priority indication",
            ),
            LanguagePattern(
                r"CRITICAL ALERT:",
                "Investigation findings indicate:",
                LanguageType.URGENT,
                "Replace alert language with investigation findings",
            ),
            # Emotional language
            LanguagePattern(
                r"EXPLOSIVE EVIDENCE",
                "Significant evidence",
                LanguageType.EMOTIONAL,
                "Replace dramatic descriptors with factual assessment",
            ),
            LanguagePattern(
                r"(SHOCKING|DEVASTATING|HORRIFIC)",
                "Notable",
                LanguageType.EMOTIONAL,
                "Replace emotional adjectives with neutral descriptors",
            ),
            LanguagePattern(
                r"(DANGEROUS|THREATENING|SCARY)",
                "requires assessment for risk factors",
                LanguageType.EMOTIONAL,
                "Replace danger language with risk assessment terms",
            ),
            # Subjective assessments
            LanguagePattern(
                r"OBVIOUSLY",
                "Evidence indicates",
                LanguageType.SUBJECTIVE,
                "Replace subjective certainty with evidence-based statements",
            ),
            LanguagePattern(
                r"CLEARLY",
                "Analysis shows",
                LanguageType.SUBJECTIVE,
                "Replace subjective clarity with analytical findings",
            ),
            LanguagePattern(
                r"WITHOUT A DOUBT",
                "Documentation supports the conclusion that",
                LanguageType.SUBJECTIVE,
                "Replace certainty claims with evidence-based conclusions",
            ),
            # Conspiracy language
            LanguagePattern(
                r"CRIMINAL CONSPIRACY",
                "coordinated activities requiring investigation",
                LanguageType.PROFESSIONAL,
                "Replace legal conclusions with investigative observations",
            ),
            LanguagePattern(
                r"CRIMINAL OPERATION",
                "organized activities",
                LanguageType.PROFESSIONAL,
                "Replace criminal determinations with operational descriptions",
            ),
            # Status indicators
            LanguagePattern(
                r"Status.*?🚨.*?(CRITICAL|EMERGENCY)",
                "Status: Requires investigation priority",
                LanguageType.URGENT,
                "Replace status alerts with professional priority indicators",
            ),
            # Action urgency
            LanguagePattern(
                r"(IMMEDIATE|URGENT|EMERGENCY)\s+(ACTION|RESPONSE|ATTENTION)",
                "Priority attention",
                LanguageType.URGENT,
                "Replace urgent action language with priority indicators",
            ),
            # Investigation language
            LanguagePattern(
                r"INVESTIGATION REVEALS",
                "Analysis indicates",
                LanguageType.PROFESSIONAL,
                "Standardize investigation language",
            ),
            LanguagePattern(
                r"EVIDENCE SHOWS",
                "Documentation indicates",
                LanguageType.PROFESSIONAL,
                "Standardize evidence presentation",
            ),
            # Risk language
            LanguagePattern(
                r"HIGH RISK",
                "Risk factors require assessment",
                LanguageType.PROFESSIONAL,
                "Replace risk determinations with assessment requirements",
            ),
            LanguagePattern(
                r"EXTREME DANGER",
                "Risk assessment indicates elevated concern levels",
                LanguageType.PROFESSIONAL,
                "Replace danger language with professional risk assessment",
            ),
            # Certainty modifiers
            LanguagePattern(
                r"CONFIRMED:",
                "Documentation supports:",
                LanguageType.PROFESSIONAL,
                "Replace confirmation language with documentation reference",
            ),
            LanguagePattern(
                r"VERIFIED:",
                "Cross-reference analysis indicates:",
                LanguageType.PROFESSIONAL,
                "Replace verification language with analysis indicators",
            ),
            # Emphasis patterns
            LanguagePattern(
                r"!!+",
                ".",
                LanguageType.EMOTIONAL,
                "Replace multiple exclamation marks with professional punctuation",
            ),
            LanguagePattern(
                r"\*\*(.*?)\*\*",
                r"\1",
                LanguageType.EMOTIONAL,
                "Remove markdown emphasis for professional presentation",
            ),
            # Timeline urgency
            LanguagePattern(
                r"(0-24 hours?|IMMEDIATE|NOW|ASAP)",
                "Priority timeframe",
                LanguageType.URGENT,
                "Replace time urgency with priority indicators",
            ),
        ]

        return patterns

    def process_document(
        self, content: str, document_id: str = None, preserve_structure: bool = True
    ) -> Dict[str, any]:
        """
        Process document content to replace non-professional language

        Args:
            content: Document content to process
            document_id: Optional identifier for the document
            preserve_structure: Whether to preserve markdown structure

        Returns:
            Dictionary with processed content and statistics
        """
        if document_id is None:
            document_id = f"doc_{len(self.processed_documents) + 1}"

        processed_content = content
        replacements_made = []

        # Apply each pattern
        for pattern in self.replacement_patterns:
            matches = re.findall(
                pattern.pattern, processed_content, re.IGNORECASE | re.MULTILINE
            )

            if matches:
                # Track pattern usage
                pattern_key = pattern.description
                if pattern_key not in self.statistics["patterns_matched"]:
                    self.statistics["patterns_matched"][pattern_key] = 0
                self.statistics["patterns_matched"][pattern_key] += len(matches)

                # Apply replacement
                processed_content = re.sub(
                    pattern.pattern,
                    pattern.replacement,
                    processed_content,
                    flags=re.IGNORECASE | re.MULTILINE,
                )

                replacements_made.append(
                    {
                        "pattern": pattern.pattern,
                        "replacement": pattern.replacement,
                        "matches": len(matches),
                        "type": pattern.pattern_type.value,
                        "description": pattern.description,
                    }
                )

        # Clean up formatting issues
        processed_content = self._clean_formatting(
            processed_content, preserve_structure
        )

        # Store processing results
        result = {
            "document_id": document_id,
            "original_length": len(content),
            "processed_length": len(processed_content),
            "replacements_made": replacements_made,
            "total_replacements": sum(r["matches"] for r in replacements_made),
            "processed_content": processed_content,
            "processing_timestamp": "2025-01-03T00:00:00",  # Placeholder for actual timestamp
        }

        self.processed_documents[document_id] = result
        self.statistics["documents_processed"] += 1
        self.statistics["replacements_made"] += result["total_replacements"]

        return result

    def _clean_formatting(self, content: str, preserve_structure: bool) -> str:
        """Clean up formatting issues from replacements"""
        # Remove multiple spaces
        content = re.sub(r" +", " ", content)

        # Fix punctuation spacing
        content = re.sub(r" +\.", ".", content)
        content = re.sub(r" +,", ",", content)
        content = re.sub(r" +:", ":", content)

        # Clean up line breaks
        content = re.sub(r"\n\s*\n\s*\n+", "\n\n", content)

        # Fix sentence spacing
        content = re.sub(r"\.(?=[A-Z])", ". ", content)

        if preserve_structure:
            # Preserve markdown headers
            content = re.sub(
                r"^#+\s*(.+)$",
                lambda m: f"{'#' * len(m.group().split()[0])} {' '.join(m.group().split()[1:])}",
                content,
                flags=re.MULTILINE,
            )

        return content.strip()

    def process_file(
        self, filepath: str, output_filepath: str = None, backup_original: bool = True
    ) -> Dict[str, any]:
        """
        Process a file and optionally save the result

        Args:
            filepath: Path to file to process
            output_filepath: Optional output path (defaults to original with .processed suffix)
            backup_original: Whether to create backup of original file

        Returns:
            Processing results dictionary
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return {"error": f"Failed to read file: {str(e)}"}

        # Process content
        result = self.process_document(content, filepath)

        # Save processed content if output path specified
        if output_filepath:
            try:
                # Backup original if requested
                if backup_original:
                    backup_path = f"{filepath}.backup"
                    with open(backup_path, "w", encoding="utf-8") as f:
                        f.write(content)

                # Write processed content
                with open(output_filepath, "w", encoding="utf-8") as f:
                    f.write(result["processed_content"])

                result["output_file"] = output_filepath
                if backup_original:
                    result["backup_file"] = backup_path

            except Exception as e:
                result["file_error"] = f"Failed to save processed file: {str(e)}"

        return result

    def analyze_language_patterns(self, content: str) -> Dict[str, any]:
        """
        Analyze language patterns in content without processing

        Returns analysis of language types and suggestions
        """
        analysis = {
            "urgent_language_count": 0,
            "emotional_language_count": 0,
            "subjective_language_count": 0,
            "professional_opportunities": [],
            "pattern_matches": {},
        }

        for pattern in self.replacement_patterns:
            matches = re.findall(pattern.pattern, content, re.IGNORECASE | re.MULTILINE)

            if matches:
                pattern_key = pattern.description
                analysis["pattern_matches"][pattern_key] = len(matches)

                if pattern.pattern_type == LanguageType.URGENT:
                    analysis["urgent_language_count"] += len(matches)
                elif pattern.pattern_type == LanguageType.EMOTIONAL:
                    analysis["emotional_language_count"] += len(matches)
                elif pattern.pattern_type == LanguageType.SUBJECTIVE:
                    analysis["subjective_language_count"] += len(matches)

                analysis["professional_opportunities"].append(
                    {
                        "current": matches[0] if matches else pattern.pattern,
                        "suggested": pattern.replacement,
                        "improvement": pattern.description,
                    }
                )

        # Calculate professionalism score
        total_issues = (
            analysis["urgent_language_count"]
            + analysis["emotional_language_count"]
            + analysis["subjective_language_count"]
        )

        content_length = len(content.split())
        if content_length > 0:
            professionalism_score = max(
                0, 100 - (total_issues * 100 / content_length * 10)
            )
        else:
            professionalism_score = 100

        analysis["professionalism_score"] = round(professionalism_score, 2)
        analysis["total_improvement_opportunities"] = total_issues

        return analysis

    def generate_style_guide(self) -> Dict[str, any]:
        """Generate professional style guide based on patterns"""
        guide = {
            "professional_language_standards": {
                "objective_terminology": [
                    "Analysis indicates",
                    "Documentation shows",
                    "Evidence supports",
                    "Investigation findings",
                    "Risk assessment indicates",
                ],
                "avoid_emotional_language": [
                    "Instead of 'SHOCKING': Use 'Notable'",
                    "Instead of 'DANGEROUS': Use 'requires risk assessment'",
                    "Instead of 'CRITICAL ALERT': Use 'Investigation findings indicate'",
                    "Instead of 'GET TO SAFETY': Use 'Risk assessment recommends protective measures'",
                ],
                "professional_priorities": [
                    "Use 'Priority attention' instead of 'URGENT ACTION'",
                    "Use 'Requires investigation priority' instead of 'CRITICAL STATUS'",
                    "Use 'Priority timeframe' instead of 'IMMEDIATE/NOW/ASAP'",
                ],
                "evidence_presentation": [
                    "Use 'Documentation indicates' instead of 'EVIDENCE SHOWS'",
                    "Use 'Cross-reference analysis indicates' instead of 'VERIFIED'",
                    "Use 'Analysis supports conclusion' instead of 'WITHOUT A DOUBT'",
                ],
            },
            "formatting_standards": {
                "punctuation": "Use single periods instead of multiple exclamation marks",
                "emphasis": "Avoid markdown emphasis (**bold**) in professional documents",
                "structure": "Maintain clear headers and organized sections",
                "spacing": "Use consistent spacing and paragraph breaks",
            },
            "investigative_terminology": {
                "findings": "Present findings as analysis results, not absolute conclusions",
                "risk_assessment": "Use risk assessment terminology instead of danger warnings",
                "evidence": "Reference documentation and cross-verification",
                "recommendations": "Provide professional recommendations instead of commands",
            },
        }

        return guide

    def export_processing_statistics(self) -> Dict[str, any]:
        """Export comprehensive processing statistics"""
        return {
            "processing_overview": {
                "documents_processed": self.statistics["documents_processed"],
                "total_replacements": self.statistics["replacements_made"],
                "average_replacements_per_document": (
                    self.statistics["replacements_made"]
                    / max(1, self.statistics["documents_processed"])
                ),
            },
            "pattern_usage": self.statistics["patterns_matched"],
            "most_common_issues": sorted(
                [
                    (pattern, count)
                    for pattern, count in self.statistics["patterns_matched"].items()
                ],
                key=lambda x: x[1],
                reverse=True,
            )[:10],
            "language_improvement_impact": {
                "total_patterns_available": len(self.replacement_patterns),
                "patterns_used": len(self.statistics["patterns_matched"]),
                "coverage_percentage": round(
                    len(self.statistics["patterns_matched"])
                    / len(self.replacement_patterns)
                    * 100,
                    2,
                ),
            },
        }


def create_sample_processor():
    """Create sample language processor for testing"""
    processor = ProfessionalLanguageProcessor()

    # Sample content with non-professional language
    sample_content = """
    # 🚨 CRITICAL ALERT: Investigation Findings
    
    CRITICAL WARNING FIRST: GET TO SAFETY NOW!!
    
    The investigation CLEARLY shows EXPLOSIVE EVIDENCE of DANGEROUS activities.
    WITHOUT A DOUBT, this is OBVIOUSLY a CRIMINAL OPERATION.
    
    **URGENT ACTION** required in 0-24 hours!!
    
    Status: 🚨 CRITICAL - IMMEDIATE RESPONSE needed.
    
    CONFIRMED: Evidence SHOWS systematic deception patterns.
    """

    # Process the sample content
    result = processor.process_document(sample_content, "sample_doc")

    return processor, result


if __name__ == "__main__":
    # Demonstrate professional language processor
    processor, result = create_sample_processor()

    print("=== ORIGINAL CONTENT ===")
    print(result["processed_content"][:200] + "...")

    print("\n=== PROCESSING STATISTICS ===")
    stats = processor.export_processing_statistics()
    print(json.dumps(stats, indent=2))

    print("\n=== STYLE GUIDE ===")
    guide = processor.generate_style_guide()
    print(json.dumps(guide, indent=2))
