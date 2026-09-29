"""
Unit Tests for Service Layer and Academic Business Logic
"""

import sys
import unittest
import tempfile
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sms.storage import StorageManager
from sms.services import StudentManagementService


class TestStudentManagementService(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = StorageManager(data_dir=Path(self.temp_dir.name))
        self.service = StudentManagementService(storage=self.storage)

        self.service.add_student("26MIM10152", "Manjeet Raghuvanshi", "manjeet@vitstudent.ac.in", "9876543202", "Computer Science", 3)
        self.service.add_course("CSE1001", "Python Programming", 4, "Computer Science", "Dr. A. Raman", 2)
        self.service.add_course("MAT1001", "Calculus", 3, "Mathematics", "Dr. Banerjee", 60)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_duplicate_student_id_rejected(self):
        with self.assertRaises(ValueError):
            self.service.add_student("26MIM10152", "Duplicate Guy", "dup@vitstudent.ac.in", "9876543219", "CS")

    def test_duplicate_email_rejected(self):
        with self.assertRaises(ValueError):
            self.service.add_student("26MIM10153", "Other Person", "manjeet@vitstudent.ac.in", "9876543218", "CS")

    def test_enrollment_and_gpa_calculation(self):
        self.service.enroll_student("26MIM10152", "CSE1001")
        self.service.enroll_student("26MIM10152", "MAT1001")

        self.service.record_grade("26MIM10152", "CSE1001", 95.0)
        self.service.record_grade("26MIM10152", "MAT1001", 85.0)

        transcript = self.service.generate_transcript("26MIM10152")
        self.assertEqual(transcript["total_registered_credits"], 7)
        self.assertEqual(transcript["total_earned_credits"], 7)
        self.assertEqual(transcript["cgpa"], 9.57)

    def test_course_capacity_enforcement(self):
        self.service.enroll_student("26MIM10152", "CSE1001")

        self.service.add_student("STU1002", "Second Student", "second@campus.edu", "9876543211", "CS")
        self.service.enroll_student("STU1002", "CSE1001")

        self.service.add_student("STU1003", "Third Student", "third@campus.edu", "9876543212", "CS")
        with self.assertRaises(ValueError):
            self.service.enroll_student("STU1003", "CSE1001")

    def test_drop_course(self):
        self.service.enroll_student("26MIM10152", "MAT1001")
        self.assertTrue(self.service.drop_course("26MIM10152", "MAT1001"))
        enr = self.service.get_enrollment("26MIM10152", "MAT1001")
        self.assertEqual(enr.status, "Dropped")


if __name__ == "__main__":
    unittest.main()
