#!/usr/bin/env python3
"""
Cleanup Script for Outdated Files
=================================

This script identifies and optionally removes outdated or duplicate files
from the rzonedevops/analysis repository to improve maintainability.
"""

import os
import shutil
from pathlib import Path
from typing import Any, Dict, List


def identify_outdated_files() -> Dict[str, List[str]]:
    """Identify files that appear to be outdated or duplicates."""

    outdated_files = {
        "old_versions": [
            "case_data_loader_old.py",
            "discrete_event_model_simplified.py",
            "requirements_llm.txt",  # Superseded by pyproject.toml
            "requirements_updated.txt",  # Superseded by improved requirements
        ],
        "potential_duplicates": [
            # These need manual review
            "hypergnn_framework_improved.py",  # vs hypergnn_framework.py
            "database_schema_enhanced.sql",  # vs database_schema_improved.sql
        ],
        "temporary_files": [
            # Look for common temporary file patterns
        ],
    }

    # Add any .pyc files or __pycache__ directories
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".pyc"):
                outdated_files["temporary_files"].append(os.path.join(root, file))
        for dir_name in dirs:
            if dir_name == "__pycache__":
                outdated_files["temporary_files"].append(os.path.join(root, dir_name))

    return outdated_files


def analyze_file_sizes() -> Dict[str, int]:
    """Analyze file sizes to identify unusually large files."""

    large_files = {}

    for root, dirs, files in os.walk("."):
        # Skip node_modules and other large directories
        if "node_modules" in root or ".git" in root:
            continue

        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                # Flag files larger than 1MB
                if size > 1024 * 1024:
                    large_files[file_path] = size
            except OSError:
                continue

    return large_files


def create_backup_list(files_to_remove: List[str]) -> str:
    """Create a backup list of files before removal."""

    backup_content = "# Backup list of files removed during cleanup\n"
    backup_content += f"# Generated on: {os.popen('date').read().strip()}\n\n"

    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                size = os.path.getsize(file_path)
                backup_content += f"{file_path} ({size} bytes)\n"
            except OSError:
                backup_content += f"{file_path} (size unknown)\n"

    return backup_content


def safe_remove_files(
    files_to_remove: List[str], dry_run: bool = True
) -> Dict[str, Any]:
    """Safely remove files with optional dry run."""

    results = {"removed": [], "failed": [], "total_size_freed": 0}

    for file_path in files_to_remove:
        if not os.path.exists(file_path):
            continue

        try:
            size = os.path.getsize(file_path) if os.path.isfile(file_path) else 0

            if dry_run:
                print(f"[DRY RUN] Would remove: {file_path} ({size} bytes)")
                results["removed"].append(file_path)
                results["total_size_freed"] += size
            else:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

                print(f"Removed: {file_path} ({size} bytes)")
                results["removed"].append(file_path)
                results["total_size_freed"] += size

        except OSError as e:
            print(f"Failed to remove {file_path}: {e}")
            results["failed"].append(file_path)

    return results


def main():
    """Main cleanup function."""

    print("🧹 Starting repository cleanup analysis...")

    # Identify outdated files
    outdated = identify_outdated_files()

    print(f"\n📊 Analysis Results:")
    print(f"   - Old versions: {len(outdated['old_versions'])}")
    print(f"   - Potential duplicates: {len(outdated['potential_duplicates'])}")
    print(f"   - Temporary files: {len(outdated['temporary_files'])}")

    # Analyze file sizes
    large_files = analyze_file_sizes()
    if large_files:
        print(f"\n📈 Large files found:")
        for file_path, size in sorted(
            large_files.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"   - {file_path}: {size / (1024*1024):.1f} MB")

    # Prepare files for removal
    files_to_remove = []
    files_to_remove.extend(outdated["old_versions"])
    files_to_remove.extend(outdated["temporary_files"])

    if files_to_remove:
        print(f"\n🗑️  Files recommended for removal:")
        for file_path in files_to_remove:
            if os.path.exists(file_path):
                print(f"   - {file_path}")

        # Create backup list
        backup_content = create_backup_list(files_to_remove)
        with open("cleanup_backup_list.txt", "w") as f:
            f.write(backup_content)
        print(f"\n💾 Backup list created: cleanup_backup_list.txt")

        # Perform dry run
        print(f"\n🔍 Performing dry run...")
        dry_results = safe_remove_files(files_to_remove, dry_run=True)

        print(f"\n📋 Dry run summary:")
        print(f"   - Files to remove: {len(dry_results['removed'])}")
        print(f"   - Space to free: {dry_results['total_size_freed'] / 1024:.1f} KB")

        # Ask for confirmation (in a real scenario)
        print(f"\n⚠️  To actually remove files, run with --execute flag")
        print(f"   Example: python cleanup_outdated_files.py --execute")

    # Report on potential duplicates that need manual review
    if outdated["potential_duplicates"]:
        print(f"\n🔍 Files requiring manual review:")
        for file_path in outdated["potential_duplicates"]:
            if os.path.exists(file_path):
                print(f"   - {file_path}")
        print(f"   These files should be manually reviewed before removal.")


if __name__ == "__main__":
    import sys

    # Check for execute flag
    execute = "--execute" in sys.argv

    if execute:
        print("⚠️  EXECUTE MODE: Files will be permanently removed!")
        input("Press Enter to continue or Ctrl+C to cancel...")

    main()

    if execute:
        # Actually remove files
        outdated = identify_outdated_files()
        files_to_remove = []
        files_to_remove.extend(outdated["old_versions"])
        files_to_remove.extend(outdated["temporary_files"])

        if files_to_remove:
            print(f"\n🗑️  Executing cleanup...")
            results = safe_remove_files(files_to_remove, dry_run=False)

            print(f"\n✅ Cleanup completed:")
            print(f"   - Files removed: {len(results['removed'])}")
            print(f"   - Failed removals: {len(results['failed'])}")
            print(f"   - Space freed: {results['total_size_freed'] / 1024:.1f} KB")
