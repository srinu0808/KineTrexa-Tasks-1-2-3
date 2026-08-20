# 🎓 Student Management System (Python OOP & Persistence)

> **Python Development Internship - Task 1**  
> **Applicant Name:** KASARABOINA SRINU  
> **Application ID:** KTS020260716223  
> **Duration:** 30 Days (20 July 2026 – 19 August 2026)

---

## 📌 Project Overview
The **Student Management System** is a full-featured, object-oriented application designed to manage student academic records, courses, grades, and analytics. It features clean architecture, atomic file storage, defensive data validation, custom exceptions, and an interactive menu-driven command-line interface (CLI).

---

## 🚀 Key Features
- ✅ **OOP Architecture:** Domain modeling with `Student` and `Course` classes, encapsulation, data validation, and custom methods.
- ✅ **Full CRUD Operations:** Add, view, update, and delete student records safely.
- ✅ **Course & GPA Tracking:** Dynamically calculate weighted GPA based on credit hours and grade points.
- ✅ **Search & Filter:** Search by name, roll number, department, or email. Filter by department, status, or GPA range.
- ✅ **Analytics & Insights:** View departmental breakdowns, active/inactive counts, class average GPA, and top academic performers.
- ✅ **Robust Persistence:** Atomic JSON file storage with temporary swap safety, plus CSV export and import.
- ✅ **Input Validation & Exception Handling:** Strict validation for emails, phone numbers, roll numbers, and grades with custom exceptions.
- ✅ **Automated Unit Tests:** Complete test suite using `pytest`.
- ✅ **PDF Project Report Generator:** Automated PDF report generation using `ReportLab`.

---

## 📂 Project Structure
```
Task1_Student_Management_System/
├── src/
│   ├── models/
│   │   ├── course.py          # Course entity and grading
│   │   └── student.py         # Student entity with GPA calculations
│   ├── storage/
│   │   ├── base.py            # Abstract Base Storage
│   │   ├── json_storage.py    # Atomic JSON persistence
│   │   └── csv_storage.py     # CSV export & import
│   ├── services/
│   │   └── student_service.py # Business logic & analytics
│   ├── utils/
│   │   ├── exceptions.py      # Custom domain exceptions
│   │   └── validators.py      # Regex & range validators
│   └── ui/
│       └── cli.py             # Menu-driven terminal interface
├── tests/
│   ├── conftest.py
│   └── test_student_service.py# Pytest unit tests
├── data/
│   └── students.json          # Persistent JSON storage
├── docs/
│   ├── PROJECT_REPORT.md      # Detailed Project Report
│   ├── generate_pdf_report.py # PDF report generator
│   └── Student_Management_System_Project_Report.pdf
├── main.py                    # Application Entry Point
├── requirements.txt           # Project Dependencies
└── README.md                  # Documentation
```

---

## 🛠️ Installation & Setup

1. **Clone the repository / Navigate to the folder:**
   ```bash
   cd Task1_Student_Management_System
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python main.py
   ```

4. **Run Unit Tests:**
   ```bash
   python -m pytest tests -v
   ```

5. **Generate the PDF Report:**
   ```bash
   python docs/generate_pdf_report.py
   ```

---

## 📊 Sample CLI Menu
```text
========================================================================
   🎓 STUDENT MANAGEMENT SYSTEM - PYTHON OOP & PERSISTENCE
   Intern: KASARABOINA SRINU | App ID: KTS020260716223
========================================================================
Main Menu:
  1. Add Student Record
  2. View All Students
  3. Search Students
  4. Filter Students (by Dept, GPA, Status)
  5. View Student Profile & Enrolled Courses
  6. Update Student Details
  7. Manage Courses & Grades (GPA Calculation)
  8. Delete Student Record
  9. View System Analytics & Reports
  10. CSV Data Export / Import
  0. Exit
```
