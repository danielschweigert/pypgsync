"""
Postgres query functions which are not specific to any pypgsync mode and therefore can potentially
be re-used
"""
from typing import List, Dict
import psycopg


def get_primary_keys(cur: psycopg.Cursor, table_names: List[str]) -> List[str]:
    """
    Get the primary keys for a list of tables
    """
    if table_names is None or len(table_names) == 0:
        return []

    condition_str = ",".join([f"'{table_name}'::regclass" for table_name in table_names])
    sql = f"""
        SELECT
            i.indrelid::regclass AS table_name,
            a.attname
        FROM pg_index i
        JOIN pg_attribute a
            ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
        WHERE TRUE
            AND i.indrelid::regclass IN ({condition_str})
            AND i.indisprimary;"""
    cur.execute(sql)
    primary_keys = {row[0]: row[1] for row in cur.fetchall()}
    return primary_keys


def get_column_records(cur: psycopg.Cursor, table_name: str, column_name: str) -> List[str]:
    """
    Get the records for a single column in a table
    """
    sql = f"SELECT {column_name} FROM {table_name}"
    cur.execute(sql)
    records = [row[0] for row in cur.fetchall()]
    return records


def get_column_set_diff(cur_db_1: psycopg.Cursor, cur_db_2: psycopg.Cursor, table_name: str,
                        column_name: str) -> Dict:
    values_db_1 = get_column_records(cur_db_1, table_name, column_name)
    values_db_2 = get_column_records(cur_db_2, table_name, column_name)

    result = {
        "intersection": set(values_db_1).intersection(set(values_db_2)),
        "not_in_db_1": set(values_db_2).difference(set(values_db_1)),
        "not_in_db_2": set(values_db_1).difference(set(values_db_2)),
    }
    return result
