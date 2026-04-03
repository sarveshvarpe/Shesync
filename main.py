from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.logger import logger
from app.core.exceptions import register_exception_handlers

# API Routers
from app.api.v1 import auth
from app.api.v1 import cycle
from app.api.v1 import cycle_log
from app.api.v1 import chat
from app.api.v1 import health
from app.api.v1 import history
from app.api.v1 import user
from app.api.v1 import report


# =========================
# CREATE FASTAPI APP
# =========================

app = FastAPI(
    title="SheSync API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# =========================
# CORS CONFIG
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://10.65.4.73:5173",  # your laptop network IP
        "http://10.217.21.61:5173",
        "http://10.217.17.212:5173",
        "http://10.217.15.198:5173",
        "http://10.217.15.53:5173",
        "http://10.217.27.175:5173",
        "http://10.217.21.14:5173",
        "http://10.217.29.89:5173"

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# REGISTER ROUTERS
# =========================

app.include_router(auth.router)
app.include_router(cycle.router)
app.include_router(cycle_log.router)
app.include_router(chat.router)
app.include_router(health.router)
# app.include_router(history.router)
app.include_router(user.router)
app.include_router(report.router)


# =========================
# EXCEPTION HANDLERS
# =========================

register_exception_handlers(app)


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health_check():
    return {"status": "healthy"}


logger.info("SheSync API started successfully")