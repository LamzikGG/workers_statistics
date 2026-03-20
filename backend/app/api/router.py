from fastapi import APIRouter
from app.api.endpoint import upload, statistics, tasks

api_router = APIRouter()

api_router.include_router(upload.router)
api_router.include_router(statistics.router)
api_router.include_router(tasks.router)