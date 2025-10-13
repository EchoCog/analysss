#!/usr/bin/env python3
"""
Unit tests for emoji syntax validation.

Tests the validate_emoji_syntax.py script to ensure it correctly
identifies emoji syntax issues in Python code.
"""

import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path to import the validator
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.validate_emoji_syntax import (
    check_file_syntax,
    detect_potential_emoji_issues,
)


class TestEmojiValidation(unittest.TestCase):
    """Test emoji syntax validation functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_valid_emoji_in_string(self):
        """Test that properly quoted emojis pass validation"""
        test_code = '''#!/usr/bin/env python3
print("🚀 Starting application")
print('✅ Success')
message = f"🔍 Searching for {item}"
'''
        test_file = self.temp_path / "test_valid.py"
        test_file.write_text(test_code)

        is_valid, errors = check_file_syntax(test_file)
        self.assertTrue(is_valid, f"Valid code flagged as invalid: {errors}")
        self.assertEqual(len(errors), 0)

    def test_emoji_in_comments(self):
        """Test that emojis in comments are allowed"""
        test_code = '''#!/usr/bin/env python3
# 🚀 This function launches the app
def launch():
    """Launch the application 🚀"""
    print("Starting...")  # ✅ Good practice
'''
        test_file = self.temp_path / "test_comments.py"
        test_file.write_text(test_code)

        is_valid, errors = check_file_syntax(test_file)
        self.assertTrue(is_valid)

    def test_emoji_in_docstring(self):
        """Test that emojis in docstrings are allowed"""
        test_code = '''#!/usr/bin/env python3
def example():
    """
    Example function 🚀
    
    Returns:
        str: Success message ✅
    """
    return "Done"
'''
        test_file = self.temp_path / "test_docstring.py"
        test_file.write_text(test_code)

        is_valid, errors = check_file_syntax(test_file)
        self.assertTrue(is_valid)

    def test_emoji_in_fstring(self):
        """Test that emojis in f-strings work correctly"""
        test_code = '''#!/usr/bin/env python3
status = "ready"
message = f"🚀 Status: {status}"
print(f"✅ {message}")
'''
        test_file = self.temp_path / "test_fstring.py"
        test_file.write_text(test_code)

        is_valid, errors = check_file_syntax(test_file)
        self.assertTrue(is_valid)

    def test_emoji_in_multiline_string(self):
        """Test that emojis in multiline strings work"""
        test_code = '''#!/usr/bin/env python3
message = """
🚀 Starting process
✅ Step 1 complete
✅ Step 2 complete
"""
print(message)
'''
        test_file = self.temp_path / "test_multiline.py"
        test_file.write_text(test_code)

        is_valid, errors = check_file_syntax(test_file)
        self.assertTrue(is_valid)

    def test_emoji_in_variable_assignment(self):
        """Test emojis in various assignment contexts"""
        test_code = '''#!/usr/bin/env python3
rocket = "🚀"
success = '✅'
messages = {
    "start": "🚀 Starting",
    "done": "✅ Complete"
}
emoji_list = ["🚀", "✅", "🔍"]
'''
        test_file = self.temp_path / "test_assignment.py"
        test_file.write_text(test_code)

        is_valid, errors = check_file_syntax(test_file)
        self.assertTrue(is_valid)

    def test_emoji_in_dictionary(self):
        """Test emojis as dictionary values"""
        test_code = '''#!/usr/bin/env python3
status_icons = {
    "running": "🚀",
    "success": "✅",
    "error": "❌",
    "warning": "⚠️"
}
print(status_icons["running"])
'''
        test_file = self.temp_path / "test_dict.py"
        test_file.write_text(test_code)

        is_valid, errors = check_file_syntax(test_file)
        self.assertTrue(is_valid)

    def test_emoji_in_list_comprehension(self):
        """Test emojis in list comprehension"""
        test_code = '''#!/usr/bin/env python3
emojis = ["🚀", "✅", "❌"]
prefixed = [f"{e} Item" for e in emojis]
'''
        test_file = self.temp_path / "test_comprehension.py"
        test_file.write_text(test_code)

        is_valid, errors = check_file_syntax(test_file)
        self.assertTrue(is_valid)

    def test_emoji_in_format_string(self):
        """Test emojis in .format() strings"""
        test_code = '''#!/usr/bin/env python3
message = "🚀 Status: {}".format("ready")
print("✅ {} complete".format("Task"))
'''
        test_file = self.temp_path / "test_format.py"
        test_file.write_text(test_code)

        is_valid, errors = check_file_syntax(test_file)
        self.assertTrue(is_valid)

    def test_emoji_in_class_attribute(self):
        """Test emojis as class attributes"""
        test_code = '''#!/usr/bin/env python3
class Status:
    RUNNING = "🚀"
    SUCCESS = "✅"
    ERROR = "❌"
    
    def __init__(self):
        self.icon = "🔍"
'''
        test_file = self.temp_path / "test_class.py"
        test_file.write_text(test_code)

        is_valid, errors = check_file_syntax(test_file)
        self.assertTrue(is_valid)

    def test_multiple_emojis_in_string(self):
        """Test multiple emojis in a single string"""
        test_code = '''#!/usr/bin/env python3
print("🚀 Starting ✅ Ready 🔍 Searching")
message = "Status: 🚀 ➡️ ✅"
'''
        test_file = self.temp_path / "test_multiple.py"
        test_file.write_text(test_code)

        is_valid, errors = check_file_syntax(test_file)
        self.assertTrue(is_valid)

    def test_emoji_concatenation(self):
        """Test emoji string concatenation"""
        test_code = '''#!/usr/bin/env python3
prefix = "🚀"
suffix = "✅"
message = prefix + " Status " + suffix
'''
        test_file = self.temp_path / "test_concat.py"
        test_file.write_text(test_code)

        is_valid, errors = check_file_syntax(test_file)
        self.assertTrue(is_valid)

    def test_no_false_positives(self):
        """Test that code without emojis passes"""
        test_code = '''#!/usr/bin/env python3
def hello():
    print("Hello, World!")
    return "Success"

if __name__ == "__main__":
    hello()
'''
        test_file = self.temp_path / "test_no_emoji.py"
        test_file.write_text(test_code)

        is_valid, errors = check_file_syntax(test_file)
        self.assertTrue(is_valid)
        
        issues = detect_potential_emoji_issues(test_file)
        self.assertEqual(len(issues), 0, "No issues should be found in emoji-free code")


class TestEmojiUsageBestPractices(unittest.TestCase):
    """Test best practices for emoji usage"""

    def test_emoji_string_examples(self):
        """Test that documented examples work correctly"""
        # These are the recommended patterns from the documentation
        examples = [
            'print("🚀")',
            "print('🚀')",
            'print(f"🚀 {variable}")',
            'print("🚀 Launching {}".format("app"))',
        ]

        for example in examples:
            with self.subTest(example=example):
                try:
                    compile(example, '<string>', 'exec')
                    success = True
                except SyntaxError:
                    success = False
                
                self.assertTrue(success, f"Example should compile: {example}")


class TestEmojiValidatorOutput(unittest.TestCase):
    """Test the validator produces correct output"""

    def test_validator_returns_correct_format(self):
        """Test that validator returns expected data structure"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('print("🚀 Test")\n')
            temp_file = Path(f.name)

        try:
            is_valid, errors = check_file_syntax(temp_file)
            self.assertIsInstance(is_valid, bool)
            self.assertIsInstance(errors, list)
            self.assertTrue(is_valid)
        finally:
            temp_file.unlink()

    def test_detect_issues_returns_correct_format(self):
        """Test that issue detection returns expected format"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('print("🚀 Test")\n')
            temp_file = Path(f.name)

        try:
            issues = detect_potential_emoji_issues(temp_file)
            self.assertIsInstance(issues, list)
            for issue in issues:
                self.assertIsInstance(issue, tuple)
                self.assertEqual(len(issue), 2)
                self.assertIsInstance(issue[0], int)  # line number
                self.assertIsInstance(issue[1], str)  # description
        finally:
            temp_file.unlink()


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == "__main__":
    run_tests()
