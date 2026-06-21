from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import get_settings
from src.middleware.tenant import TenantMiddleware
from src.auth.router import router as auth_router
from src.ingestion.upload_controller import router as upload_router
from src.ai_core.router import router as analysis_router
from src.collaboration.router import router as collab_router
from src.estimation.router import router as estimation_router
from src.estimation.export_controller import router as export_router
from src.integration.router import router as integration_router
from src.storage.storage_service import ensure_bucket_exists

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_bucket_exists()
    yield


app = FastAPI(
    title="AI ReqInsight & Estimator",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url=None,
)

app.add_middleware(TenantMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(analysis_router)
app.include_router(collab_router)
app.include_router(estimation_router)
app.include_router(export_router)
app.include_router(integration_router)


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
