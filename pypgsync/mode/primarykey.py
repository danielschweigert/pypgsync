"""
Implementation of the primary key mode, which is used to sync the tables by selected primary keys
"""
from typing import List, Dict
import psycopg
from pypgsync.util.query import get_column_set_diff


def primary_key_delta(cur_source: psycopg.Cursor, cur_destination: psycopg.Cursor, table_name: str,
                      primary_key: str) -> List[Dict]:
    diff = get_column_set_diff(cur_db_1=cur_source, cur_db_2=cur_destination, table_name=table_name,
                               column_name=primary_key)

    response = {
        "table_name": table_name,
        "primary_key": primary_key,
        "intersection": diff["intersection"],
        "delete": diff["not_in_db_1"],
        "insert": diff["not_in_db_2"],
    }

    return response
