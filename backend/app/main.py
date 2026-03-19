from fastapi import FastAPI, UploadFile, HTTPException, File
import pandas as pd
import os
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/upload_data")
async def uploda_data(file: UploadFile = File(...)):
    try:
        filename = f"file.json"
        filepath = os.path.join("./json_data", filename)
        df = pd.read_excel(file.file)
        json_data = df.to_json(orient='record', force_ascii = True)
        with open(filepath, 'w', encoding = 'utf-8') as f:
            f.write(json_data)
        return JSONResponse(
            content=[filename]
        )
    except Exception as e:
        HTTPException(status_code=500, detail=f"Ошибка работы с файлами{str(e)}")

