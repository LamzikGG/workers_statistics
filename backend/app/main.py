from fastapi import FastAPI, HTTPException
from app.api.router import api_router

app = FastAPI()

app.include_router(api_router)
