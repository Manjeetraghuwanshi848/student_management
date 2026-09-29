"""
Quick Report Card Generator
Generates an official-looking printable report card HTML file
and automatically opens it in your default web browser.

Usage:
    python generate_report.py
    python generate_report.py 26MIM10152
"""

import sys
import webbrowser
from pathlib import Path

# Ensure project directory is always in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sms.services import StudentManagementService


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Academic Grade Sheet - {name} ({student_id}) | VIT Bhopal</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 12mm 15mm;
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 24px;
      color: #0f172a;
      background-color: #f1f5f9;
    }}
    .no-print-bar {{
      max-width: 820px;
      margin: 0 auto 16px auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #0f172a;
      color: white;
      padding: 12px 22px;
      border-radius: 8px;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.15);
    }}
    .no-print-bar .title {{
      font-weight: 600;
      font-size: 14px;
      letter-spacing: 0.5px;
    }}
    .print-btn {{
      background: #2563eb;
      color: white;
      border: none;
      padding: 9px 24px;
      font-size: 14px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
      transition: background 0.15s ease;
    }}
    .print-btn:hover {{
      background: #1d4ed8;
    }}
    .card {{
      max-width: 820px;
      margin: 0 auto;
      background: #ffffff;
      padding: 42px 46px;
      border-radius: 8px;
      border: 1px solid #e2e8f0;
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.06);
    }}
    .header {{
      text-align: center;
      border-bottom: 2.5px solid #0f172a;
      padding-bottom: 18px;
      margin-bottom: 24px;
    }}
    .header h1 {{
      margin: 0;
      font-size: 26px;
      letter-spacing: 2px;
      color: #0f172a;
      font-weight: 800;
      text-transform: uppercase;
    }}
    .header h2 {{
      margin: 6px 0 0 0;
      font-size: 15px;
      color: #334155;
      font-weight: 600;
    }}
    .header .subtitle {{
      margin-top: 6px;
      font-size: 13px;
      font-weight: 700;
      color: #2563eb;
      letter-spacing: 1.2px;
      text-transform: uppercase;
    }}
    .info-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      row-gap: 10px;
      column-gap: 28px;
      background: #f8fafc;
      padding: 18px 24px;
      border-radius: 6px;
      font-size: 13.5px;
      border: 1px solid #e2e8f0;
      margin-bottom: 26px;
    }}
    .info-item {{
      display: flex;
    }}
    .info-label {{
      font-weight: 600;
      width: 140px;
      color: #64748b;
    }}
    .info-val {{
      font-weight: 700;
      color: #0f172a;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 24px;
      font-size: 13.5px;
    }}
    th {{
      background-color: #0f172a;
      color: #ffffff;
      font-weight: 600;
      padding: 11px 10px;
      text-align: left;
      font-size: 12px;
      letter-spacing: 0.5px;
    }}
    th.center, td.center {{
      text-align: center;
    }}
    td {{
      padding: 11px 10px;
      border-bottom: 1px solid #e2e8f0;
      color: #1e293b;
    }}
    tr:nth-child(even) {{
      background-color: #f8fafc;
    }}
    .badge {{
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 4px;
      display: inline-block;
    }}
    .badge-S {{ background-color: #dcfce7; color: #15803d; }}
    .badge-A {{ background-color: #dbeafe; color: #1d4ed8; }}
    .badge-B {{ background-color: #fef3c7; color: #b45309; }}
    .badge-C {{ background-color: #ffedd5; color: #c2410c; }}
    .badge-D {{ background-color: #f1f5f9; color: #475569; }}
    .badge-E {{ background-color: #fee2e2; color: #b91c1c; }}
    .badge-F {{ background-color: #991b1b; color: #ffffff; }}
    .badge-NA {{ background-color: #f1f5f9; color: #64748b; }}
    .summary-box {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      border-radius: 6px;
      padding: 16px;
      text-align: center;
      margin-bottom: 22px;
    }}
    .summary-box .item-title {{
      font-size: 11px;
      text-transform: uppercase;
      color: #1e40af;
      font-weight: 600;
      letter-spacing: 0.5px;
    }}
    .summary-box .item-value {{
      font-size: 22px;
      font-weight: 800;
      color: #1e3a8a;
      margin-top: 4px;
    }}
    .classification-note {{
      font-size: 12.5px;
      color: #334155;
      line-height: 1.6;
      background: #ffffff;
      border-left: 4px solid #2563eb;
      padding: 10px 14px;
      margin-top: 10px;
      background: #f8fafc;
      border-radius: 0 4px 4px 0;
    }}
    .footer {{
      display: flex;
      justify-content: space-between;
      margin-top: 48px;
      padding-top: 24px;
      border-top: 1px dashed #cbd5e1;
      font-size: 12px;
      color: #64748b;
    }}
    .signature {{
      text-align: center;
      width: 210px;
    }}
    .sig-line {{
      border-top: 1px solid #334155;
      margin-top: 42px;
      padding-top: 5px;
      font-weight: 700;
      color: #0f172a;
    }}
    @media print {{
      body {{
        background-color: #ffffff;
        padding: 0;
      }}
      .no-print-bar {{
        display: none;
      }}
      .card {{
        border: none;
        box-shadow: none;
        padding: 0;
      }}
    }}
  </style>
</head>
<body>

<div class="no-print-bar">
  <div class="title"><strong>VIT Bhopal University:</strong> Student Grade Transcript</div>
  <button class="print-btn" onclick="window.print()">Save as PDF / Print</button>
</div>

<div class="card">
  <div class="header">
    <h1>VIT BHOPAL UNIVERSITY</h1>
    <h2>School of Computing Science & Engineering</h2>
    <div class="subtitle">OFFICIAL SEMESTER GRADE REPORT & ACADEMIC TRANSCRIPT</div>
  </div>

  <div class="info-grid">
    <div class="info-item">
      <span class="info-label">Student Name:</span>
      <span class="info-val">{name}</span>
    </div>
    <div class="info-item">
      <span class="info-label">Register Number:</span>
      <span class="info-val">{student_id}</span>
    </div>
    <div class="info-item">
      <span class="info-label">Programme:</span>
      <span class="info-val">{department}</span>
    </div>
    <div class="info-item">
      <span class="info-label">Current Semester:</span>
      <span class="info-val">Semester {semester}</span>
    </div>
    <div class="info-item">
      <span class="info-label">Academic Session:</span>
      <span class="info-val">Fall Semester 2025–26</span>
    </div>
    <div class="info-item">
      <span class="info-label">Institution:</span>
      <span class="info-val">VIT Bhopal University</span>
    </div>
  </div>

  <table>
    <thead>
      <tr>
        <th class="center" style="width: 85px;">Course Code</th>
        <th>Course Title</th>
        <th class="center" style="width: 60px;">Credits</th>
        <th class="center" style="width: 85px;">Attendance</th>
        <th class="center" style="width: 75px;">Marks</th>
        <th class="center" style="width: 65px;">Grade</th>
        <th class="center" style="width: 65px;">Points</th>
        <th class="center" style="width: 75px;">Status</th>
      </tr>
    </thead>
    <tbody>
      {table_rows}
    </tbody>
  </table>

  <div class="summary-box">
    <div>
      <div class="item-title">Credits Registered</div>
      <div class="item-value">{total_registered_credits}</div>
    </div>
    <div>
      <div class="item-title">Credits Earned</div>
      <div class="item-value">{total_earned_credits}</div>
    </div>
    <div>
      <div class="item-title">Semester SGPA</div>
      <div class="item-value">{cgpa}</div>
    </div>
    <div>
      <div class="item-title">Cumulative CGPA</div>
      <div class="item-value">{cgpa} / 10.0</div>
    </div>
  </div>

  <div class="classification-note">
    <strong>Academic Standing:</strong> {academic_status}<br>
    <strong>Formula:</strong> CGPA = &sum;(Course Credits &times; Grade Point) / &sum;(Course Credits) = <strong>{cgpa}</strong>
  </div>

  <div class="footer">
    <div class="signature">
      <div class="sig-line">Faculty Advisor</div>
      <div>VIT Bhopal University</div>
    </div>
    <div style="text-align: center; align-self: flex-end;">
      <div>Verified via Student Management System (SMS)</div>
      <div style="font-size: 11px; color: #94a3b8;">System Digital Hash: {student_id}-VITB-AUTH</div>
    </div>
    <div class="signature">
      <div class="sig-line">Controller of Examinations</div>
      <div>VIT Bhopal University</div>
    </div>
  </div>
</div>

</body>
</html>
"""


def generate_report_card(student_id: str = "26MIM10152") -> Path:
    service = StudentManagementService()
    student_id = student_id.strip().upper()

    try:
        transcript = service.generate_transcript(student_id)
    except KeyError:
        print(f"[!] Error: Student with ID '{student_id}' does not exist.")
        sys.exit(1)

    student = transcript["student"]
    records = transcript["records"]

    rows_html = []
    for r in records:
        badge_cls = f"badge-{r['letter_grade']}" if r['letter_grade'] in ["S", "A", "B", "C", "D", "E", "F"] else "badge-NA"
        status_color = "#15803d" if r['grade_point'] > 0 else "#b91c1c"
        result_text = "PASS" if r['grade_point'] > 0 else ("FAIL" if r['status'] == 'Completed' else "INCOMPLETE")

        row = f"""
        <tr>
          <td class="center"><strong>{r['course_code']}</strong></td>
          <td>{r['title']}</td>
          <td class="center">{r['credits']}</td>
          <td class="center">{r['attendance_pct']}%</td>
          <td class="center">{r['marks']}</td>
          <td class="center"><span class="badge {badge_cls}">{r['letter_grade']}</span></td>
          <td class="center">{r['grade_point']}</td>
          <td class="center" style="color: {status_color}; font-weight: 700;">{result_text}</td>
        </tr>
        """
        rows_html.append(row)

    cgpa = transcript["cgpa"]
    if cgpa >= 9.0:
        status_text = "Passed with First Class with Distinction (Dean's Merit List)"
    elif cgpa >= 7.5:
        status_text = "Passed with First Class"
    elif cgpa >= 6.0:
        status_text = "Passed with Second Class"
    else:
        status_text = "Satisfactory Progress"

    filled_html = HTML_TEMPLATE.format(
        name=student["name"],
        student_id=student["student_id"],
        department=student["department"],
        semester=student["semester"],
        total_registered_credits=transcript["total_registered_credits"],
        total_earned_credits=transcript["total_earned_credits"],
        cgpa=transcript["cgpa"],
        academic_status=status_text,
        table_rows="".join(rows_html),
    )

    out_file = Path(__file__).resolve().parent / f"report_card_{student_id}.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(filled_html)

    print(f"\n[OK] Report card generated successfully: {out_file.name}")
    print(f"     Opening in browser...")
    webbrowser.open(str(out_file.resolve()))
    return out_file


def main():
    if len(sys.argv) > 1:
        sid = sys.argv[1]
    else:
        print("\n=== VIT Bhopal Quick Report Card Generator ===")
        user_input = input("Enter Student ID [Press Enter for 26MIM10152]: ").strip()
        sid = user_input if user_input else "26MIM10152"

    generate_report_card(sid)


if __name__ == "__main__":
    main()
