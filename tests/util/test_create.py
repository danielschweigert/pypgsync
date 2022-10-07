"""
Unit test for create module.
"""
import pytest
from pypgsync.util.create import insert_records
from pypgsync.util.conversion import convert_return_value_to_python_type
from tests.util.case_data_util import case_data


@pytest.mark.usefixtures("con_source")
@pytest.mark.parametrize("table_name, records",
                         case_data["create"]["test_insert_records"])
def test_insert_records(con_source, table_name, records):
    insert_records(con=con_source, table_name=table_name, records=records)

    cur = con_source.cursor()
    cur.execute(f"SELECT * FROM {table_name};")
    result = cur.fetchall()

    assert len(result) == len(records)
    column_names = [desc[0] for desc in cur.description]

    _types = set()
    for i_res in range(len(result)):
        r = result[i_res]
        for i_col in range(len(column_names)):
            value = r[i_col]
            _types.add(type(value))
            value = convert_return_value_to_python_type(value)
            assert value == records[i_res].get(column_names[i_col])
