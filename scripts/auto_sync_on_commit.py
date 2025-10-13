#!/usr/bin/env python3
"""
Automated Database Sync on Git Commit

This script automatically syncs repository changes to Supabase and Neon
databases when commits are made. Can be used as a git hook or CI/CD step.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.database_sync.real_time_sync import RealTimeDatabaseSync
except ImportError:
    print("Error: Could not import RealTimeDatabaseSync")
    print("Make sure the module is installed: pip install -e .")
    sys.exit(1)


class GitChangeDetector:
    """Detects changes in git repository that require database sync."""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.sync_triggers = {
            "evidence": ["evidence/", ".json", ".md"],
            "entities": ["entities/", "ENTITY", "entity"],
            "timeline": ["timeline", "TIMELINE"],
            "schema": ["database_schema", ".sql", "alembic/versions/"],
        }

    def get_changed_files(self, since_commit: str = "HEAD~1") -> List[str]:
        """
        Get list of changed files since specified commit.

        Args:
            since_commit: Git reference to compare against

        Returns:
            List of changed file paths
        """
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", since_commit, "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip().split("\n") if result.stdout else []
        except subprocess.CalledProcessError as e:
            print(f"Error getting changed files: {e}")
            return []

    def get_untracked_files(self) -> List[str]:
        """Get list of untracked files."""
        try:
            result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip().split("\n") if result.stdout else []
        except subprocess.CalledProcessError as e:
            print(f"Error getting untracked files: {e}")
            return []

    def categorize_changes(self, files: List[str]) -> Dict[str, List[str]]:
        """
        Categorize changed files by sync type.

        Args:
            files: List of file paths

        Returns:
            Dictionary mapping categories to file lists
        """
        categorized = {
            "evidence": [],
            "entities": [],
            "timeline": [],
            "schema": [],
            "other": [],
        }

        for file_path in files:
            if not file_path:
                continue

            categorized_flag = False

            for category, patterns in self.sync_triggers.items():
                if any(pattern in file_path for pattern in patterns):
                    categorized[category].append(file_path)
                    categorized_flag = True
                    break

            if not categorized_flag:
                categorized["other"].append(file_path)

        return categorized

    def requires_sync(self, files: List[str]) -> bool:
        """
        Check if changes require database sync.

        Args:
            files: List of changed file paths

        Returns:
            True if sync is required
        """
        categorized = self.categorize_changes(files)
        return any(
            categorized[cat]
            for cat in ["evidence", "entities", "timeline", "schema"]
        )


class AutoSyncManager:
    """Manages automated database synchronization."""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.detector = GitChangeDetector(repo_path)
        self.sync_client = RealTimeDatabaseSync()
        self.sync_log_path = self.repo_path / "auto_sync_log.json"

    def sync_changed_files(self, files: List[str]) -> Dict[str, any]:
        """
        Sync changed files to databases.

        Args:
            files: List of changed file paths

        Returns:
            Sync results dictionary
        """
        categorized = self.detector.categorize_changes(files)

        results = {
            "timestamp": datetime.now().isoformat(),
            "files_processed": len(files),
            "categories": categorized,
            "sync_results": [],
        }

        # Sync schema changes
        if categorized["schema"]:
            print(f"\n📋 Syncing {len(categorized['schema'])} schema files...")
            for schema_file in categorized["schema"]:
                file_path = self.repo_path / schema_file
                if file_path.exists() and file_path.suffix == ".sql":
                    try:
                        with open(file_path, "r") as f:
                            schema_sql = f.read()
                        sync_result = self.sync_client.sync_schema(schema_sql)
                        results["sync_results"].append(
                            {"file": schema_file, "type": "schema", "result": sync_result}
                        )
                        print(f"  ✓ Synced: {schema_file}")
                    except Exception as e:
                        print(f"  ✗ Failed: {schema_file} - {e}")

        # Sync evidence data
        if categorized["evidence"]:
            print(f"\n📁 Syncing {len(categorized['evidence'])} evidence files...")
            evidence_data = self._load_json_files(categorized["evidence"])
            if evidence_data:
                sync_result = self.sync_client.sync_data("evidence", evidence_data)
                results["sync_results"].append(
                    {"type": "evidence", "records": len(evidence_data), "result": sync_result}
                )

        # Sync entity data
        if categorized["entities"]:
            print(f"\n👥 Syncing {len(categorized['entities'])} entity files...")
            entity_data = self._load_json_files(categorized["entities"])
            if entity_data:
                sync_result = self.sync_client.sync_data("entities", entity_data)
                results["sync_results"].append(
                    {"type": "entities", "records": len(entity_data), "result": sync_result}
                )

        # Sync timeline data
        if categorized["timeline"]:
            print(f"\n📅 Syncing {len(categorized['timeline'])} timeline files...")
            timeline_data = self._load_json_files(categorized["timeline"])
            if timeline_data:
                sync_result = self.sync_client.sync_data("events", timeline_data)
                results["sync_results"].append(
                    {"type": "timeline", "records": len(timeline_data), "result": sync_result}
                )

        self._log_sync(results)
        return results

    def _load_json_files(self, file_paths: List[str]) -> List[Dict]:
        """Load and combine data from JSON files."""
        combined_data = []

        for file_path in file_paths:
            full_path = self.repo_path / file_path
            if full_path.exists() and full_path.suffix == ".json":
                try:
                    with open(full_path, "r") as f:
                        data = json.load(f)
                    if isinstance(data, list):
                        combined_data.extend(data)
                    elif isinstance(data, dict):
                        combined_data.append(data)
                except Exception as e:
                    print(f"  ⚠ Error loading {file_path}: {e}")

        return combined_data

    def _log_sync(self, results: Dict):
        """Log sync results."""
        log_data = []

        if self.sync_log_path.exists():
            with open(self.sync_log_path, "r") as f:
                log_data = json.load(f)

        log_data.append(results)
        log_data = log_data[-50:]  # Keep last 50 entries

        with open(self.sync_log_path, "w") as f:
            json.dump(log_data, f, indent=2)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Automatically sync repository changes to databases"
    )
    parser.add_argument(
        "--since",
        default="HEAD~1",
        help="Git reference to compare against (default: HEAD~1)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be synced without actually syncing",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force sync even if no database-relevant changes detected",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("  Automated Database Sync")
    print("=" * 60)

    # Initialize managers
    detector = GitChangeDetector()
    sync_manager = AutoSyncManager()

    # Get changed files
    changed_files = detector.get_changed_files(args.since)
    untracked_files = detector.get_untracked_files()
    all_files = changed_files + untracked_files

    print(f"\n📊 Detected {len(all_files)} changed/new files")

    # Categorize changes
    categorized = detector.categorize_changes(all_files)

    print("\n📋 Change Summary:")
    for category, files in categorized.items():
        if files:
            print(f"  {category.capitalize()}: {len(files)} files")

    # Check if sync is required
    if not args.force and not detector.requires_sync(all_files):
        print("\n✓ No database-relevant changes detected. Skipping sync.")
        return

    if args.dry_run:
        print("\n🔍 DRY RUN - Would sync the following:")
        for category, files in categorized.items():
            if files and category != "other":
                print(f"\n{category.capitalize()}:")
                for file in files[:5]:  # Show first 5
                    print(f"  - {file}")
                if len(files) > 5:
                    print(f"  ... and {len(files) - 5} more")
        return

    # Perform sync
    print("\n🔄 Starting database synchronization...")
    results = sync_manager.sync_changed_files(all_files)

    # Display results
    print("\n" + "=" * 60)
    print("  Sync Complete")
    print("=" * 60)
    print(f"\nFiles processed: {results['files_processed']}")
    print(f"Sync operations: {len(results['sync_results'])}")

    for sync_result in results["sync_results"]:
        print(f"\n{sync_result.get('type', 'unknown').capitalize()}:")
        result_data = sync_result.get("result", {})
        if "supabase" in result_data:
            print(f"  Supabase: {result_data['supabase'].get('message', 'N/A')}")
        if "neon" in result_data:
            print(f"  Neon: {result_data['neon'].get('message', 'N/A')}")

    print("\n✓ Synchronization completed successfully!")


if __name__ == "__main__":
    main()

