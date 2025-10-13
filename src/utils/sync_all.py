#!/usr/bin/env python3
"""
Master Synchronization Script
=============================

This script runs both the Supabase and Neon synchronization scripts in sequence.
"""

import logging
import subprocess
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_script(script_name: str) -> bool:
    """Run a Python script and return its success status."""
    try:
        logging.info(f"Running {script_name}...")
        result = subprocess.run(
            [sys.executable, script_name], check=True, capture_output=True, text=True
        )
        logging.info(f"{script_name} completed successfully.")
        logging.debug(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"{script_name} failed.")
        logging.error(e.stderr)
        return False


def main():
    """Main function to run all synchronization scripts."""
    logging.info("Starting all database synchronizations...")

    supabase_success = run_script("analysis/supabase_sync_v2.py")
    if not supabase_success:
        logging.error("Supabase synchronization failed. Aborting.")
        sys.exit(1)

    neon_success = run_script("analysis/neon_sync_v2.py")
    if not neon_success:
        logging.error("Neon synchronization failed.")
        sys.exit(1)

    logging.info("All database synchronizations completed successfully.")


if __name__ == "__main__":
    main()
