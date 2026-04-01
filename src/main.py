from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import auth, portfolios, advisory, calculator
from src.config.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Finance Advisory AI",
    description="AI-powered financial advisory system providing portfolio analysis, "
    "risk assessment, and personalized financial guidance.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(portfolios.router, prefix="/api/v1")
app.include_router(advisory.router, prefix="/api/v1")
app.include_router(calculator.router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}
