"""
Эндпоинт для приёма и проверки файлов
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_processor import FileProcessor
import uuid
import os
from pathlib import Path
import shutil

router = APIRouter(prefix="/upload", tags=["upload"])


data_files = "../data_json"
os.makedirs(data_files, exist_ok=True)

normal_files = {".xlsx", ".xml", ".xls", ".csv"}

@router.post("/upload_file")
async def upload_data(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="нету имени файла")
    
    ext = Path(file.filename).suffix.lower()
    if ext not in normal_files:
        raise HTTPException(status_code=400, detail="расширение не поддерживается")
    
    #Уникальность файла
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(data_files, unique_filename)

    try: 
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        processor = FileProcessor()
        json_path = await processor.convert_to_json(file_path)
        """
        Проверка на ничего в файлах, но у меня linux и нету office 
        if os.path.getsize(file_path) == 0:
            os.remove(file_path)
            raise HTTPException(status_code=400, detail = "в файле ничего нету")
        """
        return {
            "task_id": unique_filename.replace(ext, ""),
            "message": "Файл конвертирован в JSON",
            "json_path": json_path,
            "original_deleted": True
        }
    
    except HTTPException:
        raise
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail = "Ошибка загрузки")