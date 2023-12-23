from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger


@asynccontextmanager
async def lifespan(application: FastAPI):
    application.state.super_secret = "my_secret_key"
    logger.info("Starting Up")
    yield
    logger.info("Shutting Down")
