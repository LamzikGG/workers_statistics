from fastapi import APIRouter, HTTPException, Query
from ...services.llm_service import LLMService_analyze_json
import os
import json

router = APIRouter(prefix = "/analyze_json", tags = ["/analyze"])

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
BASE_DIR = os.path.dirname(BACKEND_DIR)
json_dir = os.path.join(BASE_DIR, "./json_files")

@router.get("/analyze_json")
async def analyze_json(filename: str = Query(...)):
    json_path = os.path.join(json_dir, filename)
    if not os.path.exists(json_path):
              raise HTTPException(status_code=404, detail=f"Файл не найден: {json_path}")
     
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
     
        llm_service = LLMService_analyze_json()
        answer = await llm_service.analyze_json_file(data)
        return {
              "filename": filename,
              "records_count": len(data),
              "llm_response": answer
    }