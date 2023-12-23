from fastapi.routing import APIRouter

from src.api import image

# Note main '/api' route is set in application along with manage/health and manage/prometheus
api_router = APIRouter()
api_router.include_router(image.router, prefix="/image", tags=["image"])
