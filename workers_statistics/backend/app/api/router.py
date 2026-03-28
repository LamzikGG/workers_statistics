from fastapi import APIRouter
from app.api.endpoint import upload, unload

api_router = APIRouter()

api_router.include_router(upload.router)
api_router.include_router(unload.router)