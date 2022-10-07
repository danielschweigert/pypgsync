"""
Unit test for the primary key mode module.
"""
import pytest
from pypgsync.mode.primarykey import row_delta_by_primary_key, record_delta_by_primary_key, \
    delta_by_primary_key, apply_delta_by_primary_key
from pypgsync.util.create import insert_records
from pypgsync.util.query import get_column_records_for_primary_key_subset, get_table_column_names, \
    get_column_values
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


@pytest.mark.usefixtures("con_source")
@pytest.mark.parametrize("records, delta, expected_remaining",
                         case_data["primarykey"]["test_apply_delta_by_primary_key"])
def test_apply_delta_by_primary_key(con_source, records, delta, expected_remaining):

    table_name = delta["table_name"]
    primary_key = delta["primary_key"]
    insert_records(con=con_source, table_name=table_name, records=records)

    apply_delta_by_primary_key(con_source, delta)

    cur_source = con_source.cursor()
    column_names = get_table_column_names(cur=cur_source, table_name=table_name)
    pk_values = get_column_values(cur=cur_source, table_name=table_name, column_name=primary_key)
    remaining = get_column_records_for_primary_key_subset(cur=cur_source, table_name=table_name,
                                                          column_names=column_names,
                                                          primary_key_column=primary_key,
                                                          pk_values=pk_values)

    assert remaining == expected_remaining
