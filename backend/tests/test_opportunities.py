def test_insert_opportunity(transaction):
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
    assert opp_id is not None