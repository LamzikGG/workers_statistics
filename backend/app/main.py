from fastapi import FastAPI, HTTPException
from app.api.router import api_router

app = FastAPI()

app.include_router(api_router)

@app.get("/status")
async def status_check():
    try:
        return {"status": "работает"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="не работает")