def test_history_insert(transaction):
    transaction.execute("""
        INSERT INTO employees (full_name, department, role)
        VALUES ('Анна', 'Sales', 'Manager')
        RETURNING employee_id;
    """)
    emp_id = transaction.fetchone()[0]

    transaction.execute("""
        INSERT INTO opportunities (employee_id, title, client_name, current_stage)
        VALUES (%s, 'Сделка', 'Клиент', 'Лид')
        RETURNING opportunity_id;
    """, (emp_id,))
    opp_id = transaction.fetchone()[0]

    transaction.execute("""
        INSERT INTO opportunity_history (opportunity_id, employee_id, new_stage)
        VALUES (%s, %s, 'Переговоры')
        RETURNING log_id;
    """, (opp_id, emp_id))

    log_id = transaction.fetchone()[0]
    assert log_id is not None