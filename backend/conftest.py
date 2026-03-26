import pytest
import psycopg2

@pytest.fixture(scope="session")
def db_conn():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="mysecretpassword",
        host="localhost",
        port="5432"
    )
    yield conn
    conn.close()


@pytest.fixture(autouse=True)
def transaction(db_conn):
    cursor = db_conn.cursor()
    db_conn.autocommit = False

    yield cursor

    db_conn.rollback()
    cursor.close()
#git
