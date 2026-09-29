"""
Sample Data Loader

Generates realistic initial academic dataset for testing and demonstration.
Useful for evaluators to immediately verify features without manual typing.
"""

from sms.services import StudentManagementService


SAMPLE_STUDENTS = [
    ("26MIM10152", "Manjeet Raghuvanshi", "manjeet.raghuvanshi2026@vitstudent.ac.in", "9876543202", "Integrated M.Tech Software Engineering", 3),
    ("26MIM10172", "Neeraj Mewada", "neeraj.mewada2026@vitstudent.ac.in", "9876543201", "Integrated M.Tech Software Engineering", 3),
    ("STU1001", "Aarav Sharma", "aarav.sharma@campus.edu", "9876543210", "Computer Science", 4),
    ("STU1002", "Priya Nair", "priya.nair@campus.edu", "9876543211", "Computer Science", 4),
    ("STU1003", "Rohan Verma", "rohan.verma@campus.edu", "9876543212", "Information Tech", 3),
    ("STU1004", "Ananya Iyer", "ananya.iyer@campus.edu", "9876543213", "Electronics", 4),
    ("STU1005", "Kavya Patel", "kavya.patel@campus.edu", "9876543214", "Mechanical", 2),
    ("STU1006", "Devendra Joshi", "dev.joshi@campus.edu", "9876543215", "Computer Science", 4),
]

SAMPLE_COURSES = [
    ("CSE1001", "Problem Solving & Python", 4, "Computer Science", "Dr. A. Raman", 60),
    ("CSE2001", "Data Structures & Algorithms", 4, "Computer Science", "Prof. M. Kulkarni", 50),
    ("MAT1001", "Calculus & Linear Algebra", 4, "Mathematics", "Dr. S. Banerjee", 65),
    ("ECE1002", "Digital Logic Design", 3, "Electronics", "Prof. V. Reddy", 45),
    ("ENG1001", "Technical Communication", 2, "Humanities", "Dr. L. Fernandez", 70),
]

SAMPLE_ENROLLMENTS = [
    # Manjeet Raghuvanshi enrollments (CGPA: 9.43)
    ("26MIM10152", "CSE1001", 95.0, 93.0),
    ("26MIM10152", "CSE2001", 91.0, 86.5),
    ("26MIM10152", "MAT1001", 93.0, 89.0),
    ("26MIM10152", "ENG1001", 96.0, 94.0),
    # Other students
    ("26MIM10172", "CSE1001", 96.0, 95.0),
    ("26MIM10172", "CSE2001", 92.5, 88.0),
    ("26MIM10172", "MAT1001", 90.0, 85.5),
    ("26MIM10172", "ENG1001", 95.0, 92.0),
    ("STU1001", "CSE1001", 94.0, 92.5),
    ("STU1001", "CSE2001", 88.0, 84.0),
    ("STU1001", "MAT1001", 90.0, 78.0),
    ("STU1002", "CSE1001", 96.0, 95.0),
    ("STU1002", "CSE2001", 92.0, 89.0),
    ("STU1002", "MAT1001", 85.0, 91.0),
    ("STU1003", "CSE1001", 72.0, 64.0),
    ("STU1003", "MAT1001", 68.0, 52.0),
    ("STU1004", "ECE1002", 91.0, 86.0),
    ("STU1004", "MAT1001", 89.0, 74.0),
    ("STU1005", "MAT1001", 62.0, 38.0),
    ("STU1006", "CSE1001", 82.0, 76.0),
]


def load_demo_data(service: StudentManagementService) -> None:
    """Populates clean sample data into the database."""
    existing_students = {s.student_id for s in service.get_all_students()}
    for sid, name, email, phone, dept, sem in SAMPLE_STUDENTS:
        if sid not in existing_students:
            service.add_student(sid, name, email, phone, dept, sem)

    existing_courses = {c.course_code for c in service.get_all_courses()}
    for code, title, credits, dept, inst, cap in SAMPLE_COURSES:
        if code not in existing_courses:
            service.add_course(code, title, credits, dept, inst, cap)

    for sid, ccode, att, marks in SAMPLE_ENROLLMENTS:
        try:
            enr = service.get_enrollment(sid, ccode)
            if not enr:
                enr = service.enroll_student(sid, ccode)
            service.record_attendance(sid, ccode, att)
            if marks is not None:
                service.record_grade(sid, ccode, marks)
        except Exception:
            pass
