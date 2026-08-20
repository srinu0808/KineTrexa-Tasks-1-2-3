<div align="center">

# 🚀 Python Development Internship – Task Assignment

### Complete Multi-Project Repository & Live Serverless Deployment on Vercel

[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Vercel Deployment](https://img.shields.io/badge/Deployment-Vercel%20Live-black?logo=vercel&logoColor=white)](https://python-internship-projects.vercel.app)
[![Tests Status](https://img.shields.io/badge/Tests-18%2F18%20Passed%20(100%25)-success?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 👨‍💻 Candidate & Internship Details

| Parameter | Details |
|---|---|
| **Applicant Name** | **KASARABOINA SRINU** |
| **Application ID** | **`KTS020260716223`** |
| **Internship Domain** | **Python Development Internship** |
| **Internship Duration** | **30 Days (20 July 2026 – 19 August 2026)** |
| **Supervisor / HR Executive** | **Prince Asthana** |
| **Live Production URL** | **[https://python-internship-projects.vercel.app](https://python-internship-projects.vercel.app)** |

---

## 🌐 Live Production Deployment (Vercel)

The REST API and Project Dashboard are deployed live on **Vercel Serverless Functions**:

* 🌍 **Live Project Dashboard:** [https://python-internship-projects.vercel.app](https://python-internship-projects.vercel.app)
* ⚡ **Interactive Swagger UI (API Docs):** [https://python-internship-projects.vercel.app/docs](https://python-internship-projects.vercel.app/docs)
* 📖 **ReDoc API Documentation:** [https://python-internship-projects.vercel.app/redoc](https://python-internship-projects.vercel.app/redoc)
* 🩺 **API Health Check:** [https://python-internship-projects.vercel.app/health](https://python-internship-projects.vercel.app/health)
* 📦 **Live Inventory Resource API:** [https://python-internship-projects.vercel.app/api/items](https://python-internship-projects.vercel.app/api/items)

---

## 🏆 Completed Assigned Tasks

Per the internship requirement (*"You must complete any 2 tasks from the list below"*), this repository includes **Task 1**, **Task 3**, and **Task 2 (Bonus)** built with industry-standard architecture, unit test coverage, and documentation:

### 1. 🎓 Task 1: Student Management System
* **Domain & Architecture:** Object-Oriented Programming (OOP) with encapsulated `Student` and `Course` domain models.
* **Core Capabilities:** Full CRUD operations, dynamic weighted GPA calculation, keyword search, multi-field filtering, duplicate roll number/email prevention.
* **Storage Engine:** Dual persistence support with atomic JSON swap-file storage and CSV export/import.
* **Deliverables:** CLI interface, Pytest suite (9 tests passing), Project Report markdown and auto-generated PDF report via ReportLab.

### 2. 🌐 Task 3: REST API Development
* **Framework:** **FastAPI** + **SQLAlchemy ORM (SQLite)** + **Pydantic v2** + **PyJWT**.
* **Security:** JWT Bearer authentication, PBKDF2-SHA256 password hashing, protected routes (`/auth/register`, `/auth/login`, `/auth/me`).
* **CRUD & Resource Management:** Inventory items management (`/api/items`), query parameter filtering (category, price range, publishing status), pagination, and inventory analytics summary (`/api/items/stats/summary`).
* **Deliverables:** Live Vercel deployment, Swagger UI (`/docs`), Postman Collection v2.1 export, async unit tests (5 tests passing), technical API docs.

### 3. 📚 Task 2 (Bonus): Library Management System
* **Features:** Catalog tracking for book copies, patron member borrowing quotas, 14-day loan lifecycle tracking, and automatic overdue fine computation ($2/day).
* **Deliverables:** Interactive CLI, Pytest suite (4 tests passing), PDF project report, and documentation.

---

## 📂 Repository File Structure

```
.
├── api/                                          # Vercel Serverless Function entrypoint
│   ├── app/                                      # Packaged FastAPI application for Vercel
│   └── index.py                                  # Serverless handler & landing page
│
├── Task1_Student_Management_System/              # Task 1: Student Management System
│   ├── student_mgmt/
│   │   ├── models/                               # Student & Course OOP models
│   │   ├── storage/                              # Atomic JSON & CSV storage handlers
│   │   ├── services/                             # Business logic & analytics
│   │   ├── utils/                                # Regex validators & custom exceptions
│   │   └── ui/                                   # Colorized CLI interface
│   ├── tests/                                    # Pytest unit tests (9 tests)
│   ├── data/                                     # Persistent JSON data
│   ├── docs/
│   │   ├── PROJECT_REPORT.md                     # Markdown Project Report
│   │   ├── generate_pdf_report.py                # PDF Report Generator
│   │   └── Student_Management_System_Project_Report.pdf
│   ├── main.py                                   # Entry point with seed data
│   ├── requirements.txt                          # Task 1 dependencies
│   └── README.md                                 # Task 1 documentation
│
├── Task3_REST_API_Development/                   # Task 3: REST API Development
│   ├── app/
│   │   ├── core/                                 # Security (JWT, PBKDF2) & App Settings
│   │   ├── database/                             # SQLAlchemy session & SQLite engine
│   │   ├── models/                               # User & Item SQLAlchemy ORM models
│   │   ├── schemas/                              # Pydantic v2 validation models
│   │   ├── routers/                              # Auth & Items API routers
│   │   ├── services/                             # Auth & Item business logic
│   │   └── main.py                               # FastAPI application
│   ├── tests/                                    # Async integration tests (5 tests)
│   ├── postman/
│   │   └── REST_API_Postman_Collection.json      # Postman Collection v2.1 for testing
│   ├── docs/
│   │   └── API_DOCUMENTATION.md                  # Comprehensive API technical specs
│   ├── requirements.txt                          # Task 3 dependencies
│   └── README.md                                 # Task 3 documentation
│
├── Task2_Library_Management_System/              # Task 2: Library Management System
│   ├── library_mgmt/
│   │   ├── models/                               # Book, Member, Transaction models
│   │   ├── storage/                              # JSON storage handler
│   │   ├── services/                             # Loan lifecycle & fine calculation
│   │   └── ui/                                   # Interactive CLI
│   ├── tests/                                    # Pytest unit tests (4 tests)
│   ├── docs/
│   │   ├── PROJECT_REPORT.md
│   │   ├── generate_pdf_report.py
│   │   └── Library_Management_System_Project_Report.pdf
│   ├── main.py                                   # Entry point
│   ├── requirements.txt                          # Task 2 dependencies
│   └── README.md                                 # Task 2 documentation
│
├── vercel.json                                   # Vercel deployment configuration
├── requirements.txt                              # Root runtime dependencies
├── SUBMISSION_OVERVIEW.md                        # Master internship submission document
└── README.md                                     # Main repository guide
```

---

## 🧪 Automated Testing & Verification

All automated tests across all project suites execute with a **100% pass rate** (**18 out of 18 passed**):

```bash
# Run all workspace tests simultaneously
python -m pytest Task1_Student_Management_System/tests Task3_REST_API_Development/tests Task2_Library_Management_System/tests -v
```

### Test Results Breakdown:
* **Task 1 (Student Management):** 9 / 9 passed (`test_create_student_success`, `test_duplicate_roll_number_error`, `test_duplicate_email_error`, `test_invalid_email_validation`, `test_invalid_phone_validation`, `test_update_student`, `test_delete_student`, `test_course_enrollment_and_gpa_calculation`, `test_search_and_filter`)
* **Task 3 (REST API):** 5 / 5 passed (`test_health_check`, `test_user_registration_and_duplicate_check`, `test_login_and_jwt_token`, `test_crud_items_lifecycle`, `test_unauthorized_access`)
* **Task 2 (Library Management):** 4 / 4 passed (`test_add_and_search_books`, `test_member_registration`, `test_issue_and_return_workflow`, `test_fine_calculation_on_overdue`)

---

## 🚀 How to Run Locally

### 1. Prerequisites
* Python 3.11 or higher installed
* Git

### 2. Setup Virtual Environment
```bash
# Clone the repository
git clone <your-repository-url>
cd <repository-folder>

# Create and activate a virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

---

### 3. Running Task 1 (Student Management System)
```bash
cd Task1_Student_Management_System
python main.py
```
*To re-generate the PDF report:*
```bash
python docs/generate_pdf_report.py
```

---

### 4. Running Task 3 (REST API Development)
```bash
cd Task3_REST_API_Development
uvicorn app.main:app --reload --port 8000
```
* Access Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Access ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### 5. Running Task 2 (Library Management System)
```bash
cd Task2_Library_Management_System
python main.py
```
*To re-generate the PDF report:*
```bash
python docs/generate_pdf_report.py
```

---

## 📮 Postman Collection Import

To test the REST API in Postman:
1. Open Postman.
2. Click **Import** (top left).
3. Select the file: [`Task3_REST_API_Development/postman/REST_API_Postman_Collection.json`](Task3_REST_API_Development/postman/REST_API_Postman_Collection.json).
4. Run requests against `https://python-internship-projects.vercel.app` or `http://127.0.0.1:8000`.

---

## ☁️ How Vercel Deployment Works

This repository is configured to run FastAPI as a Serverless Python Function on Vercel:
1. **`vercel.json`**: Configures rewrites directing all HTTP traffic to `/api/index.py`.
2. **`api/index.py`**: Boots the FastAPI ASGI application with automated `/tmp` SQLite database support for serverless ephemeral environments.
3. **`requirements.txt`**: Declares dependencies (`fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `email-validator`, `pyjwt`).

Deploy anytime via Vercel CLI:
```bash
vercel --prod
```

---

## 📄 License & Attribution

Developed by **KASARABOINA SRINU** (Application ID: `KTS020260716223`) as part of the **Python Development Internship** under the supervision of **Prince Asthana (HR Executive)**. Released under the MIT License.
