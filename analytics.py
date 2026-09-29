"""
Analytics & Academic Reporting Module

Computes institutional metrics including GPA rankings, pass/fail rates,
attendance debarment risk alerts, and CSV report exporting.
"""

import csv
from pathlib import Path
from typing import Dict, List, Any
from sms.services import StudentManagementService


class AcademicAnalytics:
    """Provides statistical reporting and data exports across the student body."""

    def __init__(self, service: StudentManagementService):
        self.service = service

    def get_department_summary(self) -> Dict[str, Dict[str, Any]]:
        """Calculates student headcounts and average CGPA per academic department."""
        students = self.service.get_all_students()
        dept_data: Dict[str, List[float]] = {}

        for s in students:
            dept = s.department
            transcript = self.service.generate_transcript(s.student_id)
            cgpa = transcript["cgpa"]
            if dept not in dept_data:
                dept_data[dept] = []
            dept_data[dept].append(cgpa)

        summary = {}
        for dept, cgpas in dept_data.items():
            valid_cgpas = [c for c in cgpas if c > 0]
            avg_cgpa = round(sum(valid_cgpas) / len(valid_cgpas), 2) if valid_cgpas else 0.0
            summary[dept] = {
                "total_students": len(cgpas),
                "graded_students": len(valid_cgpas),
                "average_cgpa": avg_cgpa,
                "highest_cgpa": max(cgpas) if cgpas else 0.0,
            }
        return summary

    def get_course_statistics(self, course_code: str) -> Dict[str, Any]:
        """Calculates enrollment count, average score, pass rate, and grade distribution."""
        course = self.service.get_course(course_code)
        if not course:
            raise KeyError(f"Course '{course_code}' does not exist.")

        all_enr = self.service.get_all_enrollments()
        course_enr = [e for e in all_enr if e.course_code == course.course_code and e.status != "Dropped"]

        marks_list = [e.marks for e in course_enr if e.marks is not None]
        passed_count = sum(1 for m in marks_list if m >= 40.0)

        grade_distribution = {"S": 0, "A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}
        for e in course_enr:
            if e.letter_grade in grade_distribution:
                grade_distribution[e.letter_grade] += 1

        avg_marks = round(sum(marks_list) / len(marks_list), 2) if marks_list else 0.0
        pass_rate = round((passed_count / len(marks_list)) * 100, 1) if marks_list else 0.0

        return {
            "course_code": course.course_code,
            "title": course.title,
            "credits": course.credits,
            "total_enrolled": len(course_enr),
            "total_graded": len(marks_list),
            "average_marks": avg_marks,
            "highest_marks": max(marks_list) if marks_list else 0.0,
            "lowest_marks": min(marks_list) if marks_list else 0.0,
            "pass_rate_pct": pass_rate,
            "grade_distribution": grade_distribution,
        }

    def get_attendance_risk_list(self, threshold_pct: float = 75.0) -> List[Dict[str, Any]]:
        """Identifies students whose attendance has fallen below mandatory criteria."""
        all_enr = self.service.get_all_enrollments()
        students_map = {s.student_id: s for s in self.service.get_all_students()}
        courses_map = {c.course_code: c for c in self.service.get_all_courses()}

        flagged = []
        for e in all_enr:
            if e.status != "Dropped" and e.attendance_pct < threshold_pct:
                stu = students_map.get(e.student_id)
                crs = courses_map.get(e.course_code)
                flagged.append({
                    "student_id": e.student_id,
                    "student_name": stu.name if stu else "Unknown",
                    "department": stu.department if stu else "Unknown",
                    "course_code": e.course_code,
                    "course_title": crs.title if crs else "Unknown",
                    "attendance_pct": e.attendance_pct,
                    "shortage_pct": round(threshold_pct - e.attendance_pct, 1),
                })
        return sorted(flagged, key=lambda x: x["attendance_pct"])

    def get_top_rankers(self, limit: int = 5, department: str = "") -> List[Dict[str, Any]]:
        """Returns the top N students ranked by CGPA."""
        students = self.service.get_all_students()
        if department:
            students = [s for s in students if s.department.lower() == department.strip().lower()]

        rank_data = []
        for s in students:
            transcript = self.service.generate_transcript(s.student_id)
            if transcript["total_earned_credits"] > 0:
                rank_data.append({
                    "student_id": s.student_id,
                    "name": s.name,
                    "department": s.department,
                    "semester": s.semester,
                    "cgpa": transcript["cgpa"],
                    "credits": transcript["total_earned_credits"],
                })

        rank_data.sort(key=lambda x: (x["cgpa"], x["credits"]), reverse=True)
        return rank_data[:limit]

    def export_students_csv(self, output_path: Path) -> Path:
        """Exports the full student directory with CGPA calculations into a CSV file."""
        students = self.service.get_all_students()
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = ["student_id", "name", "email", "phone", "department", "semester", "cgpa", "credits_earned"]
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for s in students:
                t = self.service.generate_transcript(s.student_id)
                writer.writerow({
                    "student_id": s.student_id,
                    "name": s.name,
                    "email": s.email,
                    "phone": s.phone,
                    "department": s.department,
                    "semester": s.semester,
                    "cgpa": t["cgpa"],
                    "credits_earned": t["total_earned_credits"],
                })
        return output_path
