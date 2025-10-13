#!/usr/bin/env python3
"""
Process Recent Documents - Wrapper Script
=========================================

Simple wrapper to process recently added documents in the current repository.
Auto-detects workspace path and provides clear reporting.
"""

import sys
from pathlib import Path

from process_new_documents import DocumentProcessor


def main():
    """Process recently added documents with enhanced reporting"""
    print("=== PROCESSING RECENTLY ADDED DOCUMENTS ===")
    print()

    # Initialize processor with auto-detection
    processor = DocumentProcessor()

    print(f"📁 Workspace: {processor.workspace_path}")
    print(f"📄 Documents folder: {processor.docs_path}")
    print(f"🗂️  Case folder: {processor.case_path}")
    print()

    # Check if required directories exist
    if not processor.docs_path.exists():
        print(f"❌ Error: Documents folder not found at {processor.docs_path}")
        return 1

    if not processor.case_path.exists():
        print(
            f"⚠️  Warning: Case folder doesn't exist - will be created at {processor.case_path}"
        )

    print("🔄 Starting document processing...")

    # Process documents
    results = processor.process_new_documents()

    # Report results
    print()
    print("=== PROCESSING RESULTS ===")
    print(f"✅ Processed: {len(results['processed'])} new documents")
    print(f"⏭️  Skipped: {len(results['skipped'])} already processed documents")
    print(f"❌ Errors: {len(results['errors'])} processing errors")

    # Show processed documents
    if results["processed"]:
        print()
        print("📋 NEWLY PROCESSED DOCUMENTS:")
        for doc in results["processed"]:
            print(f"   • {doc['file']} → {doc['destination']}")

    # Show errors if any
    if results["errors"]:
        print()
        print("🚨 PROCESSING ERRORS:")
        for error in results["errors"]:
            print(f"   • {error['file']}: {error['error']}")

    # Update hypergraph and generate report
    if results["processed"] or results["errors"]:
        print()
        print("🔄 Updating case hypergraph...")
        processor.update_case_hypergraph(results)

        print("📝 Generating integration report...")
        report_path = processor.generate_integration_report(results)
        print(f"📄 Report saved to: {report_path}")

        # Save detailed results
        results_path = processor.workspace_path / "document_processing_results.json"
        with open(results_path, "w") as f:
            import json

            json.dump(results, f, indent=2)
        print(f"💾 Detailed results saved to: {results_path}")

    print()
    if results["processed"]:
        print(f"🎉 Successfully processed {len(results['processed'])} new documents!")
    else:
        print("✅ All documents are up to date!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
