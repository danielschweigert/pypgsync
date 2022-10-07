"""
Unit test for update functions
"""
import pytest

from pypgsync.util.create import insert_records
from pypgsync.util.update import point_update
from tests.util.case_data_util import case_data


@pytest.mark.usefixtures("con_source")
@pytest.mark.parametrize(
    "records, set_column, set_value, where_column, where_value",
    case_data["update"]["test_point_update"])
def test_point_update(con_source, records, set_column, set_value, where_column, where_value):

    def is_correct_update() -> bool:
        sql = f"""SELECT {set_column} FROM {table_name} WHERE {where_column}=%s;"""
        cur.execute(sql, (where_value,))
        result = cur.fetchall()

        check = True and len(result) > 0
        for r in result:
            check = check and r[0] == set_value
            if r[0] != set_value:
                print(r[0], set_value)

        return check

    table_name = "table_a"
    cur = con_source.cursor()
    insert_records(con=con_source, table_name=table_name, records=records)

    assert is_correct_update() is False
    point_update(con=con_source, table_name=table_name, set_column=set_column, set_value=set_value,
                 where_column=where_column, where_value=where_value)
    assert is_correct_update()
