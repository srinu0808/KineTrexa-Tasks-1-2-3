# 🎓 Python Development Internship - Task Assignment Submission

**Applicant Name:** KASARABOINA SRINU  
**Application ID:** KTS020260716223  
**Domain:** Python Development Internship  
**Internship Duration:** 30 Days (20 July 2026 – 19 August 2026)  
**Supervisor / HR Executive:** Prince Asthana  

---

## 🌐 Live Production Deployment

* **Live Web Application & API Dashboard:** [https://python-internship-projects.vercel.app](https://python-internship-projects.vercel.app)
* **Interactive Swagger UI (API Docs):** [https://python-internship-projects.vercel.app/docs](https://python-internship-projects.vercel.app/docs)
* **ReDoc API Documentation:** [https://python-internship-projects.vercel.app/redoc](https://python-internship-projects.vercel.app/redoc)
* **System Health Check:** [https://python-internship-projects.vercel.app/health](https://python-internship-projects.vercel.app/health)
* **Items Resource API (Live Data):** [https://python-internship-projects.vercel.app/api/items](https://python-internship-projects.vercel.app/api/items)

---

## 🏆 Summary of Completed Tasks

Per assignment guidelines (*"You must complete any 2 tasks from the list below"*), we have fully implemented, tested, and documented **Task 1**, **Task 3**, and **Task 2 (Bonus)**:

| Task # | Project Name | Tech Stack | Status | Deliverables Completed |
|---|---|---|---|---|
| **Task 1** | **Student Management System** | Python 3.11, OOP, JSON/CSV Storage, ReportLab, Pytest | **COMPLETED (100%)** | Source Code, CLI, Pytest suite (9/9 passed), README, PDF Project Report |
| **Task 3** | **REST API Development** | FastAPI, JWT Auth, SQLAlchemy, SQLite, Pydantic v2, Pytest | **COMPLETED & DEPLOYED (100%)** | Source Code, Live Vercel Deployment, Swagger UI (`/docs`), Pytest suite (5/5 passed), Postman Collection, README |
| **Task 2** | **Library Management System** *(Bonus)* | Python 3.11, OOP, Fines Engine, ReportLab, Pytest | **COMPLETED (100%)** | Source Code, CLI, Pytest suite (4/4 passed), README, PDF Project Report |

---

## 📁 Repository Directory Structure

```
ai projects/
├── Task1_Student_Management_System/
│   ├── student_mgmt/
│   │   ├── models/ (student.py, course.py)
│   │   ├── storage/ (json_storage.py, csv_storage.py)
│   │   ├── services/ (student_service.py)
│   │   ├── utils/ (validators.py, exceptions.py)
│   │   └── ui/ (cli.py)
│   ├── tests/ (test_student_service.py)
│   ├── data/ (students.json)
│   ├── docs/ (PROJECT_REPORT.md, generate_pdf_report.py, Student_Management_System_Project_Report.pdf)
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
│
├── Task3_REST_API_Development/
│   ├── app/
│   │   ├── core/ (config.py, security.py - JWT & PBKDF2)
│   │   ├── database/ (session.py - SQLAlchemy)
│   │   ├── models/ (user.py, item.py)
│   │   ├── schemas/ (user_schema.py, item_schema.py - Pydantic v2)
│   │   ├── routers/ (auth_router.py, item_router.py)
│   │   ├── services/ (auth_service.py, item_service.py)
│   │   └── main.py (FastAPI Application)
│   ├── tests/ (test_api.py)
│   ├── postman/ (REST_API_Postman_Collection.json)
│   ├── docs/ (API_DOCUMENTATION.md)
│   ├── requirements.txt
│   └── README.md
│
├── Task2_Library_Management_System/
│   ├── library_mgmt/
│   │   ├── models/ (book.py, member.py, transaction.py)
│   │   ├── storage/ (json_storage.py)
│   │   ├── services/ (library_service.py)
│   │   └── ui/ (cli.py)
│   ├── tests/ (test_library.py)
│   ├── data/ (library_data.json)
│   ├── docs/ (PROJECT_REPORT.md, generate_pdf_report.py, Library_Management_System_Project_Report.pdf)
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
│
├── api/ (Vercel Serverless Function entrypoint)
├── vercel.json
├── requirements.txt
└── SUBMISSION_OVERVIEW.md
```

---

## 🧪 Automated Test Verification

All automated tests across all projects execute with a **100% pass rate** (18 out of 18 tests):

```bash
# Run all workspace tests simultaneously
python -m pytest Task1_Student_Management_System/tests Task3_REST_API_Development/tests Task2_Library_Management_System/tests -v
```

---

## 📄 Generated PDF Project Reports
1. `Task1_Student_Management_System/docs/Student_Management_System_Project_Report.pdf`
2. `Task2_Library_Management_System/docs/Library_Management_System_Project_Report.pdf`

---

## 📮 Postman Collection
Import the collection directly into Postman to test all REST API endpoints:
- File: `Task3_REST_API_Development/postman/REST_API_Postman_Collection.json`
