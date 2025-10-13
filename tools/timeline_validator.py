"""
Timeline Validation Utility for Criminal Case Documentation (REVISED)

This script now validates timeline documents for evidence of escalating criminal activity,
including malicious prosecution and witness intimidation.

Usage:
    python3 tools/timeline_validator.py docs/JUN-SEP-2025.md
    python3 tools/timeline_validator.py --check-all
"""


import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict


class TimelineValidator:
    """Validates timeline documents against framework requirements."""

    def __init__(self):
        self.framework_phases = [
            "pre-investigation",
            "investigation",
            "prosecution",
            "trial",
        ]

        # Added new keywords for the second interdict and witness intimidation
        self.legal_keywords = [
            "criminal", "fraud", "perjury", "conspiracy", "evidence",
            "court", "hawks", "investigation", "witness intimidation",
            "malicious prosecution", "second interdict", "medical testing"
        ]

        self.validation_results = {
            "errors": [],
            "warnings": [],
            "info": [],
            "framework_compliance": False,
            "escalation_analysis": False, # New check for escalation
        }

    def validate_timeline_file(self, filepath: str) -> Dict:
        """Validate a single timeline file."""
        if not os.path.exists(filepath):
            self.validation_results["errors"].append(f"File not found: {filepath}")
            return self.validation_results

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Reset results for new file
        self.validation_results = {
            "errors": [],
            "warnings": [],
            "info": [],
            "framework_compliance": False,
            "escalation_analysis": False,
        }

        self._check_framework_compliance(content)
        self._check_for_escalation(content)
        self._extract_key_information(content)

        return self.validation_results

    def _check_framework_compliance(self, content: str):
        """Check if timeline follows framework phases."""
        content_lower = content.lower()
        found_phases = [phase for phase in self.framework_phases if phase in content_lower]

        if len(found_phases) >= 2:
            self.validation_results["framework_compliance"] = True
            self.validation_results["info"].append(f"Framework compliance: Found {len(found_phases)} phases.")
        else:
            self.validation_results["warnings"].append("Limited framework compliance.")

    def _check_for_escalation(self, content: str):
        """Check for analysis of the escalating criminal activity."""
        content_lower = content.lower()
        escalation_keywords = ["second interdict", "witness intimidation", "malicious prosecution"]
        found_keywords = [kw for kw in escalation_keywords if kw in content_lower]

        if len(found_keywords) > 0:
            self.validation_results["escalation_analysis"] = True
            self.validation_results["info"].append(f"Escalation analysis found: {', '.join(found_keywords)}")
        else:
            self.validation_results["warnings"].append("No analysis of the second interdict or witness intimidation found.")

    def _extract_key_information(self, content: str):
        """Extract key legal keywords."""
        content_lower = content.lower()
        found_keywords = [keyword for keyword in self.legal_keywords if keyword in content_lower]

        if found_keywords:
            self.validation_results["info"].append(f"Legal keywords found: {len(found_keywords)}")

    def print_validation_report(self, filepath: str, results: Dict):
        """Print a formatted validation report."""
        print(f"\n{'='*60}")
        print("TIMELINE VALIDATION REPORT (REVISED)")
        print(f"{'='*60}")
        print(f"File: {filepath}")
        print(f"Validated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")

        # Summary
        print("\nSUMMARY:")
        print(f"Framework Compliance: {'✅ PASS' if results['framework_compliance'] else '⚠️  NEEDS REVIEW'}")
        print(f"Escalation Analysis: {'✅ PASS' if results['escalation_analysis'] else '❌ FAILED'}")

        total_issues = len(results["errors"]) + len(results["warnings"])
        print(f"Total Issues: {total_issues}")

        if results["errors"]:
            print(f"\n❌ ERRORS ({len(results['errors'])}):")
            for error in results["errors"]:
                print(f"   • {error}")

        if results["warnings"]:
            print(f"\n⚠️  WARNINGS ({len(results['warnings'])}):")
            for warning in results["warnings"]:
                print(f"   • {warning}")

        print(f"\n{'='*60}")
        print("RECOMMENDATIONS:")
        if not results["escalation_analysis"]:
            print("   • CRITICAL: Update timeline to include analysis of the second interdict and witness intimidation pattern.")
        if total_issues == 0 and results["escalation_analysis"]:
            print("   • Timeline document appears up-to-date with recent escalations. ✅")
        print(f"{'='*60}\n")


def main():
    """Main function to run timeline validation."""
    if len(sys.argv) < 2:
        print("Usage: python3 timeline_validator.py <timeline_file.md> or --check-all")
        sys.exit(1)

    validator = TimelineValidator()

    if sys.argv[1] == "--check-all":
        # Check all markdown files in the case directory
        case_dir = Path("/home/ubuntu/analysis/case_2025_137857")
        if case_dir.exists():
            timeline_files = list(case_dir.rglob("*.md"))
            print(f"Found {len(timeline_files)} markdown files to validate...")
            for file_path in timeline_files:
                results = validator.validate_timeline_file(str(file_path))
                validator.print_validation_report(str(file_path), results)
        else:
            print("Case directory not found.")
    else:
        filepath = sys.argv[1]
        results = validator.validate_timeline_file(filepath)
        validator.print_validation_report(filepath, results)


if __name__ == "__main__":
    main()

