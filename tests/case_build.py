"""
Functions to help set up the test database scenarios
"""
import random
from typing import List
import psycopg
import pytest
from pytest_postgresql import factories


postgresql_destination_proc = factories.postgresql_proc(port=5433, unixsocketdir='.')
postgresql_destination = factories.postgresql('postgresql_destination_proc')


@pytest.fixture
def con_source(postgresql):
    return create_schema(postgresql)


@pytest.fixture
def con_destination(postgresql_destination):
    return create_schema(postgresql_destination)


@pytest.fixture
def insert_sql():
    insert_sql = """
        INSERT INTO table_a
            (id, my_varchar, my_int, my_float, my_decimal, my_date, my_timestamp)
        VALUES
            (DEFAULT, 'hello', 1, 1.1, 11.1, CURRENT_DATE, NOW());
    """
    return insert_sql


def create_schema(con: psycopg.Connection):
    """Create the schema for the test."""

    create_sql = """
        CREATE TABLE table_a (
            id SERIAL PRIMARY KEY,
            my_varchar VARCHAR(255),
            my_int INT,
            my_float FLOAT,
            my_decimal DECIMAL(10, 2),
            my_date DATE,
            my_timestamp TIMESTAMP
        );
        CREATE TABLE table_b (
            id SERIAL PRIMARY KEY,
            a_id INT REFERENCES table_a(id)
        );
    """

    con.cursor().execute(create_sql)
    con.commit()

    return con


def create_sql_insert_records_table_a(n: int) -> List[str]:
    """
    Create a SQL statement to insert n records into table_a.
    """
    sql_statements = [f"""
            INSERT INTO table_a
                (id, my_varchar, my_int, my_float, my_decimal, my_date, my_timestamp)
            VALUES
                (DEFAULT, 'hello{i}', {i}, {i}.{i}, {i}{i}.{i}{i}, CURRENT_DATE,
                '2022-01-0{0 % 9 + 1} 00:00:00');
            """ for i in range(n)]
    return sql_statements


def create_sql_insert_records_table_b(n: int, foreign_keys: List[int]) -> List[str]:
    """
    Create a SQL statement to insert n records into table_b.
    """
    sql_statements = []
    for i in range(n):
        sql_statements.append(f"""
            INSERT INTO table_b (id, a_id) VALUES (DEFAULT, {random.choice(foreign_keys)});
        """)
    return sql_statements


def create_sql_insert_records(n_table_a_source: int, n_table_a_destination: int,
                              n_table_b_source: int, n_table_b_destination: int) -> str:
    """
    Create a SQL statement to insert specified number of records into table_a and table_b.

    The destination inserts are a subset of the source inserts.
    """
    statements_a_source = create_sql_insert_records_table_a(n_table_a_source)
    statements_a_destination = statements_a_source[:n_table_a_destination]
    if n_table_a_destination > 0:
        statements_b_source = create_sql_insert_records_table_b(
            n_table_b_source, foreign_keys=range(1, n_table_a_destination))
        statements_b_destination = statements_b_source[:n_table_b_destination]
    else:
        statements_b_source = []
        statements_b_destination = []
    sql_source = '\n'.join(statements_a_source + statements_b_source)
    sql_destination = '\n'.join(statements_a_destination + statements_b_destination)
    return sql_source, sql_destination


def populate_all_tables(con_source: psycopg.Connection, con_destination: psycopg.Connection,
                        n_table_a_source: int, n_table_a_destination: int, n_table_b_source: int,
                        n_table_b_destination: int) -> None:
    sql_source, sql_destination = create_sql_insert_records(n_table_a_source, n_table_a_destination,
                                                            n_table_b_source, n_table_b_destination)
    cur_source = con_source.cursor()
    cur_source.execute(sql_source)
    con_source.commit()

    cur_destination = con_destination.cursor()
    cur_destination.execute(sql_destination)
    con_destination.commit()

    cur_source.execute("SELECT COUNT(*) FROM table_a")
    assert cur_source.fetchone()[0] == n_table_a_source
    cur_source.execute("SELECT COUNT(*) FROM table_b")
    assert cur_source.fetchone()[0] == n_table_b_source

    cur_destination.execute("SELECT COUNT(*) FROM table_a")
    assert cur_destination.fetchone()[0] == n_table_a_destination
    cur_destination.execute("SELECT COUNT(*) FROM table_b")
    assert cur_destination.fetchone()[0] == n_table_b_destination
