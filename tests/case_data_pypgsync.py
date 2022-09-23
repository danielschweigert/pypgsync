"""
Test case data for pypgsync
"""
insert_a_0 = """SELECT 1;"""
insert_a_1 = """
    INSERT INTO table_a
        (id, my_varchar, my_int, my_float, my_decimal, my_date, my_timestamp)
    VALUES (DEFAULT, 'hello', 1, 1.1, 11.1, CURRENT_DATE, NOW());"""
insert_a_2 = """
    INSERT INTO table_a
        (id, my_varchar, my_int, my_float, my_decimal, my_date, my_timestamp)
    VALUES (DEFAULT, 'hello2', 2, 2.2, 22.2, CURRENT_DATE, NOW());"""
insert_a_3 = """
    INSERT INTO table_a
        (id, my_varchar, my_int, my_float, my_decimal, my_date, my_timestamp)
    VALUES (DEFAULT, 'hello3', 3, 3.3, 33.3, CURRENT_DATE, NOW());"""
insert_a_12 = insert_a_1 + insert_a_2
insert_a_123 = insert_a_12 + insert_a_3


case_data = {
    "test_get_n_records_in_table": [
        (insert_a_1, 1),
        (insert_a_0, 0),
        (insert_a_12, 2),
    ],
    "test_copy_records": [
        (insert_a_0, 0, 0, 0),
        (insert_a_0, 0, 10, 0),
        (insert_a_0, 10, 11, 0),
        (insert_a_1, 0, 1, 1),
        (insert_a_1, 0, 0, 0),
        (insert_a_1, 10, 11, 0),
        (insert_a_1, 0, 5, 1),
        (insert_a_12, 0, 2, 2),
        (insert_a_12, 0, 1, 1),
        (insert_a_123, 0, 3, 3),
        (insert_a_123, 2, 3, 1),
        (insert_a_123, 3, 3, 0),
        (insert_a_123, 1, 1, 1),
        (insert_a_123, 1, 10, 2),
    ],
    "test_sync_table": [
        (10, 10, 0, 0, 1),
        (10, 5, 0, 0, 1),
        (10, 0, 0, 0, 1),
        (10, 0, 0, 0, 100),
        (100, 0, 0, 0, 1),
        (10, 2, 0, 0, 5),
    ],
    "test_sync": [
        (10, 10, 10, 10, 1),
        (10, 5, 5, 2, 1),
        (10, 0, 0, 0, 1),
        (10, 2, 8, 7, 100),
        (100, 10, 50, 10, 1),
        (10, 2, 10, 10, 5),
    ]
}
