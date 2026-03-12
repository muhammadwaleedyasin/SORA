from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router

STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-initialize DB and seed on startup (for Vercel / fresh deploys)
    import os

    from app.core.database import engine, async_session
    from app.models.base import Base

    # Import all models so metadata is complete
    import app.models  # noqa: F401

    db_url = os.environ.get("DATABASE_URL", "")
    is_sqlite = "sqlite" in db_url
    db_path = db_url.split("///")[-1] if is_sqlite else ""

    needs_seed = is_sqlite and db_path and not os.path.exists(db_path)

    if needs_seed or os.environ.get("FORCE_SEED") == "1":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        from app.seed.seed_runner import seed_all

        async with async_session() as db:
            await seed_all(db)

    yield


app = FastAPI(
    title="Drone Compliance Platform",
    description="SORA 2.5 calculation engine and Drone Maturity Assessment (DMA) tool",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")
