"""
Unit test for the primary key mode module.
"""
import pytest
from pypgsync.mode.primarykey import row_delta_by_primary_key, record_delta_by_primary_key, \
    delta_by_primary_key
from pypgsync.util.create import insert_records
from tests.mode.case_data_mode import case_data


@pytest.mark.usefixtures("con_source", "con_destination")
@pytest.mark.parametrize("records_source, records_destination, expected_result",
                         case_data["primarykey"]["test_row_delta_by_primary_key"])
def test_row_delta_by_primary_key(con_source, con_destination, records_source, records_destination,
                                  expected_result):

    table_name = "table_a"
    primary_key = "id"

    insert_records(con=con_source, table_name=table_name, records=records_source)
    insert_records(con=con_destination, table_name=table_name, records=records_destination)

    cur_source = con_source.cursor()
    cur_destination = con_destination.cursor()

    result = row_delta_by_primary_key(cur_source=cur_source, cur_destination=cur_destination,
                                      table_name=table_name, primary_key=primary_key)

    assert result == expected_result


@pytest.mark.usefixtures("con_source", "con_destination")
@pytest.mark.parametrize(
    "records_source, records_destination, columns, pk_values, expected_updates",
    case_data["primarykey"]["test_record_delta_by_primary_key"])
def test_record_delta_by_primary_key(con_source, con_destination, records_source,
                                     records_destination, columns, pk_values, expected_updates):

    table_name = "table_a"
    primary_key = "id"

    insert_records(con=con_source, table_name=table_name, records=records_source)
    insert_records(con=con_destination, table_name=table_name, records=records_destination)

    cur_source = con_source.cursor()
    cur_destination = con_destination.cursor()
    delta = record_delta_by_primary_key(cur_source, cur_destination, table_name, primary_key,
                                        columns, pk_values)

    assert delta["table_name"] == table_name
    assert delta["primary_key"] == primary_key
    assert delta["update"] == expected_updates


@pytest.mark.usefixtures("con_source", "con_destination")
@pytest.mark.parametrize(
    "records_source, records_destination, columns, pk_values, expected_result",
    case_data["primarykey"]["test_delta_by_primary_key"])
def test_delta_by_primary_key(con_source, con_destination, records_source, records_destination,
                              columns, pk_values, expected_result):

    table_name = "table_a"
    primary_key = "id"

    insert_records(con=con_source, table_name=table_name, records=records_source)
    insert_records(con=con_destination, table_name=table_name, records=records_destination)

    cur_source = con_source.cursor()
    cur_destination = con_destination.cursor()
    result = delta_by_primary_key(cur_source, cur_destination, table_name, primary_key, columns,
                                  pk_values)

    assert result == expected_result
