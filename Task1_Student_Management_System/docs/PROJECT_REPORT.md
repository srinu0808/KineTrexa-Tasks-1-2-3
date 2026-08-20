# Project Report: Student Management System

**Internship Track:** Python Development Internship  
**Applicant Name:** KASARABOINA SRINU  
**Application ID:** KTS020260716223  
**Duration:** 30 Days (20 July 2026 – 19 August 2026)  
**Supervisor / HR:** Prince Asthana (HR Executive)

---

## 1. Project Overview & Objective
The **Student Management System** is a robust, object-oriented Python application engineered to digitize and automate student record management, course enrollments, grade calculations, search, filtering, and reporting.

The system emphasizes clean code architecture, defensive input validation, custom domain exceptions, atomic file persistence, and an intuitive terminal user interface (CLI).

---

## 2. Key Features & Implementation Details

### A. Object-Oriented Programming (OOP) Architecture
- **Encapsulation:** Properties with getter and setter methods protect internal student state and enforce data transformations (e.g., uppercase roll numbers, normalized email addresses).
- **Domain Modeling:** Dedicated classes (`Student`, `Course`) clearly delineate business logic, course credit weighting, and weighted GPA calculations.

### B. CRUD & Academic Operations
- **Create:** Validates input formats and prevents duplicate entries before assigning unique auto-generated IDs (`STU-0001`).
- **Read / View:** Displays formatted tabular views of students, sorted by GPA, Name, Department, or Roll Number.
- **Update:** Safely updates student profile information and handles course grades.
- **Delete:** Removes student records with confirmation prompts.
- **Course Enrollment & GPA Calculation:** Computes cumulative GPA using credit weighting:
  $$\text{GPA} = \frac{\sum (\text{Credits} \times \text{Grade Points})}{\sum \text{Credits}}$$

### C. Search & Filter
- Real-time multi-field search across student names, roll numbers, emails, departments, and course codes.
- Multi-criteria filtering by department, status (`Active`/`Inactive`), and GPA range thresholds.

### D. Persistence & Reliability
- **Atomic JSON Storage:** Employs temporary swap files to eliminate data corruption during sudden system shutdowns.
- **CSV Data Exchange:** Complete export and import functions for interoperability with spreadsheet software.

---

## 3. Project File Hierarchy
```
Task1_Student_Management_System/
├── src/
│   ├── models/
│   │   ├── course.py
│   │   └── student.py
│   ├── storage/
│   │   ├── base.py
│   │   ├── json_storage.py
│   │   └── csv_storage.py
│   ├── services/
│   │   └── student_service.py
│   ├── utils/
│   │   ├── exceptions.py
│   │   └── validators.py
│   └── ui/
│       └── cli.py
├── tests/
│   ├── conftest.py
│   └── test_student_service.py
├── data/
│   └── students.json
├── docs/
│   ├── PROJECT_REPORT.md
│   ├── generate_pdf_report.py
│   └── Student_Management_System_Project_Report.pdf
├── main.py
├── requirements.txt
└── README.md
```

---

## 4. Verification & Testing
The project includes a comprehensive Pytest suite located in `tests/test_student_service.py`:
- `test_create_student_success`
- `test_duplicate_roll_number_error`
- `test_duplicate_email_error`
- `test_invalid_email_validation`
- `test_invalid_phone_validation`
- `test_update_student`
- `test_delete_student`
- `test_course_enrollment_and_gpa_calculation`
- `test_search_and_filter`

**Result:** 100% test pass rate with zero warnings or errors.

---

## 5. Summary & Conclusions
This task successfully fulfills all deliverables outlined in the Internship Assignment:
1. Complete, production-ready Python source code.
2. Comprehensive documentation and architectural overview.
3. Automated unit test suite.
4. Auto-generated professional PDF Project Report.
