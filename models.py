"""
Data Models Module

Defines core entities: Student, Course, and Enrollment.
Includes validation at initialization and serialization/deserialization logic.
"""

from datetime import datetime
from typing import Dict, Any, Optional
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


class Student:
    """Represents a student enrolled in the institution."""

    def __init__(
        self,
        student_id: str,
        name: str,
        email: str,
        phone: str,
        department: str,
        semester: int = 1,
        created_at: Optional[str] = None,
    ):
        ok, valid_id = validate_student_id(student_id)
        if not ok:
            raise ValueError(f"Invalid Student ID: {valid_id}")

        ok, valid_name = validate_name(name)
        if not ok:
            raise ValueError(f"Invalid Name: {valid_name}")

        ok, valid_email = validate_email(email)
        if not ok:
            raise ValueError(f"Invalid Email: {valid_email}")

        ok, valid_phone = validate_phone(phone)
        if not ok:
            raise ValueError(f"Invalid Phone: {valid_phone}")

        if not department or not department.strip():
            raise ValueError("Department cannot be blank.")

        try:
            sem_int = int(semester)
            if not 1 <= sem_int <= 10:
                raise ValueError("Semester must be between 1 and 10.")
        except (ValueError, TypeError):
            raise ValueError("Semester must be an integer between 1 and 10.")

        self.student_id = valid_id
        self.name = valid_name
        self.email = valid_email
        self.phone = valid_phone
        self.department = department.strip()
        self.semester = sem_int
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "department": self.department,
            "semester": self.semester,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        return cls(
            student_id=data.get("student_id", ""),
            name=data.get("name", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            department=data.get("department", ""),
            semester=data.get("semester", 1),
            created_at=data.get("created_at"),
        )

    def __repr__(self) -> str:
        return f"<Student {self.student_id} - {self.name} ({self.department})>"


class Course:
    """Represents an academic course offering."""

    def __init__(
        self,
        course_code: str,
        title: str,
        credits: int,
        department: str,
        instructor: str = "TBD",
        max_capacity: int = 60,
    ):
        ok, valid_code = validate_course_code(course_code)
        if not ok:
            raise ValueError(f"Invalid Course Code: {valid_code}")

        if not title or len(title.strip()) < 3:
            raise ValueError("Course title must be at least 3 characters.")

        ok, valid_credits = validate_credits(credits)
        if not ok:
            raise ValueError(f"Invalid Credits: {valid_credits}")

        self.course_code = valid_code
        self.title = title.strip()
        self.credits = valid_credits
        self.department = (department or "General").strip()
        self.instructor = (instructor or "TBD").strip()
        self.max_capacity = max(1, int(max_capacity))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "course_code": self.course_code,
            "title": self.title,
            "credits": self.credits,
            "department": self.department,
            "instructor": self.instructor,
            "max_capacity": self.max_capacity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Course":
        return cls(
            course_code=data.get("course_code", ""),
            title=data.get("title", ""),
            credits=data.get("credits", 3),
            department=data.get("department", "General"),
            instructor=data.get("instructor", "TBD"),
            max_capacity=data.get("max_capacity", 60),
        )

    def __repr__(self) -> str:
        return f"<Course {self.course_code}: {self.title} ({self.credits} Credits)>"


class Enrollment:
    """Tracks a student's enrollment, marks, and attendance in a course."""

    def __init__(
        self,
        student_id: str,
        course_code: str,
        attendance_pct: float = 100.0,
        marks: Optional[float] = None,
        status: str = "Enrolled",
        enrolled_on: Optional[str] = None,
    ):
        self.student_id = student_id.strip().upper()
        self.course_code = course_code.strip().upper()
        self.attendance_pct = max(0.0, min(100.0, float(attendance_pct)))
        self.status = status if status in ["Enrolled", "Completed", "Dropped"] else "Enrolled"
        self.enrolled_on = enrolled_on or datetime.now().strftime("%Y-%m-%d")

        self.marks: Optional[float] = None
        self.letter_grade: str = "N/A"
        self.grade_point: int = 0

        if marks is not None:
            self.set_marks(marks)

    def set_marks(self, marks_val: float) -> None:
        """Assigns final percentage and calculates letter grade and points."""
        ok, valid_val = validate_marks(marks_val)
        if not ok:
            raise ValueError(f"Invalid Marks: {valid_val}")
        self.marks = valid_val
        letter, point = marks_to_grade_point(valid_val)
        self.letter_grade = letter
        self.grade_point = point
        self.status = "Completed"

    def set_attendance(self, pct: float) -> None:
        """Updates student attendance percentage."""
        if not 0.0 <= pct <= 100.0:
            raise ValueError("Attendance must be between 0.0 and 100.0%.")
        self.attendance_pct = round(pct, 1)

    @property
    def enrollment_id(self) -> str:
        return f"{self.student_id}_{self.course_code}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "student_id": self.student_id,
            "course_code": self.course_code,
            "attendance_pct": self.attendance_pct,
            "marks": self.marks,
            "letter_grade": self.letter_grade,
            "grade_point": self.grade_point,
            "status": self.status,
            "enrolled_on": self.enrolled_on,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Enrollment":
        enr = cls(
            student_id=data.get("student_id", ""),
            course_code=data.get("course_code", ""),
            attendance_pct=data.get("attendance_pct", 100.0),
            marks=data.get("marks"),
            status=data.get("status", "Enrolled"),
            enrolled_on=data.get("enrolled_on"),
        )
        if data.get("letter_grade"):
            enr.letter_grade = data["letter_grade"]
            enr.grade_point = data.get("grade_point", 0)
        return enr

    def __repr__(self) -> str:
        return f"<Enrollment {self.student_id} in {self.course_code} [{self.status}]>"
