"""
FastAPI Main Application
Entry point cho HR & Payroll Dashboard Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from .database.connections import db_manager
from .modules.hr_management.routes import router as hr_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="HR & Payroll Dashboard API",
    description="Integrated HR & Payroll Management System - Module A: HR Management",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:5174").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Startup và Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize database connections on startup"""
    print("🚀 Starting HR & Payroll Dashboard API...")
    db_manager.init_databases()
    
    # Test connections
    if db_manager.test_connections():
        print("✅ All database connections ready")
    else:
        print("⚠️  Warning: Some database connections failed")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 Shutting down HR & Payroll Dashboard API...")


# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/")
def read_root():
    """Root endpoint với API information"""
    return {
        "message": "HR & Payroll Dashboard API",
        "version": "1.0.0",
        "module": "A - HR Management",
        "status": "running",
        "docs": "/api/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": {
            "sql_server": "connected" if db_manager.sql_server_engine else "disconnected",
            "mysql": "connected" if db_manager.mysql_engine else "disconnected"
        }
    }


# ============================================================================
# Include Routers
# ============================================================================

# HR Management Routes
app.include_router(hr_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
