import unittest
from labels import normalize

class LabelsTests(unittest.TestCase):
    def test_normalizes_case_and_space(self):
        self.assertEqual(normalize("  Hello  "), "hello")
    def test_empty(self):
        self.assertEqual(normalize("  "), "")

if __name__ == "__main__":
    unittest.main()
