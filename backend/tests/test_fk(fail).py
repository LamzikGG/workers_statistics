import pytest

def test_opportunity_fk_fail(transaction):
    with pytest.raises(Exception):
        transaction.execute("""
            INSERT INTO opportunities (employee_id, title, client_name, current_stage)
            VALUES (9999, 'Ошибка', 'Нет', 'Лид');
        """)