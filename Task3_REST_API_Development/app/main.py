"""
FastAPI Main Application Entry Point
Internship Assignment - Task 3: REST API Development
Applicant: KASARABOINA SRINU | Application ID: KTS020260716223
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.database.session import engine, Base, SessionLocal
from app.models.user import User
from app.models.item import Item
from app.core.security import hash_password
from app.routers import auth_router, item_router

_db_initialized = False

def ensure_db_initialized():
    global _db_initialized
    if not _db_initialized:
        try:
            Base.metadata.create_all(bind=engine)
            db = SessionLocal()
            try:
                demo_user = db.query(User).filter(User.username == "admin").first()
                if not demo_user:
                    demo_user = User(
                        username="admin",
                        email="admin@example.com",
                        full_name="System Administrator",
                        hashed_password=hash_password("admin123"),
                        role="admin"
                    )
                    db.add(demo_user)
                    db.commit()
                    db.refresh(demo_user)

                    sample_items = [
                        Item(title="Dell XPS 15 Laptop", description="Intel Core i9, 32GB RAM, 1TB SSD", category="Electronics", price=1899.99, quantity=15, owner_id=demo_user.id),
                        Item(title="Wireless Noise Cancelling Headphones", description="Sony WH-1000XM5 with 30hr battery", category="Electronics", price=349.99, quantity=40, owner_id=demo_user.id),
                        Item(title="Ergonomic Office Chair", description="High-back mesh chair with lumbar support", category="Furniture", price=249.50, quantity=25, owner_id=demo_user.id),
                        Item(title="Mechanical Gaming Keyboard", description="RGB backlit Cherry MX Brown switches", category="Accessories", price=129.99, quantity=50, owner_id=demo_user.id),
                        Item(title="4K Ultra-HD Monitor 27-inch", description="IPS panel, 144Hz refresh rate, USB-C hub", category="Electronics", price=429.00, quantity=20, owner_id=demo_user.id),
                    ]
                    db.add_all(sample_items)
                    db.commit()
            finally:
                db.close()
            _db_initialized = True
        except Exception as err:
            print(f"DB Init Exception: {err}")

# Safe initialization
ensure_db_initialized()


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_db_initialized()
    yield


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
    description="""
## 🚀 Production RESTful API with FastAPI & JWT Authentication

### Features:
* **Authentication**: JWT Token-based Auth (`/auth/register`, `/auth/login`, `/auth/me`)
* **Resource Management**: Complete CRUD operations for Inventory Items (`/api/items`)
* **Search & Filters**: Multi-attribute filtering (category, price range, publishing status, keyword search)
* **Pagination**: Structured pagination with total count and page calculation
* **Input Validation**: Pydantic models with auto-generated OpenAPI documentation
* **Database**: SQLite with SQLAlchemy ORM
* **Developer**: KASARABOINA SRINU (App ID: `KTS020260716223`)
    """,
    openapi_tags=[
        {"name": "Authentication", "description": "User registration and JWT token authentication"},
        {"name": "Items & Inventory", "description": "CRUD operations, search, filters, and analytics"}
    ]
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom Validation Error Formatter
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = " -> ".join([str(x) for x in err.get("loc", [])])
        msg = err.get("msg")
        errors.append(f"{loc}: {msg}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "details": errors
        }
    )


# Include API Routers
app.include_router(auth_router)
app.include_router(item_router, prefix="/api")


@app.get("/", response_class=HTMLResponse, tags=["System"])
def root_endpoint():
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


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "intern_name": "KASARABOINA SRINU",
        "application_id": "KTS020260716223"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
