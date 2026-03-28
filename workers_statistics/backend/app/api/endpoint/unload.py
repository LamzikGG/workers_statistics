"""
Тут будет выдаваться файл, который будет показывать аналитику, которую мы сгенерируем. Пока оставляю его пустым сделаю на 3 этапе
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import pandas as pd
from pathlib import Path
import uuid
import psycopg2
from app.api.database import DB_CONFIG
router = APIRouter(prefix= "/unload", tags = ["unload"])
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
EXPORT_DIR = BASE_DIR / "export"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def remove_temp_file(path: Path):
    if path.exists():
        path.unlink()

@router.get("/")
async def unload_file(background_tasks: BackgroundTasks, format_type: str = "xlsx"):
    if format_type not in ["xlsx", "csv"]:
        raise HTTPException(status_code=400, detail="Поддерживается только xlsx и csv")

    sql_query = """
        SELECT
            e.full_name AS "ФИО Сотрудника",
            e.department AS "Отдел",
            e.role AS "Должность",
            e.plan_monthly_revenue AS "План по выручке (руб)",
            COUNT(DISTINCT o.opportunity_id) AS "Кол-во сделок",
            COALESCE(SUM(o.base_amount + o.addon_amount), 0) AS "Факт выручка (руб)",
            COUNT(DISTINCT f.activity_id) AS "Состоялось встреч"
        FROM employees e 
        LEFT JOIN opportunities o ON e.employee_id = o.employee_id 
        LEFT JOIN field_activities f ON e.employee_id = f.employee_id AND f.status ='Состоялась'
        GROUP BY e.employee_id, e.full_name, e.department, e.role, e.plan_monthly_revenue
        ORDER BY "Факт выручка (руб)"DESC;
    """
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        df = pd.read_sql_query(sql_query,conn)

        if df.empty:
            raise HTTPException(status_code=404, detail="Нет данных для выгрузки")

        filename = f"KPI_Report_{uuid.uuid4().hex[:8]}.{format_type}"
        file_path = EXPORT_DIR / filename

        if format_type == "xlsx":
            df.to_excel(file_path, index=False, engine='openpyxl')
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        else:
            df.to_csv(file_path, index=False,encoding='utf-8-sig')
            media_type = "text/csv"
        background_tasks.add_task(remove_temp_file, file_path)

        return FileResponse(
            path=file_path,
            filename=f"BPM_Analytics_Report.{format_type}",
            media_type=media_type,
        )
    except psycopg2.Error as db_error:
        print(f"Ошибка базы данных: {db_error}")
        raise HTTPException(status_code=500, detail="Ошибка подключения к базе данных")
    except Exception as e:
        print(f"Ошибка выгрузки: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при генерации отчета")
    finally:
        if conn:
            conn.close()
