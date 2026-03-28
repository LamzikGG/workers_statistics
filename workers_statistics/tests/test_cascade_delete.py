def test_cascade_delete(transaction):
    transaction.execute("""
        INSERT INTO employees (full_name, department, role)
        VALUES ('Иван', 'Sales', 'Manager')
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
        VALUES (%s, %s, 'Переговоры');
    """, (opp_id, emp_id))

    transaction.execute("""
        DELETE FROM opportunities WHERE opportunity_id = %s;
    """, (opp_id,))

    transaction.execute("""
        SELECT * FROM opportunity_history WHERE opportunity_id = %s;
    """, (opp_id,))

    result = transaction.fetchall()
    assert result == []