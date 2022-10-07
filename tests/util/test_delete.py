"""
Unit test for delete functions
"""
import pytest
from pypgsync.util.query import get_column_values
from pypgsync.util.create import insert_records
from pypgsync.util.delete import delete_record_by_primary_key_value


@pytest.mark.usefixtures("con_source")
def test_delete_record_by_primary_key_value(con_source):

    table_name = "table_a"
    primary_key = "id"

    cur_source = con_source.cursor()
    remaining_pks = get_column_values(cur=cur_source, table_name=table_name,
                                      column_name=primary_key)
    assert remaining_pks == []

    records = [
        {"id": 1, "my_varchar": "a", "my_int": 10},
        {"id": 2, "my_varchar": "b", "my_int": 11},
        {"id": 3, "my_varchar": "c", "my_int": 12},
        {"id": 4, "my_varchar": "d", "my_int": 13},
        {"id": 5, "my_varchar": "e", "my_int": 14},
    ]
    insert_records(con=con_source, table_name=table_name, records=records)
    remaining_pks = get_column_values(cur=cur_source, table_name=table_name,
                                      column_name=primary_key)
    assert remaining_pks == [1, 2, 3, 4, 5]

    delete_record_by_primary_key_value(con=con_source, table_name=table_name,
                                       primary_key=primary_key, primary_key_value=3)
    remaining_pks = get_column_values(cur=cur_source, table_name=table_name,
                                      column_name=primary_key)
    assert remaining_pks == [1, 2, 4, 5]

    delete_record_by_primary_key_value(con=con_source, table_name=table_name,
                                       primary_key=primary_key, primary_key_value=3)
    remaining_pks = get_column_values(cur=cur_source, table_name=table_name,
                                      column_name=primary_key)
    assert remaining_pks == [1, 2, 4, 5]

    delete_record_by_primary_key_value(con=con_source, table_name=table_name,
                                       primary_key=primary_key, primary_key_value=4)
    remaining_pks = get_column_values(cur=cur_source, table_name=table_name,
                                      column_name=primary_key)
    assert remaining_pks == [1, 2, 5]
