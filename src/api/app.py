"""
FastAPI application factory.
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from api.routes import events, integrity, raw, ingest, health


def create_app() -> FastAPI:
    app = FastAPI(
        title="ULPF — Universal Log Pre-processing Framework",
        description=(
            "SIH Project: Ingest heterogeneous network/security logs, "
            "normalize to OCSF 1.9.0, anchor integrity on a hashchain ledger, "
            "and detect tampered events."
        ),
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS — allow all origins for demo (restrict in production)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
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
    else:
        @app.get("/", tags=["Health"])
        def health_check() -> dict:
            return {"status": "ok", "service": "ULPF", "version": "0.1.0",
                    "note": "Frontend not found. Place index.html in frontend/"}

    return app
