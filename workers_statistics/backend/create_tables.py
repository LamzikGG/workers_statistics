import psycopg2
from app.api.database import DB_CONFIG

CREATE_TABLES_SQL = """
DROP TABLE IF EXISTS field_activities, opportunity_history, opportunities, employees CASCADE;

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    department VARCHAR(100) NOT NULL,
    role VARCHAR(100) NOT NULL,
    plan_monthly_revenue DECIMAL(15, 2) DEFAULT 0.00,
    plan_monthly_meetings INT DEFAULT 0
);

CREATE TABLE opportunities (
    opportunity_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    client_name VARCHAR(255) NOT NULL,
    base_amount DECIMAL(15, 2) DEFAULT 0.00,
    addon_amount DECIMAL(15, 2) DEFAULT 0.00,
    current_stage VARCHAR(100) NOT NULL,
    is_closed_won BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

CREATE TABLE opportunity_history (
    log_id SERIAL PRIMARY KEY,
    opportunity_id INT NOT NULL,
    employee_id INT NOT NULL,
    old_stage VARCHAR(100),
    new_stage VARCHAR(100) NOT NULL,
    user_comment TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(opportunity_id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE SET NULL
);

CREATE TABLE field_activities (
    activity_id SERIAL PRIMARY KEY,
    opportunity_id INT NOT NULL,
    employee_id INT NOT NULL,
    planned_time TIMESTAMP NOT NULL,
    actual_end_time TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Запланирована',
    data_entered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    required_fields_filled_percent INT DEFAULT 0,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(opportunity_id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE SET NULL
);

CREATE INDEX idx_opp_employee ON opportunities(employee_id);
CREATE INDEX idx_history_date ON opportunity_history(changed_at);
CREATE INDEX idx_activity_dates ON field_activities(actual_end_time, data_entered_at);
"""

def init_db():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        with conn.cursor() as cur:
            print("Создаем таблицы в базе данных...")
            cur.execute(CREATE_TABLES_SQL)
            print("Схема базы данных успешно создана!")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_db()