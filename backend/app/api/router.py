from fastapi import APIRouter
from app.api.endpoint import upload, unload, analyze_json_file

api_router = APIRouter()

api_router.include_router(upload.router)
api_router.include_router(unload.router)
api_router.include_router(analyze_json_file.router)