"""
Implementation of the primary key mode, which is used to sync the tables by selected primary keys
"""
from typing import List, Dict
import psycopg
from pypgsync.util.query import get_column_set_diff, get_column_records_for_primary_key_subset


def row_delta_by_primary_key(cur_source: psycopg.Cursor, cur_destination: psycopg.Cursor,
                             table_name: str, primary_key: str) -> List[Dict]:
    """
    Get primary key ids which mismatch between the source and destination databases
    """
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


def record_delta_by_primary_key(cur_source: psycopg.Cursor, cur_destination: psycopg.Cursor,
                                table_name: str, primary_key: str, columns: List[str],
                                pk_values: List) -> List[Dict]:
    """
    Get the records that are different between the source and destination databases for the
    given primary keys and columns.
    """

    if primary_key in columns:
        raise ValueError("Primary key cannot be in the list of columns to sync")

    source_records = get_column_records_for_primary_key_subset(cur=cur_source,
                                                               table_name=table_name,
                                                               column_names=columns,
                                                               primary_key_column=primary_key,
                                                               pk_values=pk_values)
    destination_records = get_column_records_for_primary_key_subset(cur=cur_destination,
                                                                    table_name=table_name,
                                                                    column_names=columns,
                                                                    primary_key_column=primary_key,
                                                                    pk_values=pk_values)

    source_records_dict = {record[primary_key]: record for record in source_records}
    destination_records_dict = {record[primary_key]: record for record in destination_records}

    update = []
    for pk_value in pk_values:
        source_record = source_records_dict[pk_value]
        destination_record = destination_records_dict[pk_value]
        for column in columns:
            if source_record[column] != destination_record[column]:
                update.append({primary_key: pk_value, column: source_record[column]})

    result = {
        "table_name": table_name,
        "primary_key": primary_key,
        "update": update,
    }

    return result
