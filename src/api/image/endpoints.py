from fastapi import APIRouter, UploadFile
from PIL import Image

router = APIRouter()


@router.post("/upload/")
async def upload_image(file: UploadFile):
    # Read the uploaded image using PIL (Python Imaging Library)
    image = Image.open(file.file)

    # Get the size of the image
    width, height = image.size

    # Return the size of the image as a JSON response
    return {"width": width, "height": height}
