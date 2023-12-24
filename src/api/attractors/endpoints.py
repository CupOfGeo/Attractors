import gzip
import hashlib
import pickle
from io import BytesIO
from typing import List

from aiocache import caches
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from loguru import logger

from src.api.attractors.attractor_functions import ATTRACTOR_FUNCTIONS
from src.api.attractors.attractor_models import (
    AttractorRequestModel,
    InitialConditionsRequest,
)
from src.api.attractors.attractor_service import AttractorService

router = APIRouter()
attractor_service = AttractorService()


@router.post("/inital-conditions")
async def make_inital_conditions(request: InitialConditionsRequest) -> List[float]:
    """Return a list of inital conditions."""
    # request.percent_empty # forget for now
    if ATTRACTOR_FUNCTIONS[request.function] is None:
        raise HTTPException(
            status_code=400, detail=f"Invalid function name: {request.function}"
        )
    logger.info(f"request.function: {request.function}")
    return attractor_service.gen_random(ATTRACTOR_FUNCTIONS[request.function])


@router.post("/make-gif")
async def make_gif(request: AttractorRequestModel) -> Response:
    """Make GIF."""
    logger.info(f"request: {request}")
    if ATTRACTOR_FUNCTIONS[request.function] is None:
        raise HTTPException(
            status_code=400, detail=f"Invalid function name: {request.function}"
        )

    # Hash the initial_conditions to use as a cache key
    key = hashlib.md5(
        (str(request.initial_conditions) + request.function).encode()
    ).hexdigest()
    logger.info(f"Key: {key}")
    cache = caches.get("default")

    result = await cache.get(key)
    if result is not None:
        # Decompress and de-serialize the DataFrame
        with gzip.GzipFile(fileobj=BytesIO(result)) as f:
            result = pickle.load(f)

    if result is None:
        # If not in cache, perform the computation
        result = attractor_service.make_dataframe(
            inital_conditions=request.initial_conditions,
            function=ATTRACTOR_FUNCTIONS[request.function],
        )
        # Serialize and compress the DataFrame, and store it in the cache
        with BytesIO() as f:
            with gzip.GzipFile(fileobj=f, mode="w") as gz:
                pickle.dump(result, gz)
            await cache.set(key, f.getvalue())

        logger.info(f"Set cache Key: {key} to Result: {result}")

    gif_bytes = attractor_service.make_gif_from_df(result, request.color_map)
    return Response(content=gif_bytes.getvalue(), media_type="image/gif")
