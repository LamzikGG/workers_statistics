def test_update_stage(transaction):
    transaction.execute("""
        INSERT INTO employees (full_name, department, role)
        VALUES ('Петр', 'Sales', 'Manager')
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
        UPDATE opportunities
        SET current_stage = 'Закрыто'
        WHERE opportunity_id = %s;
    """, (opp_id,))

    transaction.execute("""
        SELECT current_stage FROM opportunities WHERE opportunity_id = %s;
    """, (opp_id,))

    stage = transaction.fetchone()[0]
    assert stage == 'Закрыто'