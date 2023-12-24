from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

# from src.api.redis import get_redis_pool


@asynccontextmanager
async def lifespan(application: FastAPI):
    application.state.super_secret = "my_secret_key"
    # application.state.redis_pool = get_redis_pool()
    logger.info("Starting Up")
    yield
    # application.state.redis_pool.close()
    logger.info("Shutting Down")
