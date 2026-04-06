from fastapi import APIRouter, HTTPException, Query
from ...services.llm_service import LLMService_analyze_json
from ...services.file_processor import FileProcessor
from pydantic import BaseModel
from typing import Optional
import os
import json
router = APIRouter(prefix = "/analyze_json", tags = ["/analyze"])

@router.get("/analyze_json")
async def analyze_json(json_path: str = Query(...)):

    if not os.path.exists(json_path):
        raise HTTPException(status_code = 404, details = "suck")
    processor = FileProcessor()
    with open("json_path", "r", encoding="utf-8") as f:
        data = json.load(f)

    llm_service = LLMService_analyze_json()
    answer = await llm_service.analyze_json_file(data)
    return {
        "json_path": json_path, 
        "records_count": len(data),
        "llm_respones": answer
    }