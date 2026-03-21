from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_processor import FileProcessor

router = APIRouter(prefix = "/upload", tags = ["upload"])

@router.post("/data")
async def upload_data(file: UploadFile = File(...)):
    processor = FileProcessor()
    task_id = await processor.process_upload(file)
    return{
        "task_id": task_id,
        "message": "файл принят",
        "status_check": f'task/{task_id}'
    }