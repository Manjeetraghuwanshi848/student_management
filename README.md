# Campus Student Management System (SMS)

**Institution:** VIT Bhopal University  
**Course:** Python Essentials  
**Author:** Manjeet Raghuvanshi (Registration No: 26MIM10152)  

A modular, zero-dependency academic record and course enrollment management system written in Python 3.

---

## Overview

The **Campus Student Management System (SMS)** is an administrative tool designed to manage student admissions, course registrations, academic evaluations, attendance tracking, and performance analytics. 

It provides both an **interactive terminal menu** for everyday human interaction and a full suite of **CLI subcommands** (via `argparse`) for automated scripts and headless evaluation. The system enforces strict referential integrity, validates all contact and academic data using regular expressions, calculates credit-weighted CGPA on a standard 10-point scale, and persists data reliably using atomic JSON file writes.

---

## Key Features

1. **Student Record Lifecycle:**
   - Add, inspect, search, update, and remove student profiles.
   - Strict validation for Student IDs (`26MIM10152` or `STU1001`), RFC-compliant emails, and 10-digit phone numbers.
   - Prevents duplicate student IDs and registered emails.

2. **Course Catalog Management:**
   - Define course offerings with codes (e.g., `CSE1001`), course titles, credit weightings (1–6), instructors, and maximum seat limits.
   - Prevent over-enrollment beyond class capacity.

3. **Academic Enrollment & Grading:**
   - Enroll students in courses with capacity and duplicate enrollment checks.
   - Record marks (0–100) and automatically map them to letter grades (`S`, `A`, `B`, `C`, `D`, `E`, `F`) and grade points (0–10).
   - Track and update attendance percentages.
   - Support course dropping with state preservation.

4. **Transcript & Weighted CGPA Calculation:**
   - Real-time generation of student transcripts showing registered courses, attendance, scores, letter grades, and credits earned.
   - Accurate computation of credit-weighted Cumulative Grade Point Average (CGPA):
     $$\text{CGPA} = \frac{\sum (\text{Credits} \times \text{Grade Point})}{\sum \text{Credits}}$$

5. **Institutional Analytics & Dean's Merit List:**
   - Department-wise student counts and average CGPA metrics.
   - Course pass/fail statistics, score ranges, and grade distribution histograms.
   - Attendance shortage alerts highlighting all students below the mandatory 75% attendance threshold.
   - Top academic rankers list (Dean's List) filterable by department.

6. **Data Durability & CSV Export:**
   - Atomic file writes using temporary files and `os.replace` to prevent corrupted data during unexpected termination.
   - Direct export of consolidated student rosters with CGPA to `student_report.csv`.

---

## Technologies & Tools

- **Language:** Python 3.8+
- **Standard Library Modules:**
  - `json` & `csv` – Structured data persistence and tabular report generation.
  - `re` – Pattern matching for emails, phone numbers, and academic IDs.
  - `argparse` – Subcommand parsing and automated grading execution.
  - `pathlib`, `os`, `shutil` – Filesystem isolation and atomic write swaps.
  - `datetime` – Timestamp tracking for registrations and course enrollments.
  - `unittest` – Comprehensive automated unit test suite.
- **External Dependencies:** **None** (100% pure standard library, guaranteeing portability and zero installation errors).

---

## Project Structure

```text
student_management_system/
├── README.md                 # Project documentation and quickstart
├── statement.md              # Problem statement, scope, and target users
├── PROJECT_REPORT.md         # Detailed 15-section academic project report
├── REPORT_CARD_26MIM10152.html # Official printable grade sheet for Manjeet Raghuvanshi
├── REPORT_CARD_26MIM10152.md   # Markdown transcript for Manjeet Raghuvanshi
├── generate_report.py        # 1-click script to generate & open report card in browser
├── requirements.txt          # Library dependencies note
├── .gitignore                # Ignored cache, reports, and temp files
├── .vscode/                  # VS Code environment configurations
│   └── settings.json
├── main.py                   # CLI entry point (interactive & subcommands)
├── sms/                      # Core application package
│   ├── __init__.py           # Package initialization
│   ├── models.py             # Student, Course, and Enrollment domain models
│   ├── validators.py         # Regex checks and grade point conversions
│   ├── storage.py            # Atomic JSON persistence layer
│   ├── services.py           # Core business logic and CGPA calculator
│   ├── analytics.py          # Metrics, attendance alerts, Dean's list, CSV
│   ├── cli.py                # Console formatter and menu handlers
│   └── sample_data.py        # Demo dataset generator
├── data/                     # Persistent JSON flat files
│   ├── students.json         # Pre-populated student records
│   ├── courses.json          # Pre-populated course catalog
│   └── enrollments.json      # Pre-populated grades and attendance records
└── tests/                    # Automated test suite
    ├── __init__.py
    ├── test_validators.py    # Unit tests for input checks & boundaries
    ├── test_models.py        # Unit tests for domain entity models
    ├── test_services.py      # Unit tests for business rules & CGPA math
    └── test_storage.py       # Unit tests for atomic file writes & recovery
```

---

## Installation & Setup

1. **Prerequisites:**
   Ensure Python 3.8 or higher is installed on your system.
   ```bash
   python --version
   ```

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/{your-username}/student-management-system.git
   cd student-management-system
   ```

3. **Install Dependencies:**
   No external packages are required! The system runs straight out of the box using Python's built-in libraries.

---

## How to Run the Project

### Option A: Interactive Terminal Mode (Recommended for Evaluators)

Run the main application script without arguments to open the menu-driven console:

```bash
python main.py
```

---

### Option B: Command-Line Subcommands (For Automated Scripts / Grading)

1. **List All Students:**
   ```bash
   python main.py list-students
   ```

2. **List All Courses:**
   ```bash
   python main.py list-courses
   ```

3. **Generate Full Transcript with CGPA:**
   ```bash
   python main.py transcript --id 26MIM10152
   ```

4. **View Institutional Analytics & Dean's Merit List:**
   ```bash
   python main.py analytics
   ```

5. **Quick 1-Click Browser Report Card:**
   ```bash
   python generate_report.py
   ```

---

## Automated Testing

Run the test suite via Python's standard `unittest` test runner:

```bash
python -m unittest discover tests
```

Expected output:
```text
Ran 12 tests in 0.045s

OK
```
