"""
Application Configuration Settings
"""
import os

def _resolve_database_url() -> str:
    if os.getenv("DATABASE_URL"):
        return os.getenv("DATABASE_URL")
    # On Linux/Vercel serverless environments /tmp is the writable storage
    if os.name != "nt" or os.getenv("VERCEL") or os.getenv("VERCEL_ENV") or os.path.exists("/tmp"):
        return "sqlite:////tmp/app.db"
    # Local Windows fallback
    local_db = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app.db'))
    return f"sqlite:///{local_db}"

class Settings:
    PROJECT_NAME: str = "Enterprise Item & Inventory REST API"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Security & JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-internship-jwt-key-2026-kts020260716223")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 Hours
    
    # Database
    DATABASE_URL: str = _resolve_database_url()

settings = Settings()
