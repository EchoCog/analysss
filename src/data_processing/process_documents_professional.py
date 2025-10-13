#!/usr/bin/env python3
"""
Professional Document Processing Script
======================================

Processes existing repository documents to replace non-professional language
with objective investigative terminology.
"""

import os
import sys
from pathlib import Path

from hypergnn_framework_improved import (
    AnalysisConfiguration,
    AnalysisScope,
    ComplexityLevel,
)

from frameworks.hypergnn_core import HyperGNNFramework


def find_documents_to_process(base_path: str) -> list:
    """Find markdown documents that may contain non-professional language"""

    documents = []
    base = Path(base_path)

    # Priority documents to process
    priority_files = [
        "docs/eviden-thread.md",
        "docs/court-order-timeline-cross-reference-analysis.md",
        "docs/APR-SEP-2025.md",
        "docs/comprehensive-ocr-assumptions-analysis.md",
        "docs/ocr-email-cc-analysis-critical-findings.md",
    ]

    # Check if priority files exist
    for file_path in priority_files:
        full_path = base / file_path
        if full_path.exists():
            documents.append(str(full_path))
            print(f"Found priority document: {file_path}")

    # Find additional markdown files
    for md_file in base.rglob("*.md"):
        if str(md_file) not in documents and "README" not in md_file.name:
            documents.append(str(md_file))

    return documents


def process_documents_for_professional_language(
    documents: list, output_dir: str = None
):
    """Process documents using HyperGNN professional language processor"""

    if not documents:
        print("No documents found to process")
        return

    # Create HyperGNN framework for language processing
    config = AnalysisConfiguration(
        case_id="professional_language_processing",
        scope=AnalysisScope.COMPREHENSIVE,
        complexity_level=ComplexityLevel.ADVANCED,
        enable_evidence_management=False,  # Not needed for language processing
        enable_system_dynamics=False,  # Not needed for language processing
        enable_language_processing=True,  # This is what we need
        enable_verification_tracking=False,
        enable_knowledge_matrix=False,
        output_directory=output_dir,
    )

    framework = HyperGNNFramework(config)

    if not framework.initialized:
        print("Failed to initialize framework")
        return

    print(f"Processing {len(documents)} documents for professional language...")

    # Process each document
    results = framework.process_documents_for_professional_language(documents)

    print(f"\n=== PROCESSING RESULTS ===")
    print(f"Documents processed: {results.get('documents_processed', 0)}")
    print(f"Total replacements made: {results.get('total_replacements', 0)}")

    # Show detailed results
    for file_result in results.get("processed_files", []):
        if "error" in file_result:
            print(f"❌ {file_result['original']}: {file_result['error']}")
        else:
            print(
                f"✅ {file_result['original']}: {file_result.get('replacements', 0)} replacements"
            )
            if file_result.get("processed"):
                print(f"   → Processed: {file_result['processed']}")
            if file_result.get("backup"):
                print(f"   → Backup: {file_result['backup']}")

    # Show processing summary
    if "processing_summary" in results:
        summary = results["processing_summary"]
        print(f"\n=== PROCESSING SUMMARY ===")

        if "most_common_issues" in summary:
            print("Most common language improvements:")
            for issue, count in summary["most_common_issues"][:5]:
                print(f"  • {issue}: {count} times")

        if "language_improvement_impact" in summary:
            impact = summary["language_improvement_impact"]
            print(
                f"\nLanguage improvement coverage: {impact.get('coverage_percentage', 0)}%"
            )

    return results


def main():
    """Main processing function"""
    # Get repository base path
    repo_path = os.path.dirname(os.path.abspath(__file__))

    print("=== PROFESSIONAL LANGUAGE PROCESSING ===")
    print(f"Repository path: {repo_path}")

    # Find documents to process
    documents = find_documents_to_process(repo_path)

    if not documents:
        print("No documents found to process")
        return

    print(f"Found {len(documents)} documents to process")

    # Process documents
    results = process_documents_for_professional_language(
        documents, f"{repo_path}/processed_docs"
    )

    print("\n=== PROCESSING COMPLETE ===")

    # Generate professional language style guide
    config = AnalysisConfiguration(
        case_id="style_guide_generation",
        scope=AnalysisScope.COMPREHENSIVE,
        complexity_level=ComplexityLevel.ADVANCED,
        enable_language_processing=True,
        enable_evidence_management=False,
        enable_system_dynamics=False,
        enable_verification_tracking=False,
        enable_knowledge_matrix=False,
    )

    framework = HyperGNNFramework(config)

    if framework.initialized and "language" in framework.components:
        style_guide = framework.components["language"].generate_style_guide()

        # Save style guide
        style_guide_path = f"{repo_path}/PROFESSIONAL_LANGUAGE_STYLE_GUIDE.md"

        with open(style_guide_path, "w") as f:
            f.write("# Professional Language Style Guide\n\n")
            f.write(
                "This guide provides standards for professional investigative documentation.\n\n"
            )

            # Objective terminology
            f.write("## Objective Terminology\n\n")
            for term in style_guide["professional_language_standards"][
                "objective_terminology"
            ]:
                f.write(f"- {term}\n")
            f.write("\n")

            # Avoid emotional language
            f.write("## Avoid Emotional Language\n\n")
            for guideline in style_guide["professional_language_standards"][
                "avoid_emotional_language"
            ]:
                f.write(f"- {guideline}\n")
            f.write("\n")

            # Professional priorities
            f.write("## Professional Priority Language\n\n")
            for guideline in style_guide["professional_language_standards"][
                "professional_priorities"
            ]:
                f.write(f"- {guideline}\n")
            f.write("\n")

            # Evidence presentation
            f.write("## Evidence Presentation\n\n")
            for guideline in style_guide["professional_language_standards"][
                "evidence_presentation"
            ]:
                f.write(f"- {guideline}\n")
            f.write("\n")

            # Formatting standards
            f.write("## Formatting Standards\n\n")
            for standard, description in style_guide["formatting_standards"].items():
                f.write(f"- **{standard.title()}**: {description}\n")
            f.write("\n")

            # Investigative terminology
            f.write("## Investigative Terminology Guidelines\n\n")
            for area, guideline in style_guide["investigative_terminology"].items():
                f.write(f"- **{area.title()}**: {guideline}\n")

        print(f"✅ Style guide saved to: {style_guide_path}")


if __name__ == "__main__":
    main()
