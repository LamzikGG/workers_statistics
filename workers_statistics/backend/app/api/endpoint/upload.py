from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_processor import FileProcessor
import uuid
import json
from pathlib import Path
import psycopg2
from app.api.database import DB_CONFIG

router = APIRouter(prefix="/upload", tags=["upload"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data_json"
DATA_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".xlsx", ".xml", ".xls", ".csv"}


@router.post("/upload_file")
async def upload_data(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Нет имени файла")

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Формат не поддерживается")

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Файл пуст")

    task_id = str(uuid.uuid4())
    unique_filename = f"{task_id}{file_ext}"
    file_path = DATA_DIR / unique_filename

    try:
        with open(file_path, "wb") as f:
            f.write(contents)

        processor = FileProcessor()
        json_path_str = await processor.convert_to_json(str(file_path))
        json_file_path = Path(json_path_str)

        with open(json_file_path, "r", encoding='utf-8') as f:
            parsed_data = json.load(f)

        if parsed_data:
            print(f"DEBUG: Ключи в JSON: {list(parsed_data[0].keys())}")

        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = False
        try:
            with conn.cursor() as cur:
                for row in parsed_data:
                    full_name = row.get("ФИО Сотрудника") or row.get("ФИО") or "Неизвестно"
                    dept = row.get("Отдел") or "Продажи"
                    role = row.get("Должность") or "Менеджер"
                    plan = row.get("План по выручке (руб)") or 0

                    cur.execute("""
                        INSERT INTO employees (full_name, department, role, plan_monthly_revenue)
                        VALUES (%s, %s, %s, %s)
                        RETURNING employee_id;
                    """, (full_name, dept, role, float(plan)))

                    new_id = cur.fetchone()[0]
                    revenue = row.get("Факт выручка (руб)") or row.get("Сумма") or 0

                    cur.execute("""
                        INSERT INTO opportunities (employee_id, title, client_name, base_amount, current_stage)
                        VALUES (%s, %s, %s, %s, %s);
                    """, (new_id, f"Сделка {full_name}", "Из Excel", float(revenue), "Завершено"))

            conn.commit()
        except Exception as db_err:
            conn.rollback()
            raise db_err
        finally:
            conn.close()

        if file_path.exists(): file_path.unlink()
        if json_file_path.exists(): json_file_path.unlink()

        return {"status": "success", "records_inserted": len(parsed_data)}

    except Exception as e:
        if file_path.exists(): file_path.unlink()
        print(f"Ошибка в upload_data: {e}")
        raise HTTPException(status_code=500, detail=str(e))