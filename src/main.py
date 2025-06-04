from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.api import router
from configs.config import app_settings
from configs.logger import logger
from schemas.service import ServiceInfo


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting Services...")
    yield


@asynccontextmanager
async def test_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting Services for Tests...")
    yield


app = FastAPI(
    title="ROOF Pro Service",
    openapi_url="/api/openapi.json/",
    docs_url="/api/docs/",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api")


@app.get("/", response_model=ServiceInfo)
async def root() -> ServiceInfo:
    return ServiceInfo(
        name_service=app_settings.SERVICE_NAME,
        version=app_settings.SERVICE_VERSION,
    )


origins = [
    "http://localhost:8001",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "https://roof-pro.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

if __name__ == "__main__":
    if app_settings.ENVIRONMENT == "local":
        uvicorn.run(
            "main:app",
            host="0.0.0.0",  # noqa: S104
            port=app_settings.SERVICE_PORT,
            reload=True,
            forwarded_allow_ips="*",
        )
    else:
        uvicorn.run(
            app,
            host="0.0.0.0",  # noqa: S104
            port=app_settings.SERVICE_PORT,
            forwarded_allow_ips="*",
        )
