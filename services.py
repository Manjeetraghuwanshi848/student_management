"""
Business Logic & Service Layer

Coordinates interactions between data models and storage persistence.
Enforces business rules such as capacity limits, unique IDs, GPA calculations,
and transcript generation.
"""

from typing import List, Dict, Any, Optional
from sms.models import Student, Course, Enrollment
from sms.storage import StorageManager


class StudentManagementService:
    """Core service orchestrating business rules and database mutations."""

    def __init__(self, storage: Optional[StorageManager] = None):
        self.storage = storage or StorageManager()

    # -------------------------------------------------------------
    # Student Operations
    # -------------------------------------------------------------
    def get_all_students(self) -> List[Student]:
        raw = self.storage.load_students()
        return [Student.from_dict(item) for item in raw]

    def get_student(self, student_id: str) -> Optional[Student]:
        cleaned_id = student_id.strip().upper()
        for s in self.get_all_students():
            if s.student_id == cleaned_id:
                return s
        return None

    def add_student(
        self,
        student_id: str,
        name: str,
        email: str,
        phone: str,
        department: str,
        semester: int = 1,
    ) -> Student:
        student = Student(student_id, name, email, phone, department, semester)

        all_students = self.get_all_students()
        for existing in all_students:
            if existing.student_id == student.student_id:
                raise ValueError(f"Student with ID '{student.student_id}' already exists.")
            if existing.email.lower() == student.email.lower():
                raise ValueError(f"Email '{student.email}' is already registered to another student.")

        all_students.append(student)
        self.storage.save_students([s.to_dict() for s in all_students])
        return student

    def update_student(
        self,
        student_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        department: Optional[str] = None,
        semester: Optional[int] = None,
    ) -> Student:
        student = self.get_student(student_id)
        if not student:
            raise KeyError(f"Student with ID '{student_id}' not found.")

        all_students = self.get_all_students()

        if email and email.lower() != student.email.lower():
            for other in all_students:
                if other.student_id != student.student_id and other.email.lower() == email.lower():
                    raise ValueError(f"Email '{email}' is already in use by another student.")

        updated_student = Student(
            student_id=student.student_id,
            name=name if name is not None else student.name,
            email=email if email is not None else student.email,
            phone=phone if phone is not None else student.phone,
            department=department if department is not None else student.department,
            semester=semester if semester is not None else student.semester,
            created_at=student.created_at,
        )

        persisted = []
        for s in all_students:
            if s.student_id == updated_student.student_id:
                persisted.append(updated_student.to_dict())
            else:
                persisted.append(s.to_dict())

        self.storage.save_students(persisted)
        return updated_student

    def delete_student(self, student_id: str) -> bool:
        cleaned_id = student_id.strip().upper()
        all_students = self.get_all_students()
        remaining = [s for s in all_students if s.student_id != cleaned_id]

        if len(remaining) == len(all_students):
            raise KeyError(f"Student with ID '{cleaned_id}' not found.")

        all_enr = self.get_all_enrollments()
        kept_enr = [e for e in all_enr if e.student_id != cleaned_id]

        self.storage.save_students([s.to_dict() for s in remaining])
        self.storage.save_enrollments([e.to_dict() for e in kept_enr])
        return True

    def search_students(self, keyword: str) -> List[Student]:
        """Case-insensitive search matching ID, name, or department."""
        kw = keyword.strip().lower()
        if not kw:
            return self.get_all_students()
        return [
            s
            for s in self.get_all_students()
            if kw in s.student_id.lower() or kw in s.name.lower() or kw in s.department.lower()
        ]

    # -------------------------------------------------------------
    # Course Operations
    # -------------------------------------------------------------
    def get_all_courses(self) -> List[Course]:
        raw = self.storage.load_courses()
        return [Course.from_dict(item) for item in raw]

    def get_course(self, course_code: str) -> Optional[Course]:
        cleaned_code = course_code.strip().upper()
        for c in self.get_all_courses():
            if c.course_code == cleaned_code:
                return c
        return None

    def add_course(
        self,
        course_code: str,
        title: str,
        credits: int,
        department: str,
        instructor: str = "TBD",
        max_capacity: int = 60,
    ) -> Course:
        course = Course(course_code, title, credits, department, instructor, max_capacity)

        all_courses = self.get_all_courses()
        for existing in all_courses:
            if existing.course_code == course.course_code:
                raise ValueError(f"Course '{course.course_code}' is already registered.")

        all_courses.append(course)
        self.storage.save_courses([c.to_dict() for c in all_courses])
        return course

    def update_course(
        self,
        course_code: str,
        title: Optional[str] = None,
        credits: Optional[int] = None,
        department: Optional[str] = None,
        instructor: Optional[str] = None,
        max_capacity: Optional[int] = None,
    ) -> Course:
        course = self.get_course(course_code)
        if not course:
            raise KeyError(f"Course '{course_code}' not found.")

        updated_course = Course(
            course_code=course.course_code,
            title=title if title is not None else course.title,
            credits=credits if credits is not None else course.credits,
            department=department if department is not None else course.department,
            instructor=instructor if instructor is not None else course.instructor,
            max_capacity=max_capacity if max_capacity is not None else course.max_capacity,
        )

        all_courses = self.get_all_courses()
        persisted = []
        for c in all_courses:
            if c.course_code == updated_course.course_code:
                persisted.append(updated_course.to_dict())
            else:
                persisted.append(c.to_dict())

        self.storage.save_courses(persisted)
        return updated_course

    def delete_course(self, course_code: str) -> bool:
        cleaned_code = course_code.strip().upper()
        all_courses = self.get_all_courses()
        remaining = [c for c in all_courses if c.course_code != cleaned_code]

        if len(remaining) == len(all_courses):
            raise KeyError(f"Course '{cleaned_code}' not found.")

        all_enr = self.get_all_enrollments()
        kept_enr = [e for e in all_enr if e.course_code != cleaned_code]

        self.storage.save_courses([c.to_dict() for c in remaining])
        self.storage.save_enrollments([e.to_dict() for e in kept_enr])
        return True

    # -------------------------------------------------------------
    # Enrollment & Academic Operations
    # -------------------------------------------------------------
    def get_all_enrollments(self) -> List[Enrollment]:
        raw = self.storage.load_enrollments()
        return [Enrollment.from_dict(item) for item in raw]

    def get_enrollment(self, student_id: str, course_code: str) -> Optional[Enrollment]:
        sid = student_id.strip().upper()
        ccode = course_code.strip().upper()
        for e in self.get_all_enrollments():
            if e.student_id == sid and e.course_code == ccode:
                return e
        return None

    def enroll_student(self, student_id: str, course_code: str) -> Enrollment:
        sid = student_id.strip().upper()
        ccode = course_code.strip().upper()

        student = self.get_student(sid)
        if not student:
            raise KeyError(f"Cannot enroll: Student '{sid}' does not exist.")

        course = self.get_course(ccode)
        if not course:
            raise KeyError(f"Cannot enroll: Course '{ccode}' does not exist.")

        all_enr = self.get_all_enrollments()

        for e in all_enr:
            if e.student_id == sid and e.course_code == ccode:
                if e.status == "Dropped":
                    e.status = "Enrolled"
                    self.storage.save_enrollments([x.to_dict() for x in all_enr])
                    return e
                raise ValueError(f"Student '{sid}' is already enrolled in '{ccode}'.")

        active_in_course = sum(1 for e in all_enr if e.course_code == ccode and e.status in ["Enrolled", "Completed"])
        if active_in_course >= course.max_capacity:
            raise ValueError(f"Course '{ccode}' has reached its maximum capacity of {course.max_capacity}.")

        new_enr = Enrollment(student_id=sid, course_code=ccode)
        all_enr.append(new_enr)
        self.storage.save_enrollments([e.to_dict() for e in all_enr])
        return new_enr

    def record_grade(self, student_id: str, course_code: str, marks: float) -> Enrollment:
        sid = student_id.strip().upper()
        ccode = course_code.strip().upper()

        all_enr = self.get_all_enrollments()
        target = None
        for e in all_enr:
            if e.student_id == sid and e.course_code == ccode:
                target = e
                break

        if not target:
            raise KeyError(f"No active enrollment found for {sid} in course {ccode}.")

        target.set_marks(marks)
        self.storage.save_enrollments([e.to_dict() for e in all_enr])
        return target

    def record_attendance(self, student_id: str, course_code: str, attendance_pct: float) -> Enrollment:
        sid = student_id.strip().upper()
        ccode = course_code.strip().upper()

        all_enr = self.get_all_enrollments()
        target = None
        for e in all_enr:
            if e.student_id == sid and e.course_code == ccode:
                target = e
                break

        if not target:
            raise KeyError(f"No active enrollment found for {sid} in course {ccode}.")

        target.set_attendance(attendance_pct)
        self.storage.save_enrollments([e.to_dict() for e in all_enr])
        return target

    def drop_course(self, student_id: str, course_code: str) -> bool:
        sid = student_id.strip().upper()
        ccode = course_code.strip().upper()

        all_enr = self.get_all_enrollments()
        found = False
        for e in all_enr:
            if e.student_id == sid and e.course_code == ccode:
                e.status = "Dropped"
                found = True
                break

        if not found:
            raise KeyError(f"Enrollment for {sid} in {ccode} was not found.")

        self.storage.save_enrollments([e.to_dict() for e in all_enr])
        return True

    # -------------------------------------------------------------
    # Transcript & GPA Calculation
    # -------------------------------------------------------------
    def generate_transcript(self, student_id: str) -> Dict[str, Any]:
        """
        Calculates cumulative GPA based on credit weightage:
        CGPA = Sum(course_credits * grade_point) / Sum(course_credits)
        """
        student = self.get_student(student_id)
        if not student:
            raise KeyError(f"Student '{student_id}' does not exist.")

        courses_map = {c.course_code: c for c in self.get_all_courses()}
        all_enr = self.get_all_enrollments()
        student_enr = [e for e in all_enr if e.student_id == student.student_id and e.status != "Dropped"]

        records = []
        total_credit_points = 0.0
        total_graded_credits = 0
        total_registered_credits = 0

        for enr in student_enr:
            course = courses_map.get(enr.course_code)
            credits = course.credits if course else 3
            title = course.title if course else "Unknown Course"
            total_registered_credits += credits

            record = {
                "course_code": enr.course_code,
                "title": title,
                "credits": credits,
                "attendance_pct": enr.attendance_pct,
                "marks": enr.marks if enr.marks is not None else "N/A",
                "letter_grade": enr.letter_grade,
                "grade_point": enr.grade_point,
                "status": enr.status,
            }
            records.append(record)

            if enr.marks is not None and enr.status == "Completed":
                total_credit_points += credits * enr.grade_point
                total_graded_credits += credits

        cgpa = round(total_credit_points / total_graded_credits, 2) if total_graded_credits > 0 else 0.0

        return {
            "student": student.to_dict(),
            "records": records,
            "total_registered_credits": total_registered_credits,
            "total_earned_credits": sum(r["credits"] for r in records if r["grade_point"] > 0),
            "cgpa": cgpa,
        }
