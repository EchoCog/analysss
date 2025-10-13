#!/usr/bin/env python3
"""
Codebase Validation Script
==========================

Runs comprehensive quality checks on the codebase including:
- Linting with flake8
- Code formatting with black
- Import sorting with isort
- Unit tests with pytest
- Optional integration tests

Usage:
    python scripts/validate_codebase.py [--full] [--fix]
    
Arguments:
    --full    Run all tests including integration tests
    --fix     Auto-fix formatting and import issues
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(cmd, description, fix_mode=False):
    """Run a command and report results."""
    print(f"\n{'='*70}")
    print(f"🔍 {description}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        if result.stdout:
            print(result.stdout)
        
        if result.returncode != 0:
            if result.stderr:
                print(result.stderr)
            print(f"❌ {description} FAILED")
            return False
        else:
            print(f"✅ {description} PASSED")
            return True
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False


def main():
    """Main validation function."""
    parser = argparse.ArgumentParser(description='Validate codebase quality')
    parser.add_argument('--full', action='store_true', help='Run integration tests')
    parser.add_argument('--fix', action='store_true', help='Auto-fix formatting issues')
    args = parser.parse_args()
    
    results = {}
    
    print("🚀 Starting Codebase Validation")
    print(f"Repository: {Path.cwd()}")
    
    # 1. Syntax and critical error check with flake8
    results['flake8_critical'] = run_command(
        "flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics",
        "Flake8 - Critical Errors Check"
    )
    
    # 2. Full linting check
    results['flake8_full'] = run_command(
        "flake8 src/ --count --statistics --exit-zero",
        "Flake8 - Full Linting (warnings only)"
    )
    
    # 3. Code formatting check/fix with black
    if args.fix:
        results['black'] = run_command(
            "black src/",
            "Black - Code Formatting (Auto-fix)",
            fix_mode=True
        )
    else:
        results['black'] = run_command(
            "black --check src/",
            "Black - Code Formatting Check"
        )
    
    # 4. Import sorting check/fix with isort
    if args.fix:
        results['isort'] = run_command(
            "isort src/",
            "isort - Import Sorting (Auto-fix)",
            fix_mode=True
        )
    else:
        results['isort'] = run_command(
            "isort --check-only src/",
            "isort - Import Sorting Check"
        )
    
    # 5. Run unit tests
    results['unit_tests'] = run_command(
        "pytest tests/unit/ -v --tb=short",
        "Unit Tests"
    )
    
    # 6. Run integration tests (optional)
    if args.full:
        results['integration_tests'] = run_command(
            "pytest tests/integration/ -v --tb=short",
            "Integration Tests"
        )
    
    # Print summary
    print(f"\n{'='*70}")
    print("📊 VALIDATION SUMMARY")
    print(f"{'='*70}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check, passed_check in results.items():
        status = "✅ PASSED" if passed_check else "❌ FAILED"
        print(f"{check.ljust(30)}: {status}")
    
    print(f"\n{'='*70}")
    print(f"Total: {passed}/{total} checks passed ({passed/total*100:.1f}%)")
    print(f"{'='*70}")
    
    if passed == total:
        print("\n🎉 All validation checks passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} check(s) failed")
        if not args.fix:
            print("💡 Tip: Run with --fix to automatically fix formatting issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())
