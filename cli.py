"""
Terminal User Interface & Command Dispatcher

Provides both an interactive text menu and command-line argument dispatching.
Formats outputs into clean tables using only Python standard library.
"""

from typing import List, Any, Optional
from pathlib import Path

from sms.services import StudentManagementService
from sms.analytics import AcademicAnalytics


def print_header(title: str) -> None:
    width = 68
    print("\n" + "=" * width)
    print(f" {title.upper()}".center(width))
    print("=" * width)


def print_table(headers: List[str], rows: List[List[Any]]) -> None:
    """Renders tabular data with dynamic column widths using standard string formatting."""
    if not rows:
        print("  (No records found)")
        return

    col_widths = [len(h) for h in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(str(cell)))

    col_widths = [w + 2 for w in col_widths]

    header_line = "".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    separator = "".join("-" * (w - 1) + " " for w in col_widths)

    print("  " + header_line)
    print("  " + separator)

    for row in rows:
        row_line = "".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        print("  " + row_line)
    print()


class CommandLineInterface:
    """Manages user interaction via terminal console."""

    def __init__(self, service: Optional[StudentManagementService] = None):
        self.service = service or StudentManagementService()
        self.analytics = AcademicAnalytics(self.service)

    def run_interactive(self) -> None:
        while True:
            print_header("VIT Bhopal - Student Management System")
            print("  1. Student Records (Add, View, Search, Delete)")
            print("  2. Course Offerings (Add, View, Update, Remove)")
            print("  3. Academic Enrollment & Records (Enroll, Marks, Attendance)")
            print("  4. Grade Reports & Transcripts (CGPA Computation)")
            print("  5. Institutional Analytics & Dean's List")
            print("  6. Export Reports to CSV")
            print("  0. Exit System")
            print("-" * 68)

            try:
                choice = input("Select an option [0-6]: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\nExiting Student Management System. Goodbye!")
                break

            if choice == "1":
                self._menu_students()
            elif choice == "2":
                self._menu_courses()
            elif choice == "3":
                self._menu_enrollments()
            elif choice == "4":
                self._menu_transcripts()
            elif choice == "5":
                self._menu_analytics()
            elif choice == "6":
                self._menu_export()
            elif choice == "0":
                print("\nExiting Student Management System. Have a productive day!")
                break
            else:
                print("\n[!] Invalid selection. Please enter a number between 0 and 6.")

    def _menu_students(self) -> None:
        while True:
            print_header("Student Management Menu")
            print("  1. List All Students")
            print("  2. Add New Student")
            print("  3. Search Student Records")
            print("  4. View Student Profile")
            print("  5. Update Student Details")
            print("  6. Delete Student Record")
            print("  0. Back to Main Menu")
            print("-" * 68)

            choice = input("Select an option: ").strip()
            if choice == "1":
                self.list_students()
            elif choice == "2":
                self.prompt_add_student()
            elif choice == "3":
                kw = input("Enter search term (ID, Name, or Department): ").strip()
                results = self.service.search_students(kw)
                rows = [
                    [s.student_id, s.name, s.department, f"Sem {s.semester}", s.email]
                    for s in results
                ]
                print_header(f"Search Results for '{kw}' ({len(results)} found)")
                print_table(["ID", "Name", "Department", "Semester", "Email"], rows)
            elif choice == "4":
                sid = input("Enter Student ID: ").strip()
                s = self.service.get_student(sid)
                if s:
                    print(f"\n  Student ID : {s.student_id}")
                    print(f"  Name       : {s.name}")
                    print(f"  Department : {s.department}")
                    print(f"  Semester   : {s.semester}")
                    print(f"  Email      : {s.email}")
                    print(f"  Phone      : {s.phone}")
                    print(f"  Registered : {s.created_at}")
                else:
                    print(f"\n[!] Student '{sid}' not found.")
            elif choice == "5":
                self.prompt_update_student()
            elif choice == "6":
                sid = input("Enter Student ID to delete: ").strip()
                confirm = input(f"Are you sure you want to permanently delete {sid}? (y/N): ").strip().lower()
                if confirm == "y":
                    try:
                        self.service.delete_student(sid)
                        print(f"[OK] Student record '{sid}' removed.")
                    except KeyError as err:
                        print(f"[!] Error: {err}")
            elif choice == "0":
                break

    def _menu_courses(self) -> None:
        while True:
            print_header("Course Management Menu")
            print("  1. List All Courses")
            print("  2. Add New Course")
            print("  3. Update Course Details")
            print("  4. Remove Course Offering")
            print("  0. Back to Main Menu")
            print("-" * 68)

            choice = input("Select an option: ").strip()
            if choice == "1":
                self.list_courses()
            elif choice == "2":
                self.prompt_add_course()
            elif choice == "3":
                self.prompt_update_course()
            elif choice == "4":
                code = input("Enter Course Code to remove: ").strip()
                confirm = input(f"Confirm deleting course '{code}'? (y/N): ").strip().lower()
                if confirm == "y":
                    try:
                        self.service.delete_course(code)
                        print(f"[OK] Course '{code}' removed.")
                    except KeyError as err:
                        print(f"[!] Error: {err}")
            elif choice == "0":
                break

    def _menu_enrollments(self) -> None:
        while True:
            print_header("Academic Enrollment & Records")
            print("  1. Enroll Student in Course")
            print("  2. Record / Update Final Marks")
            print("  3. Update Attendance Percentage")
            print("  4. View Course Roster")
            print("  5. Drop Student from Course")
            print("  0. Back to Main Menu")
            print("-" * 68)

            choice = input("Select an option: ").strip()
            if choice == "1":
                self.prompt_enroll_student()
            elif choice == "2":
                self.prompt_record_marks()
            elif choice == "3":
                self.prompt_record_attendance()
            elif choice == "4":
                ccode = input("Enter Course Code: ").strip().upper()
                c = self.service.get_course(ccode)
                if not c:
                    print(f"[!] Course '{ccode}' does not exist.")
                    continue
                enrs = [e for e in self.service.get_all_enrollments() if e.course_code == ccode and e.status != "Dropped"]
                students_map = {s.student_id: s for s in self.service.get_all_students()}
                rows = []
                for e in enrs:
                    stu = students_map.get(e.student_id)
                    sname = stu.name if stu else "Unknown"
                    rows.append([e.student_id, sname, f"{e.attendance_pct}%", e.marks if e.marks is not None else "--", e.letter_grade, e.status])
                print_header(f"Enrollment Roster for {ccode} - {c.title} ({len(rows)} students)")
                print_table(["ID", "Name", "Attendance", "Marks", "Grade", "Status"], rows)
            elif choice == "5":
                sid = input("Enter Student ID: ").strip()
                ccode = input("Enter Course Code: ").strip()
                try:
                    self.service.drop_course(sid, ccode)
                    print(f"[OK] Dropped student {sid} from course {ccode}.")
                except Exception as err:
                    print(f"[!] Error: {err}")
            elif choice == "0":
                break

    def _menu_transcripts(self) -> None:
        sid = input("\nEnter Student ID for Grade Transcript: ").strip()
        try:
            transcript = self.service.generate_transcript(sid)
            student = transcript["student"]
            print_header(f"Academic Transcript: {student['name']} ({student['student_id']})")
            print(f"  Department: {student['department']} | Semester: {student['semester']}")
            print("-" * 68)

            rows = []
            for r in transcript["records"]:
                rows.append([
                    r["course_code"],
                    r["title"][:22],
                    r["credits"],
                    f"{r['attendance_pct']}%",
                    r["marks"],
                    r["letter_grade"],
                    r["grade_point"],
                ])
            print_table(["Code", "Course Name", "Credits", "Attend.", "Marks", "Grade", "Points"], rows)
            print(f"  Total Registered Credits : {transcript['total_registered_credits']}")
            print(f"  Total Credits Earned     : {transcript['total_earned_credits']}")
            print(f"  Cumulative GPA (CGPA)    : {transcript['cgpa']} / 10.00")
            print("-" * 68)
        except KeyError as err:
            print(f"[!] Error: {err}")

    def _menu_analytics(self) -> None:
        while True:
            print_header("Institutional Analytics & Metrics")
            print("  1. Department Performance Overview")
            print("  2. Course Pass/Fail & Grade Breakdown")
            print("  3. Attendance Shortage Risk Alert (< 75%)")
            print("  4. Top Academic Rankers (Dean's List)")
            print("  0. Back to Main Menu")
            print("-" * 68)

            choice = input("Select an option: ").strip()
            if choice == "1":
                dept_summary = self.analytics.get_department_summary()
                rows = []
                for dept, data in dept_summary.items():
                    rows.append([dept, data["total_students"], data["graded_students"], data["average_cgpa"], data["highest_cgpa"]])
                print_header("Department Performance Summary")
                print_table(["Department", "Total Students", "Graded", "Avg CGPA", "Top CGPA"], rows)
            elif choice == "2":
                ccode = input("Enter Course Code: ").strip()
                try:
                    stats = self.analytics.get_course_statistics(ccode)
                    print_header(f"Performance Metrics: {stats['course_code']} - {stats['title']}")
                    print(f"  Credits: {stats['credits']} | Total Enrolled: {stats['total_enrolled']} | Graded: {stats['total_graded']}")
                    print(f"  Average Score : {stats['average_marks']} / 100")
                    print(f"  Highest Score : {stats['highest_marks']} | Lowest Score: {stats['lowest_marks']}")
                    print(f"  Pass Rate     : {stats['pass_rate_pct']}%")
                    print("\n  Grade Distribution:")
                    for g, count in stats["grade_distribution"].items():
                        bar = "#" * count
                        print(f"    Grade {g:2s}: {count:2d}  {bar}")
                    print()
                except KeyError as err:
                    print(f"[!] Error: {err}")
            elif choice == "3":
                risks = self.analytics.get_attendance_risk_list(threshold_pct=75.0)
                if not risks:
                    print("\n[OK] No students are currently below the 75% attendance threshold.")
                else:
                    rows = [[r["student_id"], r["student_name"][:18], r["course_code"], f"{r['attendance_pct']}%", f"-{r['shortage_pct']}%"] for r in risks]
                    print_header("Attendance Shortage Alerts (< 75%)")
                    print_table(["Student ID", "Name", "Course", "Attendance", "Shortage"], rows)
            elif choice == "4":
                dept = input("Filter by department (or press Enter for all): ").strip()
                rankers = self.analytics.get_top_rankers(limit=5, department=dept)
                rows = [[idx + 1, r["student_id"], r["name"], r["department"], f"Sem {r['semester']}", r["cgpa"]] for idx, r in enumerate(rankers)]
                print_header("Dean's Merit List - Top Rankers")
                print_table(["Rank", "ID", "Name", "Department", "Semester", "CGPA"], rows)
            elif choice == "0":
                break

    def _menu_export(self) -> None:
        target_path = Path("student_report.csv")
        try:
            self.analytics.export_students_csv(target_path)
            print(f"\n[OK] Export successful! Data saved to '{target_path.resolve()}'.")
        except Exception as err:
            print(f"[!] Export failed: {err}")

    def list_students(self) -> None:
        students = self.service.get_all_students()
        rows = [[s.student_id, s.name, s.department, f"Sem {s.semester}", s.email, s.phone] for s in students]
        print_header(f"Student Directory ({len(students)} Total)")
        print_table(["ID", "Name", "Department", "Semester", "Email", "Phone"], rows)

    def list_courses(self) -> None:
        courses = self.service.get_all_courses()
        all_enr = self.service.get_all_enrollments()
        rows = []
        for c in courses:
            enrolled_count = sum(1 for e in all_enr if e.course_code == c.course_code and e.status != "Dropped")
            cap_str = f"{enrolled_count}/{c.max_capacity}"
            rows.append([c.course_code, c.title, c.credits, c.department, c.instructor, cap_str])
        print_header(f"Course Catalogue ({len(courses)} Total)")
        print_table(["Code", "Title", "Credits", "Department", "Instructor", "Enrollment"], rows)

    def prompt_add_student(self) -> None:
        print("\nEnter Student Details:")
        sid = input("  Student ID (e.g. 26MIM10152 or STU1001): ").strip()
        name = input("  Full Name: ").strip()
        email = input("  Email: ").strip()
        phone = input("  Phone (10 digits): ").strip()
        dept = input("  Department: ").strip()
        sem = input("  Semester (1-8): ").strip()
        try:
            sem_int = int(sem) if sem else 1
            s = self.service.add_student(sid, name, email, phone, dept, sem_int)
            print(f"[OK] Student registered successfully: {s.name} ({s.student_id})")
        except Exception as err:
            print(f"[!] Registration failed: {err}")

    def prompt_update_student(self) -> None:
        sid = input("Enter Student ID to update: ").strip()
        s = self.service.get_student(sid)
        if not s:
            print(f"[!] Student '{sid}' not found.")
            return

        print(f"Leave field blank to keep current value.")
        name = input(f"  Name [{s.name}]: ").strip() or None
        email = input(f"  Email [{s.email}]: ").strip() or None
        phone = input(f"  Phone [{s.phone}]: ").strip() or None
        dept = input(f"  Department [{s.department}]: ").strip() or None
        sem_in = input(f"  Semester [{s.semester}]: ").strip()
        sem = int(sem_in) if sem_in else None

        try:
            self.service.update_student(sid, name=name, email=email, phone=phone, department=dept, semester=sem)
            print(f"[OK] Student '{sid}' updated successfully.")
        except Exception as err:
            print(f"[!] Update failed: {err}")

    def prompt_add_course(self) -> None:
        print("\nEnter Course Details:")
        code = input("  Course Code (e.g. CSE1001): ").strip()
        title = input("  Course Title: ").strip()
        credits_in = input("  Credits (1-6): ").strip()
        dept = input("  Department: ").strip()
        instructor = input("  Instructor Name: ").strip()
        capacity_in = input("  Max Capacity [default 60]: ").strip()

        try:
            credits = int(credits_in)
            cap = int(capacity_in) if capacity_in else 60
            c = self.service.add_course(code, title, credits, dept, instructor, cap)
            print(f"[OK] Course '{c.course_code}' registered successfully.")
        except Exception as err:
            print(f"[!] Course registration failed: {err}")

    def prompt_update_course(self) -> None:
        code = input("Enter Course Code to update: ").strip()
        c = self.service.get_course(code)
        if not c:
            print(f"[!] Course '{code}' not found.")
            return

        print("Leave blank to retain existing value.")
        title = input(f"  Title [{c.title}]: ").strip() or None
        creds_in = input(f"  Credits [{c.credits}]: ").strip()
        creds = int(creds_in) if creds_in else None
        dept = input(f"  Department [{c.department}]: ").strip() or None
        inst = input(f"  Instructor [{c.instructor}]: ").strip() or None
        cap_in = input(f"  Capacity [{c.max_capacity}]: ").strip()
        cap = int(cap_in) if cap_in else None

        try:
            self.service.update_course(code, title=title, credits=creds, department=dept, instructor=inst, max_capacity=cap)
            print(f"[OK] Course '{code}' updated successfully.")
        except Exception as err:
            print(f"[!] Update failed: {err}")

    def prompt_enroll_student(self) -> None:
        sid = input("Enter Student ID: ").strip()
        ccode = input("Enter Course Code: ").strip()
        try:
            enr = self.service.enroll_student(sid, ccode)
            print(f"[OK] Successfully enrolled {enr.student_id} into {enr.course_code}.")
        except Exception as err:
            print(f"[!] Enrollment failed: {err}")

    def prompt_record_marks(self) -> None:
        sid = input("Enter Student ID: ").strip()
        ccode = input("Enter Course Code: ").strip()
        marks_in = input("Enter Final Score (0 - 100): ").strip()
        try:
            marks = float(marks_in)
            enr = self.service.record_grade(sid, ccode, marks)
            print(f"[OK] Grade recorded: {enr.marks}% -> Grade '{enr.letter_grade}' (Grade Point: {enr.grade_point})")
        except Exception as err:
            print(f"[!] Failed to record marks: {err}")

    def prompt_record_attendance(self) -> None:
        sid = input("Enter Student ID: ").strip()
        ccode = input("Enter Course Code: ").strip()
        pct_in = input("Enter Attendance Percentage (0 - 100): ").strip()
        try:
            pct = float(pct_in)
            enr = self.service.record_attendance(sid, ccode, pct)
            print(f"[OK] Attendance updated: {enr.student_id} in {enr.course_code} is now {enr.attendance_pct}%.")
        except Exception as err:
            print(f"[!] Failed to record attendance: {err}")
