import pytest
from pypgsync.pypgsync import get_n_records_in_table, copy_records, sync_table, sync
from tests.case_data_pypgsync import case_data
from tests.case_build import populate_all_tables


@pytest.mark.usefixtures("con_source", "con_destination", "insert_sql")
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


@pytest.mark.usefixtures("con_source", "insert_sql")
@pytest.mark.parametrize("insert_sql, n_expected", case_data["test_get_n_records_in_table"])
def test_get_n_records_in_table(con_source, insert_sql, n_expected):
    cur_source = con_source.cursor()
    cur_source.execute(insert_sql)
    con_source.commit()
    n_records = get_n_records_in_table(cur_source, "table_a")
    assert n_records == n_expected


@pytest.mark.usefixtures("con_source", "con_destination", "insert_sql")
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


@pytest.mark.usefixtures("con_source", "con_destination")
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


@pytest.mark.usefixtures("con_source", "con_destination")
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
