"""
Space Catalog API - FastAPI Application
Professional backend for live astronomical data streaming
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from loguru import logger
import sys
import os
from pathlib import Path

from config import settings
from services.cache_service import cache_service
from routes.stars_api import router as stars_router


# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL
)

# Create logs directory
Path("logs").mkdir(exist_ok=True)
logger.add(
    settings.LOG_FILE,
    rotation="500 MB",
    retention="10 days",
    level=settings.LOG_LEVEL
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🚀 Starting Space Catalog API...")
    logger.info(f"Environment: {settings.ENV}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Initialize services
    await cache_service.initialize()
    
    logger.success("✅ API ready!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down API...")
    await cache_service.clear_expired()


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)


# CORS middleware - allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(stars_router)


@app.get("/")
async def root():
    """Redirect to viewer"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/viewer/index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    cache_stats = await cache_service.stats()
    
    return {
        "status": "healthy",
        "cache": cache_stats,
        "gaia_endpoint": settings.GAIA_TAP_URL
    }


# Backward/compat alias used by some scripts
@app.get("/api/health")
async def health_check_api_alias():
    return await health_check()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


# Mount static files for viewer (must be AFTER all API routes)
# Check multiple possible paths for the viewer directory
viewer_paths = [
    Path(__file__).parent.parent / "viewer",  # Local dev: d:\space\viewer
    Path("/app/viewer"),                        # Docker: /app/viewer
]

for viewer_path in viewer_paths:
    if viewer_path.exists():
        app.mount("/viewer", StaticFiles(directory=str(viewer_path), html=True), name="viewer")
        logger.info(f"📁 Static files mounted from: {viewer_path}")
        break
else:
    logger.warning("⚠️ Viewer directory not found - static files not mounted")

# Mount data directory for constellations.json etc.
data_paths = [
    Path(__file__).parent.parent / "data",  # Local dev: d:\space\data
    Path("/app/data"),                        # Docker: /app/data
]

for data_path in data_paths:
    if data_path.exists():
        app.mount("/data", StaticFiles(directory=str(data_path)), name="data")
        logger.info(f"📁 Data files mounted from: {data_path}")
        break


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
