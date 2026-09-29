# Project Problem Statement & Scope Specification

**Course:** Python Essentials  
**Institution:** VIT Bhopal University  
**Student Name:** Manjeet Raghuvanshi  
**Registration Number:** 26MIM10152  
**Project Title:** Campus Student Records & Academic Management System (SMS)  
**System Architecture:** Modular CLI-driven architecture with atomic JSON persistence  

---

## 1. Problem Statement

Academic institutions and departmental coordinators face recurring challenges with tracking student enrollments, course capacities, attendance records, and grade point calculations. Many small departments either rely on disorganized spreadsheets that lack referential integrity and validation, or bulky web platforms that are difficult to automate and inspect locally. 

Common real-world issues include:
* **Data Inconsistency:** Duplicated registration IDs, invalid email formats, and incorrect phone numbers entering records without regex checks.
* **Enrollment Bottlenecks:** Students exceeding maximum seat limits for lab or lecture courses due to lack of real-time capacity validation.
* **Manual GPA Errors:** Inaccurate grade point averaging when courses possess different credit weightages.
* **Attendance Risk Blindspots:** Difficulties quickly identifying students falling below the mandatory 75% attendance threshold prior to semester examinations.

There is a clear need for a self-contained, robust, and platform-independent command-line tool built in Python that enforces business constraints, maintains data persistence, provides instant GPA computation, and generates analytical summaries.

---

## 2. Scope of the Project

The scope encompasses:
1. **Core Entity Management:** Complete lifecycle management for Students, Academic Courses, and Enrollments.
2. **Academic Evaluation:** Automated mapping of marks (0-100) to letter grades (`S` through `F`) and 10-point scale grade points, with credit-weighted Cumulative Grade Point Average (CGPA) computation.
3. **Attendance Compliance:** Tracking attendance percentages per course enrollment and flagging students with attendance shortage (< 75%).
4. **Data Durability:** Resilient local storage using atomic file write patterns to avoid file corruption on unexpected interruptions.
5. **Administrative Analytics:** Computing department-wise CGPA distributions, course pass rates, Dean's merit list rankings, and exporting records to CSV.

**Out of Scope for this Version:**
* Multi-user concurrent network sockets (handled via single-node local terminal execution).
* Direct web/browser GUI (system is strictly terminal and CLI-driven as mandated by evaluation guidelines).

---

## 3. Target Users

* **Academic Program Coordinators & Faculty Advisors:** To monitor enrolled students, review attendance shortages, and track semester performance.
* **Course Instructors:** To input course details, submit final student evaluation marks, and view roster allocations.
* **Department Administrators:** To retrieve institutional metrics, compute department-wide CGPA averages, and export CSV reports for official archiving.
* **Course Evaluators:** To verify code correctness, run unit test suites, and execute subcommands in automated grading environments.

---

## 4. High-Level Features

* **Strict Input Validation:** Enforces regex patterns for Student IDs (`26MIM10152` or `STU1001`), emails, 10-digit phone numbers, and course codes (`CSE1001`).
* **Credit-Weighted CGPA Engine:** Accurately computes cumulative grade points according to course credits:
  $$\text{CGPA} = \frac{\sum (\text{Course Credits} \times \text{Grade Point})}{\sum \text{Course Credits}}$$
* **Course Seat & Capacity Protection:** Prevents over-enrollment beyond maximum course capacity limits.
* **Attendance Shortage Alert System:** Instant identification and sorting of students at risk of exam debarment (< 75% attendance).
* **Dual Execution Interface:** Interactive menu-driven console for human users alongside direct `argparse` CLI subcommands for scriptable and automated testing.
* **Zero External Dependencies:** Built entirely with the standard Python 3 library for 100% portability.
