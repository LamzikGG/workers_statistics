def test_insert_employee(transaction):
    transaction.execute("""
        INSERT INTO employees (full_name, department, role)
        VALUES ('Тестовый', 'Sales', 'Manager')
        RETURNING employee_id;
    """)

    emp_id = transaction.fetchone()[0]
    assert emp_id is not None