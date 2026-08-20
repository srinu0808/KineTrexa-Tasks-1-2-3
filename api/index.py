"""
Vercel Serverless Function Entry Point for FastAPI REST API
"""
import sys
import os

# Add current directory and api directory to sys.path
api_dir = os.path.dirname(os.path.abspath(__file__))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

from app.main import app
from fastapi.responses import HTMLResponse

# Rich landing dashboard for Vercel deployment root
@app.get("/", response_class=HTMLResponse, tags=["Landing"])
def landing_page():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Development Internship - Live Deployment</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: #0f172a; color: #f8fafc; font-family: 'Segoe UI', system-ui, sans-serif; min-height: 100vh; }
        .hero-card { background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; backdrop-filter: blur(10px); }
        .task-card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; transition: transform 0.2s, border-color 0.2s; }
        .task-card:hover { transform: translateY(-4px); border-color: #38bdf8; }
        .badge-custom { background: #0284c7; color: white; padding: 6px 12px; border-radius: 20px; font-weight: 500; }
        .btn-custom { background: linear-gradient(135deg, #0284c7, #2563eb); border: none; color: white; padding: 10px 24px; border-radius: 8px; font-weight: 600; text-decoration: none; display: inline-block; }
        .btn-custom:hover { background: linear-gradient(135deg, #0369a1, #1d4ed8); color: white; }
    </style>
</head>
<body class="py-5">
    <div class="container">
        <div class="hero-card p-5 mb-5 text-center shadow-lg">
            <span class="badge-custom mb-3 d-inline-block"><i class="fas fa-certificate me-2"></i>Python Development Internship Assignment</span>
            <h1 class="display-5 fw-bold text-white mb-2">Live Production Deployment</h1>
            <p class="lead text-secondary mb-4">Enterprise REST API & Automation Project Suite</p>
            
            <div class="row justify-content-center g-3 mb-4 text-start">
                <div class="col-md-5">
                    <div class="p-3 bg-dark bg-opacity-50 rounded-3 border border-secondary border-opacity-25">
                        <small class="text-muted d-block">Applicant Name</small>
                        <strong class="text-light fs-5">KASARABOINA SRINU</strong>
                    </div>
                </div>
                <div class="col-md-5">
                    <div class="p-3 bg-dark bg-opacity-50 rounded-3 border border-secondary border-opacity-25">
                        <small class="text-muted d-block">Application ID</small>
                        <strong class="text-info fs-5">KTS020260716223</strong>
                    </div>
                </div>
            </div>

            <div class="d-flex flex-wrap justify-content-center gap-3">
                <a href="/docs" class="btn-custom"><i class="fas fa-bolt me-2"></i>Interactive Swagger UI</a>
                <a href="/redoc" class="btn btn-outline-light px-4 py-2"><i class="fas fa-book me-2"></i>ReDoc API Specs</a>
                <a href="/health" class="btn btn-outline-success px-4 py-2"><i class="fas fa-heartbeat me-2"></i>Health Check</a>
            </div>
        </div>

        <h3 class="fw-bold mb-4 text-center text-white"><i class="fas fa-layer-group me-2 text-info"></i>Completed Internship Tasks</h3>

        <div class="row g-4">
            <!-- Task 3 -->
            <div class="col-md-4">
                <div class="task-card p-4 h-100 d-flex flex-column">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <span class="badge bg-primary">Task 3</span>
                        <span class="text-success small"><i class="fas fa-check-circle me-1"></i>Live API</span>
                    </div>
                    <h5 class="text-white fw-bold">REST API Development</h5>
                    <p class="text-secondary small flex-grow-1">FastAPI RESTful service with JWT Bearer authentication, SQLAlchemy ORM with SQLite, Pydantic v2 schemas, and CRUD inventory management.</p>
                    <a href="/docs" class="btn btn-sm btn-outline-primary mt-3 w-100"><i class="fas fa-code me-1"></i>Try Endpoints in Swagger</a>
                </div>
            </div>

            <!-- Task 1 -->
            <div class="col-md-4">
                <div class="task-card p-4 h-100 d-flex flex-column">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <span class="badge bg-info">Task 1</span>
                        <span class="text-success small"><i class="fas fa-check-circle me-1"></i>Complete</span>
                    </div>
                    <h5 class="text-white fw-bold">Student Management System</h5>
                    <p class="text-secondary small flex-grow-1">Comprehensive OOP-based student academic records manager with dual JSON/CSV persistence, weighted GPA calculation, search & filters, and PDF report generation.</p>
                    <a href="/api/items" class="btn btn-sm btn-outline-info mt-3 w-100"><i class="fas fa-file-alt me-1"></i>View Items API</a>
                </div>
            </div>

            <!-- Task 2 -->
            <div class="col-md-4">
                <div class="task-card p-4 h-100 d-flex flex-column">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <span class="badge bg-warning text-dark">Task 2</span>
                        <span class="text-success small"><i class="fas fa-check-circle me-1"></i>Complete</span>
                    </div>
                    <h5 class="text-white fw-bold">Library Management System</h5>
                    <p class="text-secondary small flex-grow-1">Book catalog, patron member management, 14-day loan lifecycle tracking, overdue fine calculation engine, and system analytics.</p>
                    <a href="/api/items/stats/summary" class="btn btn-sm btn-outline-warning mt-3 w-100"><i class="fas fa-chart-pie me-1"></i>View API Analytics</a>
                </div>
            </div>
        </div>

        <footer class="mt-5 text-center text-secondary small">
            <p>Python Development Internship • Candidate: Kasaraboina Srinu (ID: KTS020260716223) • Supervisor: Prince Asthana</p>
        </footer>
    </div>
</body>
</html>
    """
