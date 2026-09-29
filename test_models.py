"""
Unit Tests for Data Models
"""

import sys
import unittest
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sms.models import Student, Course, Enrollment


class TestModels(unittest.TestCase):

    def test_student_creation_and_dict(self):
        s = Student(
            student_id="26MIM10152",
            name="Manjeet Raghuvanshi",
            email="manjeet@vitstudent.ac.in",
            phone="9876543202",
            department="Integrated M.Tech Software Engineering",
            semester=3,
        )
        self.assertEqual(s.student_id, "26MIM10152")
        self.assertEqual(s.semester, 3)

        d = s.to_dict()
        self.assertEqual(d["name"], "Manjeet Raghuvanshi")

        restored = Student.from_dict(d)
        self.assertEqual(restored.student_id, s.student_id)
        self.assertEqual(restored.email, s.email)

    def test_student_invalid_creation(self):
        with self.assertRaises(ValueError):
            Student("INVALID_ID", "Name", "email@mail.com", "9876543210", "CS")

        with self.assertRaises(ValueError):
            Student("STU2002", "", "email@mail.com", "9876543210", "CS")

    def test_course_creation_and_dict(self):
        c = Course(
            course_code="CSE3001",
            title="Database Systems",
            credits=4,
            department="Computer Science",
            instructor="Dr. Rao",
            max_capacity=55,
        )
        self.assertEqual(c.course_code, "CSE3001")
        self.assertEqual(c.credits, 4)

        d = c.to_dict()
        restored = Course.from_dict(d)
        self.assertEqual(restored.title, "Database Systems")

    def test_enrollment_lifecycle(self):
        enr = Enrollment(student_id="26MIM10152", course_code="CSE3001")
        self.assertEqual(enr.status, "Enrolled")
        self.assertEqual(enr.letter_grade, "N/A")

        enr.set_marks(87.5)
        self.assertEqual(enr.status, "Completed")
        self.assertEqual(enr.letter_grade, "A")
        self.assertEqual(enr.grade_point, 9)

        enr.set_attendance(85.0)
        self.assertEqual(enr.attendance_pct, 85.0)


if __name__ == "__main__":
    unittest.main()
