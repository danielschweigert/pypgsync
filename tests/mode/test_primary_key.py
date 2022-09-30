"""
Unit test for the primary key mode module.
"""
import pytest
from pypgsync.mode.primarykey import primary_key_delta
from tests.case_build import populate_all_tables
from tests.mode.case_data_mode import case_data


@pytest.mark.usefixtures("con_source", "con_destination")
@pytest.mark.parametrize("b_records_source, b_records_destination, li, delete, insert",
                         case_data["primarykey"]["test_primary_key_delta"])
def test_primary_key_delta(con_source, con_destination, b_records_source, b_records_destination,
                           li, delete, insert):

    populate_all_tables(con_source=con_source, con_destination=con_destination,
                        n_table_a_source=20,
                        n_table_a_destination=20,
                        n_table_b_source=0,
                        n_table_b_destination=0)
    cur_source = con_source.cursor()
    cur_destination = con_destination.cursor()

    for record in b_records_source:
        cur_source.execute("INSERT INTO table_b (id, a_id) VALUES (%s, %s)", record)
        con_source.commit()
    for record in b_records_destination:
        cur_destination.execute("INSERT INTO table_b (id, a_id) VALUES (%s, %s)", record)
        con_destination.commit()

    result = primary_key_delta(cur_source=cur_source, cur_destination=cur_destination,
                               table_name="table_b", primary_key="id")

    assert result["intersection"] == li
    assert result["delete"] == delete
    assert result["insert"] == insert
    assert result["table_name"] == "table_b"
    assert result["primary_key"] == "id"
