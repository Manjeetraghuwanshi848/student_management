"""
Unit Tests for Storage Persistence Layer
"""

import sys
import unittest
import tempfile
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sms.storage import StorageManager


class TestStorageManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = StorageManager(data_dir=Path(self.temp_dir.name))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load_students(self):
        data = [{"student_id": "26MIM10152", "name": "Manjeet Raghuvanshi", "email": "manjeet@vitstudent.ac.in"}]
        self.storage.save_students(data)
        loaded = self.storage.load_students()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["student_id"], "26MIM10152")

    def test_corrupted_json_recovery(self):
        with open(self.storage.students_file, "w", encoding="utf-8") as f:
            f.write("{ invalid json content ...")

        loaded = self.storage.load_students()
        self.assertEqual(loaded, [])


if __name__ == "__main__":
    unittest.main()
