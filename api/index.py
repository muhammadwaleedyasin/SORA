"""Vercel serverless entry point."""

import os

# Force SQLite to /tmp on Vercel (writable ephemeral storage)
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:////tmp/drone_compliance.db")
os.environ.setdefault("DEBUG", "false")

from app.main import app  # noqa: E402, F401
