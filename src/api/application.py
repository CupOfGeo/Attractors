from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from src.api import health, lifespan
from src.api.router import api_router
from src.logging import configure_logging
from src.settings import settings


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="Attractors API",
        version="0.0.1",
        docs_url="/",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
        lifespan=lifespan.lifespan
    )

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # Health endpoint
    app.include_router(router=health.router, prefix="/manage", tags=["manage"])
    # prometheus
    Instrumentator().instrument(app).expose(app, endpoint='/manage/prometheus', tags=["manage"])

    # Adding CORS Middleware to the FastAPI application.
    # This middleware allows cross-origin requests from specified origins.
    # It enables:
    #   - Requests from origins defined in settings.backend_cors_origins.
    #   - Credentials to be included in the requests.
    #   - All HTTP methods and headers in the requests.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.backend_cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
