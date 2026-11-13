"""FastAPI application entry point with CORS for Streamlit."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel

import supplychainops.database_models  # noqa: F401
from supplychainops import (
    port_claims_service as claims,
    port_demurrage_service as demurrage,
    port_read_service as reads,
)
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


@app.exception_handler(reads.ContainerContextNotFoundError)
@app.exception_handler(claims.ClaimNotFoundError)
async def not_found_response(_request, error: Exception):
    return JSONResponse(status_code=404, content={"detail": str(error)})


@app.exception_handler(demurrage.GateOutConflictError)
@app.exception_handler(claims.DuplicateClaimError)
async def conflict_response(_request, error: Exception):
    return JSONResponse(status_code=409, content={"detail": str(error)})


@app.exception_handler(claims.ClaimValidationError)
async def invalid_claim_response(_request, error: Exception):
    return JSONResponse(status_code=400, content={"detail": str(error)})
