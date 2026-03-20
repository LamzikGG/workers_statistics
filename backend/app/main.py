from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse, FileResponse
import pandas as pd
import os
import shutil
app = FastAPI()


@app.get("/files/{filename}")
async def retrieve_data(filename: str):
    try:
        return FileResponse(filename)
    except Exception as e:
        HTTPException(status_code=404, detail = "Нету файла")

@app.post("/upload_data")
async def uploda_data(file: UploadFile = File(...)):
    file_support = [".xlsx", ".csv", ".xls", ".db"]
    file_ext = os.path.splitext(file.filename)[1]
    file_location = os.path.join("./temp_file")
    if file_ext not in file_support:
        raise HTTPException(status_code=400, detail="Данный формат не поддерживается")
    try:
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file)
        #task = нужно отправить task в RabbitMq для того чтобы было брокер сообщений 
        return JSONResponse(
            status_code=2020,
            content={
                "task_id": id,
                "message": "Файл принят в обработку",
                "status_check_endpoint": f"."#Добавить task_status после 
            }
        )
    except Exception as e:
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=500, detail="Ошибка загрузки")

@app.post("/multiple_files")
async def upload_data(uploaded_files: list[UploadFile]):
    for upload_files in uploaded_files:
        file = upload_files.file
        filename = upload_files.filename
        with open(f'1_{filename}', "wb") as f:
            f.write(file.read())