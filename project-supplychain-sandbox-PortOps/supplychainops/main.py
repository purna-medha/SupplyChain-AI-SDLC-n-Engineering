"""FastAPI application entry point with CORS for Streamlit."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

import supplychainops.database_models  # noqa: F401
from supplychainops.application_api_routes import router
from supplychainops.database_configuration import get_engine


@asynccontextmanager
async def application_lifespan(_app: FastAPI):
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="SupplyChainOps API",
    version="1.0.0",
    lifespan=application_lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
