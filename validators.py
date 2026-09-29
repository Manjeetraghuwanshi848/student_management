"""
Input Validation Module

Contains verification utilities for IDs, contact details, academic scores,
and course codes before they enter persistent storage.
"""

import re
from typing import Tuple


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
PHONE_REGEX = re.compile(r"^(\+?\d{1,3}[- ]?)?\d{10}$")
STUDENT_ID_REGEX = re.compile(r"^(STU\d{3,6}|\d{2}[A-Z]{2,4}\d{4,6})$", re.IGNORECASE)
COURSE_CODE_REGEX = re.compile(r"^[A-Z]{2,4}\d{3,4}$", re.IGNORECASE)


def validate_student_id(student_id: str) -> Tuple[bool, str]:
    """Validates student registration ID format (e.g. 26MIM10152 or STU1001)."""
    cleaned = (student_id or "").strip().upper()
    if not cleaned:
        return False, "Student ID cannot be empty."
    if not STUDENT_ID_REGEX.match(cleaned):
        return False, "Student ID must match format like 26MIM10152 or STU1001."
    return True, cleaned


def validate_name(name: str) -> Tuple[bool, str]:
    """Ensures names are non-empty and only contain letters, spaces, and hyphens."""
    cleaned = (name or "").strip()
    if len(cleaned) < 2:
        return False, "Name must be at least 2 characters long."
    if len(cleaned) > 60:
        return False, "Name cannot exceed 60 characters."
    if not re.match(r"^[A-Za-z\s.'-]+$", cleaned):
        return False, "Name contains invalid characters. Only letters, spaces, periods, and hyphens allowed."
    return True, cleaned


def validate_email(email: str) -> Tuple[bool, str]:
    """Checks for standard RFC-compatible email address."""
    cleaned = (email or "").strip().lower()
    if not EMAIL_REGEX.match(cleaned):
        return False, "Invalid email address format (e.g., student@vitstudent.ac.in)."
    return True, cleaned


def validate_phone(phone: str) -> Tuple[bool, str]:
    """Validates 10-digit mobile number with optional country code."""
    cleaned = re.sub(r"[\s\-]", "", (phone or "").strip())
    if not PHONE_REGEX.match(cleaned):
        return False, "Phone number must be a valid 10-digit number."
    return True, cleaned


def validate_course_code(code: str) -> Tuple[bool, str]:
    """Validates course code format (e.g., CSE1001, MAT1001)."""
    cleaned = (code or "").strip().upper()
    if not COURSE_CODE_REGEX.match(cleaned):
        return False, "Course code must have 2-4 letters followed by 3-4 digits (e.g., CSE1001)."
    return True, cleaned


def validate_credits(credits_val: int) -> Tuple[bool, int]:
    """Ensures course credit is within realistic limits (1 to 6)."""
    try:
        val = int(credits_val)
        if 1 <= val <= 6:
            return True, val
        return False, "Credits must be an integer between 1 and 6."
    except (ValueError, TypeError):
        return False, "Credits must be a valid whole number."


def validate_marks(marks_val: float) -> Tuple[bool, float]:
    """Ensures exam score / percentage is between 0.0 and 100.0."""
    try:
        val = round(float(marks_val), 2)
        if 0.0 <= val <= 100.0:
            return True, val
        return False, "Marks must be between 0.0 and 100.0."
    except (ValueError, TypeError):
        return False, "Marks must be a valid numeric value."


def marks_to_grade_point(marks: float) -> Tuple[str, int]:
    """
    Standard university 10-point relative scale conversion.
    Returns (Letter Grade, Grade Point).
    """
    if marks >= 90.0:
        return "S", 10
    elif marks >= 80.0:
        return "A", 9
    elif marks >= 70.0:
        return "B", 8
    elif marks >= 60.0:
        return "C", 7
    elif marks >= 50.0:
        return "D", 6
    elif marks >= 40.0:
        return "E", 5
    else:
        return "F", 0
