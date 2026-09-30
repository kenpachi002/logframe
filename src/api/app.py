"""
FastAPI application factory.
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from api.routes import events, integrity, raw, ingest, health
from api.security import limiter, rate_limit_handler, SecurityHeadersAndSizeMiddleware


def create_app() -> FastAPI:
    app = FastAPI(
        title="ULPF — Universal Log Pre-processing Framework",
        description=(
            "Enterprise-grade log ingestion and normalization. Ingest multi-vendor network/security logs, "
            "normalize to OCSF 1.9.0, anchor integrity on a cryptographic hashchain ledger, "
            "and detect tampered events."
        ),
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── Security & Rate Limiting state ────────────────────────────────────────
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

    # CORS — allow all origins for demo (restrict in production)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Security Headers & Request Payload Protection Middleware
    app.add_middleware(SecurityHeadersAndSizeMiddleware)
    app.add_middleware(SlowAPIMiddleware)

    # ── Structured exception handling (OWASP sanitization) ────────────────────
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        import traceback
        print(f"[ULPF ERROR] {request.method} {request.url.path}: {exc}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": "An internal error occurred while processing the request.",
                "status_code": 500,
            },
        )

    # ── API routes ────────────────────────────────────────────────────────────
    app.include_router(health.router,    prefix="/api", tags=["Health"])
    app.include_router(ingest.router,    prefix="/api", tags=["Ingest"])
    app.include_router(events.router,    prefix="/api", tags=["Events"])
    app.include_router(raw.router,       prefix="/api", tags=["Raw Events"])
    app.include_router(integrity.router, prefix="/api", tags=["Integrity & Blockchain"])

    # ── Initialize DB on startup ──────────────────────────────────────────────
    @app.on_event("startup")
    def _startup() -> None:
        from storage.db import init_db
        try:
            init_db()
        except Exception as exc:
            print(f"[ULPF] WARNING: DB init failed: {exc}")

    # ── Serve frontend static files ───────────────────────────────────────────
    frontend_dir = Path(__file__).parent.parent.parent / "frontend"
    if frontend_dir.exists():
        app.mount("/frontend", StaticFiles(directory=str(frontend_dir)), name="frontend")

        @app.get("/", include_in_schema=False)
        def serve_frontend() -> FileResponse:
            return FileResponse(str(frontend_dir / "index.html"))

        @app.get("/examples", include_in_schema=False)
        @app.get("/examples.html", include_in_schema=False)
        def serve_examples() -> FileResponse:
            return FileResponse(str(frontend_dir / "examples.html"))

        @app.get("/roadmap", include_in_schema=False)
        @app.get("/roadmap.html", include_in_schema=False)
        def serve_roadmap() -> FileResponse:
            return FileResponse(str(frontend_dir / "roadmap.html"))
    else:
        @app.get("/", tags=["Health"])
        def health_check() -> dict:
            return {"status": "ok", "service": "ULPF", "version": "0.1.0",
                    "note": "Frontend not found. Place index.html in frontend/"}

    return app
