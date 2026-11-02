"""
test_app.py
-----------
Verification script to run all required test cases for the Language Translator project.
Ensures real translation accuracy and robust error handling.
"""

import sys
import unittest

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from translator import translate_text, get_available_languages


class TestLanguageTranslator(unittest.TestCase):

    def test_languages_retrieval(self):
        """Verify that supported languages are loaded dynamically."""
        languages = get_available_languages()
        self.assertIsInstance(languages, list)
        self.assertGreater(len(languages), 10)
        self.assertIn("English", languages)
        self.assertIn("Hindi", languages)
        self.assertIn("French", languages)
        self.assertIn("Spanish", languages)
        print(f"[PASS] Supported Languages fetched: {len(languages)} languages available.")

    def test_1_english_to_hindi(self):
        """Test 1: English -> Hindi ('Good morning, how are you?')"""
        text = "Good morning, how are you?"
        result = translate_text(text, "English", "Hindi")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        # Verify result contains Devanagari characters
        has_devanagari = any('\u0900' <= char <= '\u097F' for char in result)
        self.assertTrue(has_devanagari, f"Expected Hindi output, got: {result}")
        print(f"[PASS] Test 1 (English -> Hindi):\n  Input:  '{text}'\n  Output: '{result}'")

    def test_2_english_to_french(self):
        """Test 2: English -> French ('Welcome to my project.')"""
        text = "Welcome to my project."
        result = translate_text(text, "English", "French")
        self.assertIsInstance(result, str)
        self.assertTrue("bienvenue" in result.lower() or "projet" in result.lower())
        print(f"[PASS] Test 2 (English -> French):\n  Input:  '{text}'\n  Output: '{result}'")

    def test_3_english_to_spanish(self):
        """Test 3: English -> Spanish ('I am learning Python.')"""
        text = "I am learning Python."
        result = translate_text(text, "English", "Spanish")
        self.assertIsInstance(result, str)
        self.assertTrue("aprendiendo" in result.lower() or "python" in result.lower())
        print(f"[PASS] Test 3 (English -> Spanish):\n  Input:  '{text}'\n  Output: '{result}'")

    def test_4_empty_input(self):
        """Test 4: Empty input validation"""
        result = translate_text("", "English", "Hindi")
        self.assertEqual(result, "Please enter some text to translate.")
        whitespace_result = translate_text("    ", "English", "Hindi")
        self.assertEqual(whitespace_result, "Please enter some text to translate.")
        print(f"[PASS] Test 4 (Empty input):\n  Output: '{result}'")

    def test_5_same_language(self):
        """Test 5: Same source and target language"""
        text = "This text should not break."
        result = translate_text(text, "English", "English")
        self.assertIn("identical", result)
        self.assertIn(text, result)
        print(f"[PASS] Test 5 (Same language):\n  Output: '{result}'")

    def test_6_auto_detect(self):
        """Test 6: Auto detection functionality"""
        text = "Bonjour tout le monde"
        result = translate_text(text, "Auto Detect", "English")
        self.assertIn("hello", result.lower())
        print(f"[PASS] Test 6 (Auto Detect French -> English):\n  Input:  '{text}'\n  Output: '{result}'")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 Running Language Translator Automated Test Suite")
    print("=" * 60 + "\n")
    unittest.main()
