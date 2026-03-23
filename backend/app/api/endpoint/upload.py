from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_processor import FileProcessor
import shutil
from ...services.file_processor import FileProcessor
import os

router = APIRouter(prefix = "/upload", tags = ["upload"])

data_files = "./data_json"
os.mkdir(data_files, exist_ok = True)

@router.post("/uplod_file")
async def upload_data(file: UploadFile = File(...)):
    with open(f"./data_files/{file.filename}", "wb") as f:
        if file.filename in {".xlsx", ".xml", ".xls", ".csv"}:
            return shutil.copyfileobj(file.file, f)
        else:
            raise HTTPException(status_code=400, detail = "Не правильный формат")
