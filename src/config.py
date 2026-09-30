"""
ULPF Configuration
Reads from environment variables; falls back to safe defaults.
Load a .env file by setting ULPF_ENV_FILE or placing a .env in the project root.

Database priority:
  1. DATABASE_URL env var (full SQLAlchemy URL — Supabase, Railway, etc.)
  2. Individual DB_HOST/DB_PORT/DB_NAME/DB_USER/DB_PASSWORD env vars → Postgres
  3. No vars set → SQLite (ulpf.db in project root)
"""
import os
from pathlib import Path


def _env(key: str, default: str) -> str:
    return os.environ.get(key, default)


def _env_int(key: str, default: int) -> int:
    try:
        return int(os.environ.get(key, str(default)))
    except ValueError:
        return default


# ── Attempt to load .env file ─────────────────────────────────────────────────
try:
    from dotenv import load_dotenv

    _env_file = os.environ.get("ULPF_ENV_FILE", ".env")
    if Path(_env_file).exists():
        load_dotenv(_env_file)
except ImportError:
    pass  # python-dotenv not installed; env vars must be set externally


# ── Config values (module-level constants; import Config from this module) ────

class Config:
    # Database — full URL takes precedence over individual parts
    DATABASE_URL: str = _env("DATABASE_URL", "")
    DB_HOST: str = _env("DB_HOST", "")
    DB_PORT: int = _env_int("DB_PORT", 5432)
    DB_NAME: str = _env("DB_NAME", "ulpf")
    DB_USER: str = _env("DB_USER", "")
    DB_PASSWORD: str = _env("DB_PASSWORD", "")

    @classmethod
    def db_url(cls) -> str:
        """Return the database URL to use.

        Priority:
          1. DATABASE_URL env var (Supabase / Railway full connection string)
          2. Individual DB_* env vars → PostgreSQL
          3. Fallback → SQLite (ulpf.db in project root)
        """
        if cls.DATABASE_URL:
            return cls.DATABASE_URL
        if cls.DB_HOST and cls.DB_USER:
            return (
                f"postgresql+psycopg2://{cls.DB_USER}:{cls.DB_PASSWORD}"
                f"@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
            )
        # Default: SQLite in project root (zero-config for demos)
        return "sqlite:///ulpf.db"

    @classmethod
    def is_sqlite(cls) -> bool:
        """True when using SQLite (affects type mappings and pool config)."""
        return cls.db_url().startswith("sqlite")

    @classmethod
    def db_type_label(cls) -> str:
        url = cls.db_url()
        if url.startswith("sqlite"):
            return "SQLite"
        if "supabase" in url:
            return "Supabase (PostgreSQL)"
        return "PostgreSQL"

    # Blockchain / ledger
    BLOCKCHAIN_LEDGER_PATH: str = _env(
        "BLOCKCHAIN_LEDGER_PATH", "blockchain_ledger/chain.jsonl"
    )

    # Normalizer settings
    LOG_TIMEZONE: str = _env("LOG_TIMEZONE", "Asia/Kolkata")

    # Pipeline batch settings
    BATCH_SIZE: int = _env_int("BATCH_SIZE", 50)

    # Version strings
    ULPF_VERSION: str = _env("ULPF_VERSION", "0.1.0")
    OCSF_VERSION: str = _env("OCSF_VERSION", "1.9.0")

    # API
    API_HOST: str = _env("API_HOST", "0.0.0.0")
    API_PORT: int = _env_int("API_PORT", 8000)

    # Security & Scalability
    RATE_LIMIT_DEFAULT: str = _env("RATE_LIMIT_DEFAULT", "120/minute")
    RATE_LIMIT_INGEST: str = _env("RATE_LIMIT_INGEST", "60/minute")
    MAX_REQUEST_SIZE_BYTES: int = _env_int("MAX_REQUEST_SIZE_BYTES", 2 * 1024 * 1024)  # 2MB
    API_KEY: str = _env("ULPF_API_KEY", "")  # Optional auth key; if empty, endpoints remain open for demo
