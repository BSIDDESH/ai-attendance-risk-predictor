# 🎓 AI Attendance Risk Predictor

> A Python CLI tool with a rule-based AI engine that tracks **subject-wise attendance and marks** to predict student risk levels and generate personalised recommendations.

**Author:** B. Siddesh | [github.com/BSIDDESH](https://github.com/BSIDDESH)  
**Built for:** Google — The Big Code 2026

---

## 🚀 Features

- ✅ **Subject-wise attendance tracking** — Maths, Physics, Programming, DSA, AI & ML
- ✅ **Subject-wise marks tracking** — per subject out of 100
- ✅ **AI Risk Engine** — combines attendance + marks into a risk score
- ✅ Predicts **HIGH / MEDIUM / LOW** risk per student
- ✅ **Detailed AI Report** with subject breakdown and grade (O/A+/A/B/C/F)
- ✅ Personalised recommendations targeting the weakest subjects
- ✅ Class-wide statistics with risk distribution bar chart
- ✅ Persistent **CSV storage** — data saved between sessions
- ✅ Sample data loader for instant demo

---

## 🧠 How the AI Works

For each subject, the engine calculates a **risk score (0–100)** combining:

| Factor | Max Points |
|--------|-----------|
| Attendance % | 50 |
| Marks / 100 | 50 |

The **overall risk** is the average across all 5 subjects:

| Score | Risk Level |
|-------|-----------|
| 55–100 | 🔴 HIGH RISK |
| 28–54  | 🟡 MEDIUM RISK |
| 0–27   | 🟢 LOW RISK |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3 | Core language |
| CSV module | Persistent data storage |
| OS / Datetime | Cross-platform terminal + timestamps |

**No pip install needed — runs on pure Python 3!**

---

## ▶️ How to Run

```bash
git clone https://github.com/BSIDDESH/ai-attendance-risk-predictor.git
cd ai-attendance-risk-predictor
python main.py
```

---

## 📂 Project Structure

```
ai-attendance-risk-predictor/
├── main.py        # Full application
├── students.csv   # Auto-generated on first run
└── README.md
```

---

## 🎯 What I Learned

- Rule-based AI scoring engine design
- Subject-wise data modelling in Python
- CSV file handling and persistent storage
- Terminal UI with ANSI colour codes
- Modular Python project structure

---

⭐ Star this repo if you found it useful!
