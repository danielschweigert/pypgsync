"""
Unit test for the query module.
"""
import pytest
from typing import List, Dict, Any, Optional
from pypgsync.util.query import get_primary_keys, get_column_records, get_column_set_diff, \
    get_column_records_for_primary_key_subset, get_table_column_names, get_column_values
from pypgsync.util.create import insert_records
from tests.case_build import create_sql_insert_records_table_a, populate_all_tables
from tests.util.case_data_util import case_data


@pytest.mark.usefixtures("con_source")
def test_get_primary_keys(con_source):

    cur_source = con_source.cursor()
    primary_keys = get_primary_keys(cur=cur_source, table_names=["table_a", "table_b"])
    assert primary_keys == {'table_a': 'id', 'table_b': 'id'}


@pytest.mark.usefixtures("con_source")
def test_get_column_values(con_source):

    table_name = "table_a"
    column_name = "my_int"

    cur_source = con_source.cursor()
    result_1 = get_column_values(cur=cur_source, table_name=table_name, column_name=column_name)
    assert result_1 == []

    records = [{"id": 1, "my_int": 10}, {"id": 2, "my_int": 100}, {"id": 3, "my_int": 1000}]
    insert_records(con=con_source, table_name=table_name, records=records)

    result_2 = get_column_values(cur=cur_source, table_name=table_name, column_name="id")
    assert result_2 == [1, 2, 3]

    result_3 = get_column_values(cur=cur_source, table_name=table_name, column_name="my_int")
    assert result_3 == [10, 100, 1000]


@pytest.mark.usefixtures("con_source")
def test_get_table_column_names(con_source):

    cur_source = con_source.cursor()
    columns = get_table_column_names(cur=cur_source, table_name="table_a")
    assert columns == ["id", "my_varchar", "my_int", "my_float", "my_decimal", "my_date",
                       "my_timestamp"]
    columns = get_table_column_names(cur=cur_source, table_name="table_b")
    assert columns == ["id", "a_id"]


@pytest.mark.usefixtures("con_source")
def test_get_column_records(con_source):

    cur_source = con_source.cursor()
    assert get_column_records(cur=cur_source, table_name="table_a", column_name="id") == []

    insert_sql = create_sql_insert_records_table_a(n=5)
    insert_sql = ''.join(insert_sql)
    cur_source.execute(insert_sql)
    con_source.commit()
    assert get_column_records(cur=cur_source, table_name="table_a", column_name="id") \
           == [1, 2, 3, 4, 5]


@pytest.mark.usefixtures("con_source", "con_destination")
@pytest.mark.parametrize("n_table_b_source, n_table_b_destination", [(15, 10), (0, 0)])
def test_get_column_set_diff(con_source, con_destination, n_table_b_source, n_table_b_destination):

    populate_all_tables(con_source=con_source, con_destination=con_destination,
                        n_table_a_source=20,
                        n_table_a_destination=20,
                        n_table_b_source=n_table_b_source,
                        n_table_b_destination=n_table_b_destination)
    cur_source = con_source.cursor()
    cur_destination = con_destination.cursor()

    diff_1 = get_column_set_diff(cur_db_1=cur_source, cur_db_2=cur_source,
                                 table_name="table_b", column_name="a_id")
    cur_source.execute("SELECT a_id FROM table_b")
    aid_1 = set([row[0] for row in cur_source.fetchall()])
    assert diff_1 == {
        "intersection": aid_1,
        "not_in_db_1": set(),
        "not_in_db_2": set(),
    }

    def detailed_diff_test(cur_1, cur_2):
        diff = get_column_set_diff(cur_db_1=cur_1, cur_db_2=cur_2, table_name="table_b",
                                   column_name="a_id")
        for value in diff["intersection"]:
            for cur in (cur_1, cur_2):
                cur.execute("SELECT COUNT(*) FROM table_b WHERE a_id = %s", (value,))
                assert cur.fetchone()[0] > 0

        for value in diff["not_in_db_1"]:
            cur_1.execute("SELECT COUNT(*) FROM table_b WHERE a_id = %s", (value,))
            assert cur_1.fetchone()[0] == 0
            cur_2.execute("SELECT COUNT(*) FROM table_b WHERE a_id = %s", (value,))
            assert cur_2.fetchone()[0] > 0

        for value in diff["not_in_db_2"]:
            cur_2.execute("SELECT COUNT(*) FROM table_b WHERE a_id = %s", (value,))
            assert cur_2.fetchone()[0] == 0
            cur_1.execute("SELECT COUNT(*) FROM table_b WHERE a_id = %s", (value,))
            assert cur_1.fetchone()[0] > 0

    detailed_diff_test(cur_source, cur_destination)
    detailed_diff_test(cur_destination, cur_source)


@pytest.mark.usefixtures("con_source")
@pytest.mark.parametrize("records, column_names, pk_subset",
                         case_data["query"]["test_get_column_records_for_primary_key_subset"])
def test_get_column_records_for_primary_key_subset(con_source, records, column_names, pk_subset):

    table_name = "table_a"
    primary_key = "id"

    insert_records(con=con_source, table_name=table_name, records=records)

    cur_source = con_source.cursor()
    result = get_column_records_for_primary_key_subset(cur=cur_source, table_name=table_name,
                                                       column_names=column_names,
                                                       primary_key_column=primary_key,
                                                       pk_values=pk_subset)

    def find_record_by_pk(records: List, pv_value: Any) -> Optional[Dict]:
        for record in records:
            if record[primary_key] == pv_value:
                return record
        return None

    if len(pk_subset) == 0 or len(column_names) == 0:
        assert result == []
    else:
        assert len(result) == len(pk_subset)
        for row in result:
            assert len(row) == len(column_names) + 1
            record = find_record_by_pk(records, row[primary_key])
            for column_name in column_names:
                assert row[column_name] == record[column_name]
