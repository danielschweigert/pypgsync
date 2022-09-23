import pytest
import psycopg
import random
from typing import List
from pytest_postgresql import factories
from pypgsync.pypgsync import get_n_records_in_table, copy_records, sync_table, sync
from tests.case_data_pypgsync import case_data

postgresql_destination_proc = factories.postgresql_proc(port=5433, unixsocketdir='.')
postgresql_destination = factories.postgresql('postgresql_destination_proc')


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


def test_test_fixtures_are_different_dbs(con_source, con_destination, insert_sql):

    cur_source = con_source.cursor()
    cur_source.execute(insert_sql)
    con_source.commit()

    cur_source.execute("SELECT * FROM table_a")
    content_source = cur_source.fetchall()

    cur_destination = con_destination.cursor()
    cur_destination.execute("SELECT * FROM table_a")
    content_destination = cur_destination.fetchall()

    assert len(content_source) == 1
    assert len(content_destination) == 0


@pytest.mark.parametrize("insert_sql, n_expected", case_data["test_get_n_records_in_table"])
def test_get_n_records_in_table(con_source, insert_sql, n_expected):
    cur_source = con_source.cursor()
    cur_source.execute(insert_sql)
    con_source.commit()
    n_records = get_n_records_in_table(cur_source, "table_a")
    assert n_records == n_expected


@pytest.mark.parametrize("insert_sql, offset, limit, n_expected", case_data["test_copy_records"])
def test_copy_records(con_source, con_destination, insert_sql, offset, limit, n_expected):

    test_table = "table_a"

    # Insert data into source table
    cur_source = con_source.cursor()
    cur_source.execute(insert_sql)
    con_source.commit()
    cur_destination = con_destination.cursor()

    # Copy data from source to destination
    n_records = copy_records(cur_source, con_destination, test_table, offset, limit)

    # Check that the records were copied
    assert n_records == n_expected
    offset_check = get_n_records_in_table(cur_destination, test_table) - n_records
    cur_destination.execute(f"SELECT * FROM {test_table} OFFSET {offset_check}")
    content_destination = cur_destination.fetchall()
    cur_source.execute(f"SELECT * FROM {test_table} OFFSET {offset} LIMIT {limit}")
    content_source = cur_source.fetchall()
    assert content_destination == content_source


@pytest.mark.parametrize("n_table_a_source, n_table_a_destination, n_table_b_source, "
                         "n_table_b_destination, chunk_size", case_data["test_sync"])
def test_sync_table(con_source, con_destination, n_table_a_source, n_table_a_destination,
                    n_table_b_source, n_table_b_destination, chunk_size):
    populate_all_tables(con_source=con_source, con_destination=con_destination,
                        n_table_a_source=n_table_a_source,
                        n_table_a_destination=n_table_a_destination,
                        n_table_b_source=n_table_b_source,
                        n_table_b_destination=n_table_b_destination)

    cur_source = con_source.cursor()
    cur_destination = con_destination.cursor()
    sync_table(cur_source, con_destination, "table_a", chunk_size)

    cur_source.execute("SELECT * FROM table_a")
    content_source = cur_source.fetchall()
    cur_destination.execute("SELECT * FROM table_a")
    content_destination = cur_destination.fetchall()
    assert content_source == content_destination


@pytest.mark.parametrize("n_table_a_source, n_table_a_destination, n_table_b_source, "
                         "n_table_b_destination, chunk_size", case_data["test_sync_table"])
def test_sync_(con_source, con_destination, n_table_a_source, n_table_a_destination,
               n_table_b_source, n_table_b_destination, chunk_size):
    populate_all_tables(con_source=con_source, con_destination=con_destination,
                        n_table_a_source=n_table_a_source,
                        n_table_a_destination=n_table_a_destination,
                        n_table_b_source=n_table_b_source,
                        n_table_b_destination=n_table_b_destination)

    cur_source = con_source.cursor()
    cur_destination = con_destination.cursor()

    sync(cur_source=cur_source, con_destination=con_destination, tables=["table_b", "table_a"],
         chunk_size=chunk_size)

    for table_name in ["table_a", "table_b"]:
        select_sql = f"SELECT * FROM {table_name}"
        cur_destination.execute(select_sql)
        cur_source.execute(select_sql)
        assert cur_destination.fetchall() == cur_source.fetchall()
