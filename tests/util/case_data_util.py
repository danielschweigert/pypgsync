"""
Case data for tests in util package
"""
case_data = {
    "query": {
        "test_get_column_records_for_primary_key_subset": []
    },
    "create": {
        "test_insert_records": [
            ("table_a",
             [{"id": 1, "my_varchar": "a", "my_int": 1, "my_float": 1.2, "my_decimal": 10.12,
               "my_date": "2022-10-01", "my_timestamp": "2011-05-16T15:36:38"},
              {"id": 2, "my_varchar": "b", "my_int": 2, "my_float": 2.4, "my_decimal": 20.24,
               "my_date": "2022-10-02", "my_timestamp": "2011-05-17T15:36:38"},
              {"id": 3, "my_varchar": "c", "my_int": 3, "my_float": 3.6, "my_decimal": 30.36,
               "my_date": "2022-10-03", "my_timestamp": "2011-05-18T15:36:38"}, ]),
            ("table_a", [{"id": 1, "my_varchar": "a", "my_int": 1, }, ]),
            ("table_a", [{"id": 1, "my_varchar": "a", "my_int": 1, }, {"id": 2, "my_int": 3, }]),
            ("table_a", []),
            ("table_a", [{"id": 1}, {"id": 2}, {"id": 3}]),
        ]
    }
}
