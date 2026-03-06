"""
╔══════════════════════════════════════════════════════╗
║   AI ATTENDANCE RISK PREDICTOR                       ║
║   Author : B. Siddesh | github.com/BSIDDESH          ║
║   Branch : B.E. AI & ML — East West Institute        ║
║   Built  : March 2026 | The Big Code 2026 Prep       ║
╚══════════════════════════════════════════════════════╝

Features:
  - Subject-wise attendance tracking
  - Subject-wise marks tracking
  - AI risk scoring engine
  - Personalised recommendations
  - Detailed student report
  - Class statistics
  - CSV persistent storage
"""

import csv
import os
from datetime import datetime

# ── Terminal Colours ───────────────────────────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

DATA_FILE = "students.csv"

SUBJECTS = ["Maths", "Physics", "Programming", "DSA", "AI_ML"]

# ══════════════════════════════════════════════════════════════════════════
#  AI RISK ENGINE
# ══════════════════════════════════════════════════════════════════════════

def calculate_subject_risk(attendance_pct, marks):
    """Calculate risk score for a single subject."""
    score = 0
    # Attendance component (0–50 points)
    if attendance_pct < 50:   score += 50
    elif attendance_pct < 65: score += 35
    elif attendance_pct < 75: score += 20
    elif attendance_pct < 85: score += 8
    # Marks component (0–50 points)
    if marks < 35:   score += 50
    elif marks < 50: score += 30
    elif marks < 60: score += 15
    elif marks < 75: score += 5
    return score

def predict_overall_risk(student):
    """
    AI engine: combines subject-wise attendance + marks into an overall risk score.
    Weights subjects equally. Returns risk level and detailed breakdown.
    """
    subject_scores = {}
    for sub in SUBJECTS:
        att  = student[f"{sub}_att"]
        mark = student[f"{sub}_marks"]
        subject_scores[sub] = calculate_subject_risk(att, mark)

    overall = sum(subject_scores.values()) / len(SUBJECTS)

    # Classify
    if overall >= 55:
        risk, col = "HIGH RISK", RED
    elif overall >= 28:
        risk, col = "MEDIUM RISK", YELLOW
    else:
        risk, col = "LOW RISK", GREEN

    return risk, col, overall, subject_scores

def get_grade(marks):
    if marks >= 90: return "O",  GREEN
    if marks >= 75: return "A+", GREEN
    if marks >= 60: return "A",  CYAN
    if marks >= 50: return "B",  YELLOW
    if marks >= 40: return "C",  YELLOW
    return "F", RED

def get_recommendations(risk, student, subject_scores):
    """AI generates targeted recommendations based on weakest subjects."""
    recs = []

    # Sort subjects by risk score (worst first)
    weak = sorted(subject_scores.items(), key=lambda x: x[1], reverse=True)

    if risk == "HIGH RISK":
        recs += [
            f"{RED}URGENT: Your attendance is critically low in multiple subjects!{RESET}",
            f"Immediately meet your class coordinator and subject teachers.",
            f"Check eligibility for attendance condonation before exams.",
        ]
    elif risk == "MEDIUM RISK":
        recs += [
            f"{YELLOW}Warning: You are at risk of being detained.{RESET}",
            f"Stop missing classes immediately — every class counts now.",
        ]
    else:
        recs += [f"{GREEN}Good standing! Keep up the consistency.{RESET}"]

    # Subject-specific tips
    for sub, score in weak[:2]:
        att  = student[f"{sub}_att"]
        mark = student[f"{sub}_marks"]
        if att < 75:
            recs.append(f"  {sub}: Attend ALL remaining {sub} classes (currently {att:.1f}%).")
        if mark < 50:
            recs.append(f"  {sub}: Revise {sub} thoroughly — marks critically low ({mark:.0f}/100).")
        elif mark < 65:
            recs.append(f"  {sub}: Focus on improving {sub} marks through practice tests.")

    recs.append("Join or form a study group for your weakest subjects.")
    recs.append("Use GeeksForGeeks and YouTube for quick concept revision.")

    return recs

# ══════════════════════════════════════════════════════════════════════════
#  CSV STORAGE
# ══════════════════════════════════════════════════════════════════════════

FIELDS = (
    ["name", "roll_no", "branch", "semester", "added_on"]
    + [f"{s}_total" for s in SUBJECTS]
    + [f"{s}_attended" for s in SUBJECTS]
    + [f"{s}_marks" for s in SUBJECTS]
)

def load_students():
    if not os.path.exists(DATA_FILE):
        return []
    students = []
    with open(DATA_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            s = {
                "name"    : row["name"],
                "roll_no" : row["roll_no"],
                "branch"  : row["branch"],
                "semester": row["semester"],
                "added_on": row["added_on"],
            }
            for sub in SUBJECTS:
                total    = int(row[f"{sub}_total"])
                attended = int(row[f"{sub}_attended"])
                s[f"{sub}_total"]    = total
                s[f"{sub}_attended"] = attended
                s[f"{sub}_att"]      = (attended / total * 100) if total > 0 else 0
                s[f"{sub}_marks"]    = float(row[f"{sub}_marks"])
            students.append(s)
    return students

def save_students(students):
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for s in students:
            row = {k: s[k] for k in ["name","roll_no","branch","semester","added_on"]}
            for sub in SUBJECTS:
                row[f"{sub}_total"]    = s[f"{sub}_total"]
                row[f"{sub}_attended"] = s[f"{sub}_attended"]
                row[f"{sub}_marks"]    = s[f"{sub}_marks"]
            writer.writerow(row)

# ══════════════════════════════════════════════════════════════════════════
#  MENU FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_header():
    clear()
    print(f"\n{BLUE}{BOLD}╔══════════════════════════════════════════════════╗{RESET}")
    print(f"{BLUE}{BOLD}║   AI ATTENDANCE RISK PREDICTOR                   ║{RESET}")
    print(f"{BLUE}║   B. Siddesh | github.com/BSIDDESH               ║{RESET}")
    print(f"{BLUE}{BOLD}╚══════════════════════════════════════════════════╝{RESET}\n")

def add_student(students):
    print(f"\n{BOLD}── ADD NEW STUDENT ──────────────────────────────{RESET}")
    name     = input("  Full Name       : ").strip()
    roll_no  = input("  Roll Number     : ").strip()
    branch   = input("  Branch          : ").strip()
    semester = input("  Semester        : ").strip()

    # Check duplicate
    if any(s["roll_no"] == roll_no for s in students):
        print(f"  {RED}Roll number already exists!{RESET}")
        return

    s = {"name": name, "roll_no": roll_no, "branch": branch,
         "semester": semester, "added_on": datetime.now().strftime("%Y-%m-%d")}

    print(f"\n  {BOLD}Enter Subject-wise Details:{RESET}")
    print(f"  {DIM}(For each subject: total classes, attended, marks out of 100){RESET}\n")

    try:
        for sub in SUBJECTS:
            print(f"  {CYAN}{BOLD}{sub}{RESET}")
            total    = int(input(f"    Total Classes : "))
            attended = int(input(f"    Attended      : "))
            marks    = float(input(f"    Marks /100    : "))

            if attended > total:
                print(f"    {RED}Attended cannot exceed total! Setting to total.{RESET}")
                attended = total
            if not (0 <= marks <= 100):
                print(f"    {RED}Marks must be 0-100! Setting to 0.{RESET}")
                marks = 0

            s[f"{sub}_total"]    = total
            s[f"{sub}_attended"] = attended
            s[f"{sub}_att"]      = (attended / total * 100) if total > 0 else 0
            s[f"{sub}_marks"]    = marks
            print()
    except ValueError:
        print(f"  {RED}Invalid input! Student not saved.{RESET}")
        return

    students.append(s)
    save_students(students)

    risk, col, score, _ = predict_overall_risk(s)
    avg_att   = sum(s[f"{sub}_att"] for sub in SUBJECTS) / len(SUBJECTS)
    avg_marks = sum(s[f"{sub}_marks"] for sub in SUBJECTS) / len(SUBJECTS)

    print(f"  {GREEN}✓ Student added!{RESET}")
    print(f"  Avg Attendance : {avg_att:.1f}%")
    print(f"  Avg Marks      : {avg_marks:.1f}/100")
    print(f"  Risk Level     : {col}{BOLD}{risk}{RESET}  (score: {score:.1f})")

def view_all(students):
    if not students:
        print(f"\n  {YELLOW}No students yet. Add some first!{RESET}")
        return
    print(f"\n{BOLD}  {'NAME':<20}{'ROLL':<10}{'SEM':<6}{'AVG ATT%':<11}{'AVG MARKS':<12}RISK{RESET}")
    print(f"  {'─'*65}")
    for s in students:
        risk, col, score, _ = predict_overall_risk(s)
        avg_att   = sum(s[f"{sub}_att"] for sub in SUBJECTS) / len(SUBJECTS)
        avg_marks = sum(s[f"{sub}_marks"] for sub in SUBJECTS) / len(SUBJECTS)
        print(f"  {s['name']:<20}{s['roll_no']:<10}{s['semester']:<6}"
              f"{avg_att:>7.1f}%   {avg_marks:>7.1f}/100   {col}{BOLD}{risk}{RESET}")
    print(f"  {'─'*65}")
    print(f"  Total: {len(students)} students")

def detailed_report(students):
    if not students:
        print(f"\n  {YELLOW}No students found!{RESET}")
        return
    roll = input("\n  Enter Roll Number: ").strip()
    s = next((x for x in students if x["roll_no"] == roll), None)
    if not s:
        print(f"  {RED}Student '{roll}' not found!{RESET}")
        return

    risk, col, score, sub_scores = predict_overall_risk(s)
    recs = get_recommendations(risk, s, sub_scores)
    avg_att   = sum(s[f"{sub}_att"] for sub in SUBJECTS) / len(SUBJECTS)
    avg_marks = sum(s[f"{sub}_marks"] for sub in SUBJECTS) / len(SUBJECTS)

    print(f"\n{BOLD}╔══════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}  AI ANALYSIS REPORT{RESET}")
    print(f"{'═'*52}")
    print(f"  Name     : {BOLD}{s['name']}{RESET}")
    print(f"  Roll No  : {s['roll_no']}   |   Branch: {s['branch']}")
    print(f"  Semester : {s['semester']}           |   Added: {s['added_on']}")
    print(f"{'─'*52}")
    print(f"\n  {BOLD}SUBJECT-WISE BREAKDOWN:{RESET}")
    print(f"  {'Subject':<14}{'Att%':<10}{'Attended':<12}{'Marks':<10}{'Grade':<8}{'Status'}{RESET}")
    print(f"  {'─'*60}")

    for sub in SUBJECTS:
        att   = s[f"{sub}_att"]
        mark  = s[f"{sub}_marks"]
        atnd  = s[f"{sub}_attended"]
        tot   = s[f"{sub}_total"]
        grade, gcol = get_grade(mark)
        att_col = RED if att < 65 else (YELLOW if att < 75 else GREEN)
        status = f"{RED}DANGER{RESET}" if att < 65 else (f"{YELLOW}WARNING{RESET}" if att < 75 else f"{GREEN}OK{RESET}")
        att_bar = "█" * int(att // 10) + "░" * (10 - int(att // 10))
        print(f"  {sub:<14}{att_col}{att:>5.1f}%{RESET}  {atnd}/{tot:<8}  {mark:>5.1f}/100  "
              f"{gcol}{grade}{RESET}  {status}")

    print(f"  {'─'*60}")
    print(f"  {'AVERAGE':<14}{avg_att:>5.1f}%            {avg_marks:>5.1f}/100")
    print(f"\n  {BOLD}OVERALL RISK SCORE  : {col}{score:.1f} / 100{RESET}")
    print(f"  {BOLD}RISK CLASSIFICATION : {col}{BOLD}{risk}{RESET}")
    print(f"\n{'─'*52}")
    print(f"\n  {BOLD}AI RECOMMENDATIONS:{RESET}")
    for i, rec in enumerate(recs, 1):
        print(f"  {i}. {rec}")
    print(f"\n{'═'*52}")

def class_statistics(students):
    if not students:
        print(f"\n  {YELLOW}No data!{RESET}")
        return

    high = medium = low = 0
    sub_att_totals   = {s: 0 for s in SUBJECTS}
    sub_marks_totals = {s: 0 for s in SUBJECTS}
    n = len(students)

    for st in students:
        risk, _, _, _ = predict_overall_risk(st)
        if risk == "HIGH RISK":    high   += 1
        elif risk == "MEDIUM RISK": medium += 1
        else:                       low    += 1
        for sub in SUBJECTS:
            sub_att_totals[sub]   += st[f"{sub}_att"]
            sub_marks_totals[sub] += st[f"{sub}_marks"]

    print(f"\n{BOLD}  CLASS STATISTICS{RESET}")
    print(f"  {'═'*50}")
    print(f"  Total Students  : {n}")
    print(f"\n  {BOLD}Subject-wise Averages:{RESET}")
    print(f"  {'Subject':<14}{'Avg Att%':<12}{'Avg Marks'}")
    print(f"  {'─'*35}")
    for sub in SUBJECTS:
        avg_a = sub_att_totals[sub] / n
        avg_m = sub_marks_totals[sub] / n
        a_col = RED if avg_a < 65 else (YELLOW if avg_a < 75 else GREEN)
        m_col = RED if avg_m < 50 else (YELLOW if avg_m < 60 else GREEN)
        print(f"  {sub:<14}{a_col}{avg_a:>6.1f}%{RESET}     {m_col}{avg_m:>5.1f}/100{RESET}")

    print(f"\n  {BOLD}Risk Distribution:{RESET}")
    for label, count, c in [("High Risk  ", high, RED), ("Medium Risk", medium, YELLOW), ("Low Risk   ", low, GREEN)]:
        bar = "█" * count + "░" * (n - count)
        pct = count / n * 100 if n > 0 else 0
        print(f"  {c}{label}{RESET} : {c}{bar}{RESET} {count}/{n} ({pct:.0f}%)")
    print(f"  {'═'*50}")

def load_sample_data(students):
    sample = [
        {"name":"Arjun Sharma",  "roll_no":"22AI001","branch":"AI&ML","semester":"4","added_on":"2026-01-10",
         "Maths_total":50,"Maths_attended":42,"Maths_marks":78,
         "Physics_total":40,"Physics_attended":34,"Physics_marks":70,
         "Programming_total":55,"Programming_attended":50,"Programming_marks":85,
         "DSA_total":50,"DSA_attended":45,"DSA_marks":80,
         "AI_ML_total":45,"AI_ML_attended":40,"AI_ML_marks":82},
        {"name":"Priya Reddy",   "roll_no":"22AI002","branch":"AI&ML","semester":"4","added_on":"2026-01-10",
         "Maths_total":50,"Maths_attended":22,"Maths_marks":38,
         "Physics_total":40,"Physics_attended":18,"Physics_marks":32,
         "Programming_total":55,"Programming_attended":25,"Programming_marks":48,
         "DSA_total":50,"DSA_attended":20,"DSA_marks":35,
         "AI_ML_total":45,"AI_ML_attended":19,"AI_ML_marks":30},
        {"name":"Rahul Naik",    "roll_no":"22AI003","branch":"AI&ML","semester":"4","added_on":"2026-01-10",
         "Maths_total":50,"Maths_attended":48,"Maths_marks":92,
         "Physics_total":40,"Physics_attended":39,"Physics_marks":88,
         "Programming_total":55,"Programming_attended":54,"Programming_marks":95,
         "DSA_total":50,"DSA_attended":49,"DSA_marks":91,
         "AI_ML_total":45,"AI_ML_attended":44,"AI_ML_marks":90},
        {"name":"B. Siddesh",    "roll_no":"22AI006","branch":"AI&ML","semester":"4","added_on":"2026-03-01",
         "Maths_total":50,"Maths_attended":40,"Maths_marks":78,
         "Physics_total":40,"Physics_attended":32,"Physics_marks":72,
         "Programming_total":55,"Programming_attended":46,"Programming_marks":85,
         "DSA_total":50,"DSA_attended":43,"DSA_marks":80,
         "AI_ML_total":45,"AI_ML_attended":38,"AI_ML_marks":83},
    ]
    for raw in sample:
        s = {k: raw[k] for k in ["name","roll_no","branch","semester","added_on"]}
        for sub in SUBJECTS:
            tot  = raw[f"{sub}_total"]
            atnd = raw[f"{sub}_attended"]
            s[f"{sub}_total"]    = tot
            s[f"{sub}_attended"] = atnd
            s[f"{sub}_att"]      = (atnd / tot * 100) if tot > 0 else 0
            s[f"{sub}_marks"]    = float(raw[f"{sub}_marks"])
        students.append(s)
    save_students(students)
    print(f"\n  {GREEN}✓ Sample data loaded! {len(sample)} students added.{RESET}")

# ══════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════
def main():
    students = load_students()
    while True:
        print_header()
        print(f"  {BOLD}MAIN MENU{RESET}")
        print(f"  {'─'*38}")
        print(f"  1.  Add New Student")
        print(f"  2.  View All Students (Risk Summary)")
        print(f"  3.  Detailed AI Report for a Student")
        print(f"  4.  Class Statistics Overview")
        print(f"  5.  Load Sample Data (demo mode)")
        print(f"  6.  Exit")
        print(f"  {'─'*38}")

        choice = input(f"\n  Enter choice (1-6): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_all(students)
        elif choice == "3":
            detailed_report(students)
        elif choice == "4":
            class_statistics(students)
        elif choice == "5":
            load_sample_data(students)
            students = load_students()
        elif choice == "6":
            print(f"\n  {GREEN}Goodbye! — B. Siddesh | github.com/BSIDDESH{RESET}\n")
            break
        else:
            print(f"  {RED}Invalid! Enter 1-6.{RESET}")

        input(f"\n  {BLUE}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    main()
