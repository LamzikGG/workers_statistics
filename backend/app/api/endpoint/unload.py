"""
Тут будет выдаваться файл, который будет показывать аналитику, которую мы сгенерируем. Пока оставляю его пустым сделаю на 3 этапе
"""

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(prefix= "/unload", tags = ["unload"])

@router.get("/")
async def unload_file(file):
    return