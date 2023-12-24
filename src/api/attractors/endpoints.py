import gzip
import hashlib
import pickle
from io import BytesIO
from typing import List

from aiocache import caches
from fastapi import APIRouter
from fastapi.responses import Response
from loguru import logger

from src.api.attractors.attractor_models import AttractorRequestModel
from src.api.attractors.AttractorService import AttractorService
from src.api.attractors.cliff_attractor import make_dataframe, make_gif_from_df

router = APIRouter()


@router.get("/inital-conditions")
async def get_inital_conditions() -> List[float]:
    """Return a list of inital conditions."""
    return AttractorService().gen_random()


@router.post("/make-gif")
async def make_gif(request: AttractorRequestModel) -> Response:
    """Make GIF."""

    # Hash the initial_conditions to use as a cache key
    key = hashlib.md5(str(request.initial_conditions).encode()).hexdigest()
    logger.info(f"Data: {request.initial_conditions} \n Key: {key}")
    cache = caches.get("default")

    result = await cache.get(key)
    if result is not None:
        # Decompress and de-serialize the DataFrame
        with gzip.GzipFile(fileobj=BytesIO(result)) as f:
            result = pickle.load(f)

    logger.info(f"Result: {result}")
    if result is None:
        # If not in cache, perform the computation
        result = make_dataframe(request.initial_conditions)
        # Serialize and compress the DataFrame, and store it in the cache
        with BytesIO() as f:
            with gzip.GzipFile(fileobj=f, mode="w") as gz:
                pickle.dump(result, gz)
            await cache.set(key, f.getvalue())

        logger.info(f"Set cache Key: {key} to Result: {result}")

    gif_bytes = make_gif_from_df(result, cmap=request.color_map)
    return Response(content=gif_bytes.getvalue(), media_type="image/gif")
