from contextlib import asynccontextmanager

from aiocache import caches
from fastapi import FastAPI
from loguru import logger


@asynccontextmanager
async def lifespan(application: FastAPI):
    application.state.super_secret = "my_secret_key"
    caches.set_config(
        {
            "default": {
                "cache": "aiocache.SimpleMemoryCache",
                "serializer": {"class": "aiocache.serializers.PickleSerializer"},
            },
            "redis_alt": {
                "cache": "aiocache.RedisCache",
                "endpoint": "my_redis_container",
                "port": 6379,
                "timeout": 1,
                "serializer": {"class": "aiocache.serializers.PickleSerializer"},
                "plugins": [
                    {"class": "aiocache.plugins.HitMissRatioPlugin"},
                    {"class": "aiocache.plugins.TimingPlugin"},
                ],
            },
        }
    )
    logger.info("Starting Up")
    yield
    # application.state.redis_pool.close()
    logger.info("Shutting Down")
