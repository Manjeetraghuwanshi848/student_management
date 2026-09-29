"""
Unit Tests for Validators Module
"""
import sys
import unittest
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sms.validators import (
    validate_student_id,
    validate_name,
    validate_email,
    validate_phone,
    validate_course_code,
    validate_credits,
    validate_marks,
    marks_to_grade_point,
)


class TestValidators(unittest.TestCase):

    def test_valid_student_id(self):
        ok, sid = validate_student_id("STU1001")
        self.assertTrue(ok)
        self.assertEqual(sid, "STU1001")

        ok, reg = validate_student_id("24BCE1024")
        self.assertTrue(ok)
        self.assertEqual(reg, "24BCE1024")

        ok, reg2 = validate_student_id("26MIM10152")
        self.assertTrue(ok)
        self.assertEqual(reg2, "26MIM10152")

    def test_invalid_student_id(self):
        ok, msg = validate_student_id("")
        self.assertFalse(ok)

        ok, msg = validate_student_id("abc")
        self.assertFalse(ok)

    def test_valid_name(self):
        ok, name = validate_name("Manjeet Raghuvanshi")
        self.assertTrue(ok)
        self.assertEqual(name, "Manjeet Raghuvanshi")

    def test_invalid_name(self):
        ok, _ = validate_name("A")
        self.assertFalse(ok)

        ok, _ = validate_name("John123")
        self.assertFalse(ok)

    def test_valid_email(self):
        ok, email = validate_email("manjeet@vitstudent.ac.in")
        self.assertTrue(ok)
        self.assertEqual(email, "manjeet@vitstudent.ac.in")

    def test_invalid_email(self):
        ok, _ = validate_email("invalid-email-address")
        self.assertFalse(ok)

        ok, _ = validate_email("@vitstudent.ac.in")
        self.assertFalse(ok)

    def test_phone_validation(self):
        ok, phone = validate_phone("9876543210")
        self.assertTrue(ok)
        self.assertEqual(phone, "9876543210")

        ok, phone_with_code = validate_phone("+91-9876543210")
        self.assertTrue(ok)

        ok, bad_phone = validate_phone("12345")
        self.assertFalse(ok)

    def test_course_code(self):
        ok, code = validate_course_code("CSE1001")
        self.assertTrue(ok)
        self.assertEqual(code, "CSE1001")

        ok, _ = validate_course_code("1001CSE")
        self.assertFalse(ok)

    def test_credits_boundaries(self):
        self.assertTrue(validate_credits(3)[0])
        self.assertFalse(validate_credits(0)[0])
        self.assertFalse(validate_credits(8)[0])
        self.assertFalse(validate_credits("abc")[0])

    def test_marks_and_grade_points(self):
        self.assertEqual(marks_to_grade_point(95.0), ("S", 10))
        self.assertEqual(marks_to_grade_point(85.0), ("A", 9))
        self.assertEqual(marks_to_grade_point(72.5), ("B", 8))
        self.assertEqual(marks_to_grade_point(61.0), ("C", 7))
        self.assertEqual(marks_to_grade_point(50.0), ("D", 6))
        self.assertEqual(marks_to_grade_point(41.0), ("E", 5))
        self.assertEqual(marks_to_grade_point(35.0), ("F", 0))


if __name__ == "__main__":
    unittest.main()
