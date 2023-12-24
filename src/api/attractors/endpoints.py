import gzip
import hashlib
import pickle
import time
from io import BytesIO
from typing import List

from aiocache import caches
from fastapi import APIRouter
from fastapi.responses import FileResponse
from loguru import logger

from src.api.attractors.attractor_models import AttractorRequestModel
from src.api.attractors.cliff_attractor import (
    gen_random,
    make_dataframe,
    make_gif,
    make_gif_from_df,
)

router = APIRouter()


@router.get("/inital-conditions")
async def get_inital_conditions() -> List[float]:
    """Return a list of inital conditions."""
    return gen_random()


@router.post("/generate-attractor-gif")
async def random_gif(req: AttractorRequestModel) -> FileResponse:
    """Return an attractor GIF."""
    make_gif(req.initial_conditions, req.color_map)
    return FileResponse("content/flip_gif_temp.gif", media_type="image/gif")


async def compute_result(data: List[float]) -> str:
    """Compute a result."""
    time.sleep(7)
    return str(sum(data))


@router.post("/make-gif-cache")
async def get_my_key(
    data: List[float],
    cmap: str = "fire",
) -> str:
    """Return my key."""

    # Hash the data to use as a cache key
    key = hashlib.md5(str(data).encode()).hexdigest()
    logger.info(f"Data: {data} \n Key: {key}")
    cache = caches.get('default')

    result = await cache.get(key)
    if result is not None:
        # Decompress and de-serialize the DataFrame
        with gzip.GzipFile(fileobj=BytesIO(result)) as f:
            result = pickle.load(f)

    logger.info(f"Result: {result}")
    if result is None:
        # If not in cache, perform the computation
        result = make_dataframe(data)
        # Serialize and compress the DataFrame, and store it in the cache
        with BytesIO() as f:
            with gzip.GzipFile(fileobj=f, mode='w') as gz:
                pickle.dump(result, gz)
            await cache.set(key, f.getvalue())

        logger.info(f"Set cache Key: {key} to Result: {result}")

    make_gif_from_df(result, cmap=cmap)
    return FileResponse("content/flip_gif_temp.gif", media_type="image/gif")
