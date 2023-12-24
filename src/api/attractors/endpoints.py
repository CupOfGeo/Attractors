from typing import List

from fastapi import APIRouter
from fastapi.responses import FileResponse

from src.api.attractors.attractor_models import AttractorRequestModel
from src.api.attractors.cliff_attractor import gen_random, make_gif

router = APIRouter()


# @router.post("/upload")
# async def upload_image(file: UploadFile):
#     # Read the uploaded image using PIL (Python Imaging Library)
#     image = Image.open(file.file)

#     # Get the size of the image
#     width, height = image.size

#     # Return the size of the image as a JSON response
#     return {"width": width, "height": height}

@router.get("/inital-conditions")
async def get_inital_conditions() -> List[float]:
    """Return a list of inital conditions."""
    return gen_random()


@router.post("/generate-attractor-gif")
async def random_gif(req: AttractorRequestModel) -> FileResponse:
    """Return an attractor GIF."""
    make_gif(req.initial_conditions, req.color_map)
    return FileResponse("content/flip_gif_temp.gif", media_type="image/gif")
