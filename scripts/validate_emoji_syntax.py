#!/usr/bin/env python3
"""
Emoji Syntax Validator
======================

Validates that all emoji characters in Python code are properly quoted strings
and not bare Unicode literals that would cause SyntaxError.

This script prevents issues like:
  ❌ print with bare emoji    # SyntaxError: invalid character (U+1F680)
  ✅ print("🚀")              # Correct usage
  ✅ print('🚀')              # Correct usage
"""

import ast
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple


# Common emoji characters used in the codebase
COMMON_EMOJIS = [
    '🚀', '🚨', '💰', '📈', '🎯', '🔍', '⚖️', '💸', '📊', '📄',
    '✅', '❌', '⚠️', '🔧', '📅', '🕸️', '👥', '🔗', '💾', '🤖',
    '🎉', 'ℹ️'
]


def check_file_syntax(filepath: Path) -> Tuple[bool, List[str]]:
    """
    Check if a Python file has valid syntax.
    
    Args:
        filepath: Path to the Python file
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    try:
        with open(filepath, 'rb') as f:
            code = f.read()
        compile(code, str(filepath), 'exec')
        return True, []
    except SyntaxError as e:
        # Check if it's an emoji-related error
        if any(emoji in str(e) for emoji in COMMON_EMOJIS) or 'U+1F' in str(e):
            return False, [f"Emoji syntax error at line {e.lineno}: {e.msg}"]
        return False, [f"Syntax error at line {e.lineno}: {e.msg}"]
    except Exception as e:
        return False, [f"Unexpected error: {str(e)}"]


def detect_potential_emoji_issues(filepath: Path) -> List[Tuple[int, str]]:
    """
    Detect potential emoji usage issues using heuristics.
    
    This catches issues that might not be syntax errors but could be problematic.
    
    Args:
        filepath: Path to the Python file
        
    Returns:
        List of (line_number, issue_description) tuples
    """
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Skip comments and docstrings
            stripped = line.strip()
            if stripped.startswith('#'):
                continue
            
            # Check for emoji characters
            for emoji in COMMON_EMOJIS:
                if emoji not in line:
                    continue
                
                # Check if emoji appears in suspicious contexts
                # 1. After 'print(' and before ')'
                print_pattern = r'print\([^"\'].*?' + re.escape(emoji)
                if re.search(print_pattern, line):
                    # Check if it's in a string
                    parts_before = line.split(emoji)[0]
                    # Count quotes before emoji
                    single_q = parts_before.count("'") - parts_before.count("\\'")
                    double_q = parts_before.count('"') - parts_before.count('\\"')
                    f_string = parts_before.count('f"') + parts_before.count("f'")
                    
                    # If even number of quotes and no f-string, might be bare
                    in_string = (single_q % 2 == 1) or (double_q % 2 == 1)
                    
                    if not in_string and 'print(' in parts_before:
                        issues.append((
                            i,
                            f"Potential bare emoji '{emoji}' in print statement. "
                            f"Ensure it's wrapped in quotes: print(\"{emoji}\")"
                        ))
        
    except Exception as e:
        issues.append((0, f"Error reading file: {str(e)}"))
    
    return issues


def validate_directory(directory: Path, exclude_dirs: List[str] = None) -> Tuple[int, int, List[Tuple[Path, List]]]:
    """
    Validate all Python files in a directory.
    
    Args:
        directory: Root directory to scan
        exclude_dirs: List of directory names to exclude
        
    Returns:
        Tuple of (files_checked, files_with_issues, issues_by_file)
    """
    if exclude_dirs is None:
        exclude_dirs = ['node_modules', '.git', '__pycache__', 'venv', '.venv', '.tox']
    
    files_checked = 0
    files_with_issues = 0
    issues_by_file = []
    
    for root, dirs, files in os.walk(directory):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if not file.endswith('.py'):
                continue
            
            filepath = Path(root) / file
            files_checked += 1
            
            # First, check syntax
            is_valid, syntax_errors = check_file_syntax(filepath)
            
            if not is_valid:
                files_with_issues += 1
                issues_by_file.append((filepath, syntax_errors))
                continue
            
            # Then check for potential issues
            potential_issues = detect_potential_emoji_issues(filepath)
            
            if potential_issues:
                files_with_issues += 1
                formatted_issues = [f"Line {line}: {msg}" for line, msg in potential_issues]
                issues_by_file.append((filepath, formatted_issues))
    
    return files_checked, files_with_issues, issues_by_file


def main():
    """Main validation function"""
    print("🔍 Emoji Syntax Validator")
    print("=" * 60)
    
    # Get repository root
    repo_root = Path(__file__).parent.parent
    
    print(f"📁 Scanning: {repo_root}")
    print()
    
    # Validate all Python files
    files_checked, files_with_issues, issues = validate_directory(repo_root)
    
    print(f"✅ Files checked: {files_checked}")
    print(f"{'⚠️' if files_with_issues > 0 else '✅'} Files with issues: {files_with_issues}")
    print()
    
    if issues:
        print("=" * 60)
        print("ISSUES FOUND:")
        print("=" * 60)
        
        for filepath, file_issues in issues:
            rel_path = filepath.relative_to(repo_root)
            print(f"\n📄 {rel_path}")
            for issue in file_issues:
                print(f"   {issue}")
        
        print()
        print("=" * 60)
        print("RESOLUTION:")
        print("=" * 60)
        print()
        print("To fix emoji syntax errors:")
        print("  1. Find the bare emoji character (e.g., print(🚀))")
        print("  2. Wrap it in quotes (e.g., print(\"🚀\"))")
        print()
        print("Examples:")
        print("  ❌ print(🚀)           # SyntaxError")
        print("  ✅ print(\"🚀\")         # Correct")
        print("  ✅ print('🚀')         # Correct")
        print("  ✅ print(f\"🚀 {var}\")  # Correct in f-string")
        print()
        
        return 1
    else:
        print("=" * 60)
        print("✅ SUCCESS: No emoji syntax issues found!")
        print("=" * 60)
        print()
        print("All emoji characters are properly quoted in strings.")
        print("Your Python code should execute without emoji-related syntax errors.")
        print()
        
        return 0


if __name__ == "__main__":
    sys.exit(main())
