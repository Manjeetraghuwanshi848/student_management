"""
Main Application Entry Point

Student Management System (SMS)
Course: Python Essentials
Institution: VIT Bhopal University
Author: Manjeet Raghuvanshi (26MIM10152)

Run interactively:
    python main.py

Or run direct CLI subcommands:
    python main.py --demo
    python main.py list-students
    python main.py list-courses
    python main.py transcript --id 26MIM10152
    python main.py analytics
    python main.py export --output report.csv
"""

import sys
import argparse
from pathlib import Path

# Ensure project directory is always in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sms.services import StudentManagementService
from sms.cli import CommandLineInterface, print_header, print_table
from sms.sample_data import load_demo_data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Command-line Student Management System for Python Essentials evaluation.",
        epilog="Run without arguments to launch the interactive terminal menu.",
    )

    parser.add_argument("--demo", action="store_true", help="Populate database with sample student/course records.")

    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # list-students
    subparsers.add_parser("list-students", help="List all registered students.")

    # list-courses
    subparsers.add_parser("list-courses", help="List all course offerings.")

    # add-student
    p_add_stu = subparsers.add_parser("add-student", help="Add a new student.")
    p_add_stu.add_argument("--id", required=True, help="Student ID (e.g. 26MIM10152)")
    p_add_stu.add_argument("--name", required=True, help="Full student name")
    p_add_stu.add_argument("--email", required=True, help="Email address")
    p_add_stu.add_argument("--phone", required=True, help="10-digit phone number")
    p_add_stu.add_argument("--dept", required=True, help="Department")
    p_add_stu.add_argument("--sem", type=int, default=1, help="Semester (default 1)")

    # add-course
    p_add_crs = subparsers.add_parser("add-course", help="Add a new course.")
    p_add_crs.add_argument("--code", required=True, help="Course code (e.g. CSE1002)")
    p_add_crs.add_argument("--title", required=True, help="Course title")
    p_add_crs.add_argument("--credits", type=int, required=True, help="Course credits (1-6)")
    p_add_crs.add_argument("--dept", required=True, help="Department")
    p_add_crs.add_argument("--instructor", default="TBD", help="Instructor name")
    p_add_crs.add_argument("--cap", type=int, default=60, help="Max enrollment capacity")

    # enroll
    p_enr = subparsers.add_parser("enroll", help="Enroll a student into a course.")
    p_enr.add_argument("--student", required=True, help="Student ID")
    p_enr.add_argument("--course", required=True, help="Course Code")

    # grade
    p_grd = subparsers.add_parser("grade", help="Record final course marks.")
    p_grd.add_argument("--student", required=True, help="Student ID")
    p_grd.add_argument("--course", required=True, help="Course Code")
    p_grd.add_argument("--marks", type=float, required=True, help="Score (0 - 100)")

    # attendance
    p_att = subparsers.add_parser("attendance", help="Record student attendance percentage.")
    p_att.add_argument("--student", required=True, help="Student ID")
    p_att.add_argument("--course", required=True, help="Course Code")
    p_att.add_argument("--pct", type=float, required=True, help="Attendance percentage (0 - 100)")

    # transcript
    p_trx = subparsers.add_parser("transcript", help="Print academic transcript & CGPA.")
    p_trx.add_argument("--id", required=True, help="Student ID")

    # analytics
    subparsers.add_parser("analytics", help="Show institutional analytics & merit rankings.")

    # export
    p_exp = subparsers.add_parser("export", help="Export student data to CSV.")
    p_exp.add_argument("--output", default="student_report.csv", help="Path for CSV output")

    return parser


def main() -> None:
    service = StudentManagementService()
    cli = CommandLineInterface(service)
    parser = build_parser()

    if len(sys.argv) == 1:
        cli.run_interactive()
        return

    args = parser.parse_args()

    if args.demo:
        load_demo_data(service)
        print("[OK] Sample records successfully populated into database.")
        if not args.subcommand:
            cli.list_students()
            return

    if args.subcommand == "list-students":
        cli.list_students()

    elif args.subcommand == "list-courses":
        cli.list_courses()

    elif args.subcommand == "add-student":
        try:
            s = service.add_student(args.id, args.name, args.email, args.phone, args.dept, args.sem)
            print(f"[OK] Added student: {s.name} ({s.student_id})")
        except Exception as err:
            print(f"[!] Error: {err}")
            sys.exit(1)

    elif args.subcommand == "add-course":
        try:
            c = service.add_course(args.code, args.title, args.credits, args.dept, args.instructor, args.cap)
            print(f"[OK] Added course: {c.course_code} - {c.title}")
        except Exception as err:
            print(f"[!] Error: {err}")
            sys.exit(1)

    elif args.subcommand == "enroll":
        try:
            enr = service.enroll_student(args.student, args.course)
            print(f"[OK] Successfully enrolled {enr.student_id} into {enr.course_code}.")
        except Exception as err:
            print(f"[!] Error: {err}")
            sys.exit(1)

    elif args.subcommand == "grade":
        try:
            enr = service.record_grade(args.student, args.course, args.marks)
            print(f"[OK] Grade recorded: {enr.marks}% -> Grade '{enr.letter_grade}' (Point: {enr.grade_point})")
        except Exception as err:
            print(f"[!] Error: {err}")
            sys.exit(1)

    elif args.subcommand == "attendance":
        try:
            enr = service.record_attendance(args.student, args.course, args.pct)
            print(f"[OK] Attendance updated for {enr.student_id}: {enr.attendance_pct}%")
        except Exception as err:
            print(f"[!] Error: {err}")
            sys.exit(1)

    elif args.subcommand == "transcript":
        try:
            t = service.generate_transcript(args.id)
            student = t["student"]
            print_header(f"Academic Transcript: {student['name']} ({student['student_id']})")
            print(f"  Department: {student['department']} | Semester: {student['semester']}")
            print("-" * 68)
            rows = [
                [r["course_code"], r["title"][:22], r["credits"], f"{r['attendance_pct']}%", r["marks"], r["letter_grade"], r["grade_point"]]
                for r in t["records"]
            ]
            print_table(["Code", "Course Name", "Credits", "Attend.", "Marks", "Grade", "Points"], rows)
            print(f"  Total Credits Earned : {t['total_earned_credits']}")
            print(f"  Cumulative GPA       : {t['cgpa']} / 10.00")
            print("-" * 68)
        except Exception as err:
            print(f"[!] Error: {err}")
            sys.exit(1)

    elif args.subcommand == "analytics":
        print_header("Institutional Summary")
        dept_sum = cli.analytics.get_department_summary()
        d_rows = [[d, val["total_students"], val["graded_students"], val["average_cgpa"], val["highest_cgpa"]] for d, val in dept_sum.items()]
        print_table(["Department", "Total Students", "Graded", "Avg CGPA", "Top CGPA"], d_rows)

        print_header("Top Academic Rankers")
        rankers = cli.analytics.get_top_rankers(limit=5)
        r_rows = [[idx + 1, r["student_id"], r["name"], r["department"], f"Sem {r['semester']}", r["cgpa"]] for idx, r in enumerate(rankers)]
        print_table(["Rank", "ID", "Name", "Department", "Semester", "CGPA"], r_rows)

    elif args.subcommand == "export":
        out = Path(args.output)
        cli.analytics.export_students_csv(out)
        print(f"[OK] Exported student records to '{out.resolve()}'.")


if __name__ == "__main__":
    main()
