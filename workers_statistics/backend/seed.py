import psycopg2
from app.api.database import DB_CONFIG

SEED_SQL = """
TRUNCATE TABLE field_activities, opportunity_history, opportunities, employees RESTART IDENTITY CASCADE;

INSERT INTO employees (full_name, department, role, plan_monthly_revenue, plan_monthly_meetings) VALUES
('Иванов Иван', 'Отдел продаж', 'Менеджер', 5000000.00, 15),
('Петров Петр', 'Отдел продаж', 'Старший менеджер', 8000000.00, 20);

INSERT INTO opportunities (employee_id, title, client_name, base_amount, addon_amount, current_stage, is_closed_won) VALUES
(1, 'Внедрение CRM', 'ООО Ромашка', 2000000.00, 50000.00, 'Переговоры', FALSE),
(2, 'Аудит безопасности', 'ИП Смирнов', 3000000.00, 1500000.00, 'Подписание договора', TRUE);

INSERT INTO field_activities (opportunity_id, employee_id, planned_time, actual_end_time, status) VALUES
(1, 1, '2026-03-25 12:00:00', '2026-03-25 14:00:00', 'Состоялась'),
(2, 2, '2026-03-26 12:00:00', '2026-03-26 13:00:00', 'Состоялась');
"""

def seed_db():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        with conn.cursor() as cur:
            print("Заполняем базу тестовыми данными...")
            cur.execute(SEED_SQL)
            print("Данные успешно загружены! База больше не пустая.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    seed_db()