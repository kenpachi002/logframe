"""
Security and scalability middleware and dependencies for ULPF.

Features:
  - Rate limiting via slowapi
  - Request payload size protection (prevents memory exhaustion / DoS)
  - Security response headers (OWASP best practices)
  - Optional API Key authentication (via X-API-Key header or query param)
"""
from __future__ import annotations

from typing import Callable
from fastapi import HTTPException, Request, Response, Security
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader, APIKeyQuery
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware

from config import Config

# ── Rate Limiter ─────────────────────────────────────────────────────────────
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[Config.RATE_LIMIT_DEFAULT],
)


def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Standardized 429 response when rate limit is exceeded."""
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too Many Requests",
            "detail": f"Rate limit exceeded: {exc.detail}",
            "status_code": 429,
        },
        headers={"Retry-After": "60"},
    )


# ── Optional API Key Authentication ──────────────────────────────────────────
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)


async def require_api_key(
    header_key: str | None = Security(api_key_header),
    query_key: str | None = Security(api_key_query),
) -> str | None:
    """
    Validates API key if ULPF_API_KEY is configured in Config.
    If no ULPF_API_KEY is configured, requests are allowed (demo zero-config).
    """
    expected = Config.API_KEY.strip()
    if not expected:
        return None  # Auth disabled / open demo mode

    provided = (header_key or query_key or "").strip()
    if not provided or provided != expected:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key. Provide 'X-API-Key' header or '?api_key=' parameter.",
        )
    return provided


# ── Security Headers & Request Size Middleware ──────────────────────────────
class SecurityHeadersAndSizeMiddleware(BaseHTTPMiddleware):
    """
    1. Enforces maximum request payload size to prevent DoS attacks.
    2. Injects standard OWASP security headers into all responses.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Check Content-Length for large payloads before processing
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                length_int = int(content_length)
                if length_int > Config.MAX_REQUEST_SIZE_BYTES:
                    max_mb = Config.MAX_REQUEST_SIZE_BYTES / (1024 * 1024)
                    return JSONResponse(
                        status_code=413,
                        content={
                            "error": "Payload Too Large",
                            "detail": f"Request body exceeds maximum allowed size of {max_mb:.1f} MB.",
                            "status_code": 413,
                        },
                        headers={"Connection": "close"},
                    )
            except ValueError:
                pass

        response = await call_next(request)

        # OWASP Recommended Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response
