"""
Case data for tests in util package
"""
case_data = {
    "primarykey": {
        "test_row_delta_by_primary_key": [
            (
                [{"id": 1, "my_varchar": "a", "my_int": 1, }, ],
                [{"id": 1, "my_varchar": "a", "my_int": 1, }, ],
                {
                    "table_name": "table_a",
                    "primary_key": "id",
                    "intersection": set([1, ]),
                    "delete": set(),
                    "insert": []
                }
            ),
            (
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": "b", "my_int": 2, }],
                [{"id": 1, "my_varchar": "a", "my_int": 1, }, ],
                {
                    "table_name": "table_a",
                    "primary_key": "id",
                    "intersection": set([1, ]),
                    "delete": set(),
                    "insert": [{"id": 2, "my_varchar": "b", "my_int": 2, "my_float": None,
                                "my_decimal": None, "my_date": None, "my_timestamp": None}]
                }
            ),
            (
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": "b", "my_int": 2, },
                 {"id": 3, "my_varchar": "c", "my_int": 3, }],
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": "b", "my_int": 2, },
                 {"id": 4, "my_varchar": "d", "my_int": 5, },
                 {"id": 5, "my_varchar": "e", "my_int": 5, }],
                {
                    "table_name": "table_a",
                    "primary_key": "id",
                    "intersection": set([1, 2, ]),
                    "delete": set([4, 5]),
                    "insert": [{"id": 3, "my_varchar": "c", "my_int": 3, "my_float": None,
                                "my_decimal": None, "my_date": None, "my_timestamp": None}]
                }
            ),
        ],
        "test_record_delta_by_primary_key": [
            (
                [{"id": 1, "my_varchar": "a", "my_int": 1, }, ],
                [{"id": 1, "my_varchar": "a", "my_int": 1, }, ],
                ["my_varchar", "my_int"],
                [1, ],
                []
            ),
            (
                [{"id": 1, "my_varchar": "a", "my_int": 2, }, ],
                [{"id": 1, "my_varchar": "a", "my_int": 1, }, ],
                ["my_varchar", "my_int"],
                [1, ],
                [{"id": 1, "my_int": 2}, ]
            ),
            (
                [{"id": 1, "my_varchar": "a", "my_int": 2, }, ],
                [{"id": 1, "my_varchar": "b", "my_int": 1, }, ],
                ["my_varchar", "my_int"],
                [1, ],
                [{"id": 1, "my_varchar": "a"},
                 {"id": 1, "my_int": 2}, ]
            ),
            (
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": "b", "my_int": 2, },
                 {"id": 3, "my_varchar": "c", "my_int": 3, }, ],
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": None, "my_int": 1, },
                 {"id": 3, "my_varchar": "c", "my_int": 1, }, ],
                ["my_varchar", "my_int"],
                [1, 2, 3],
                [{"id": 2, "my_varchar": "b"},
                 {"id": 2, "my_int": 2},
                 {"id": 3, "my_int": 3},
                 ]
            ),
            (
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": "b", "my_int": 2, },
                 {"id": 3, "my_varchar": "c", "my_int": 3, }, ],
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": None, "my_int": 1, },
                 {"id": 3, "my_varchar": "c", "my_int": 1, }, ],
                ["my_varchar", "my_int"],
                [1, 3],
                [
                 {"id": 3, "my_int": 3},
                ]
            ),
            (
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": "b", "my_int": 2, },
                 {"id": 3, "my_varchar": "c", "my_int": 3, }, ],
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": None, "my_int": 1, },
                 {"id": 3, "my_varchar": "c", "my_int": 1, }, ],
                ["my_int"],
                [2, 3],
                [{"id": 2, "my_int": 2},
                 {"id": 3, "my_int": 3}, ]
            )
        ],
        "test_delta_by_primary_key": [
            (
                [{"id": 1, "my_varchar": "a", "my_int": 1, }, ],
                [{"id": 1, "my_varchar": "a", "my_int": 1, }, ],
                ["my_varchar", "my_int"],
                [1, ],
                {
                    "table_name": "table_a",
                    "primary_key": "id",
                    "intersection": set([1, ]),
                    "delete": set(),
                    "insert": [],
                    "update": []
                }
            ),
            (
                [{"id": 1, "my_varchar": "a", "my_int": 2, }, ],
                [{"id": 1, "my_varchar": "a", "my_int": 1, }, ],
                ["my_varchar", "my_int"],
                [1, ],
                {
                    "table_name": "table_a",
                    "primary_key": "id",
                    "intersection": set([1, ]),
                    "delete": set(),
                    "insert": [],
                    "update": [{"id": 1, "my_int": 2}, ]
                }
            ),
            (
                [{"id": 1, "my_varchar": "a", "my_int": 2, }, ],
                [{"id": 1, "my_varchar": "b", "my_int": 1, }, ],
                ["my_varchar", "my_int"],
                [1, ],
                {
                    "table_name": "table_a",
                    "primary_key": "id",
                    "intersection": set([1, ]),
                    "delete": set(),
                    "insert": [],
                    "update": [{"id": 1, "my_varchar": "a"}, {"id": 1, "my_int": 2}, ]
                }
            ),
            (
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": "b", "my_int": 2, },
                 {"id": 3, "my_varchar": "c", "my_int": 3, }, ],
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": None, "my_int": 1, },
                 {"id": 3, "my_varchar": "c", "my_int": 1, },
                 {"id": 4, "my_varchar": "c", "my_int": 1, }, ],
                ["my_varchar", "my_int"],
                [1, 2, 3],
                {
                    "table_name": "table_a",
                    "primary_key": "id",
                    "intersection": set([1, 2, 3]),
                    "delete": set([4, ]),
                    "insert": [],
                    "update": [{"id": 2, "my_varchar": "b"},
                               {"id": 2, "my_int": 2},
                               {"id": 3, "my_int": 3}, ]
                }
            ),
            (
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": "b", "my_int": 2, },
                 {"id": 3, "my_varchar": "c", "my_int": 3, },
                 {"id": 4, "my_varchar": "d", "my_int": 4, }, ],
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": None, "my_int": 1, },
                 {"id": 3, "my_varchar": "c", "my_int": 1, }, ],
                ["my_varchar", "my_int"],
                [1, 3],
                {
                    "table_name": "table_a",
                    "primary_key": "id",
                    "intersection": set([1, 2, 3]),
                    "delete": set(),
                    "insert": [{"id": 4, "my_varchar": "d", "my_int": 4, "my_float": None,
                                "my_decimal": None, "my_date": None, "my_timestamp": None}, ],
                    "update": [{"id": 3, "my_int": 3}, ]
                }
            ),
            (
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": "b", "my_int": 2, },
                 {"id": 3, "my_varchar": "c", "my_int": 3, },
                 {"id": 4, "my_varchar": "d", "my_int": 4, }, ],
                [{"id": 1, "my_varchar": "z", "my_int": 1, },
                 {"id": 2, "my_varchar": None, "my_int": 1, },
                 {"id": 3, "my_varchar": "c", "my_int": 1, },
                 {"id": 5, "my_varchar": "e", "my_int": 1, }, ],
                ["my_int"],
                [2, 3],
                {
                    "table_name": "table_a",
                    "primary_key": "id",
                    "intersection": set([1, 2, 3]),
                    "delete": set([5, ]),
                    "insert":[{"id": 4, "my_varchar": "d", "my_int": 4, "my_float": None,
                               "my_decimal": None, "my_date": None, "my_timestamp": None}, ],
                    "update": [{"id": 2, "my_int": 2}, {"id": 3, "my_int": 3}, ]
                }
            )
        ],
        "test_apply_delta_by_primary_key": [
            (
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": "b", "my_int": 2, },
                 {"id": 3, "my_varchar": "c", "my_int": 3, }, ],
                {
                    "table_name": "table_a",
                    "primary_key": "id",
                    "intersection": set([1, 2]),
                    "delete": set([3, ]),
                    "insert": [{"id": 5, "my_varchar": "e", "my_int": 5, "my_float": 3.2}],
                    "update": [{"id": 2, "my_int": 20}, ]
                },
                [
                    {"id": 1, "my_varchar": "a", "my_int": 1, "my_float": None, "my_decimal": None,
                     "my_date": None, "my_timestamp": None},
                    {"id": 2, "my_varchar": "b", "my_int": 20, "my_float": None, "my_decimal": None,
                     "my_date": None, "my_timestamp": None},
                    {"id": 5, "my_varchar": "e", "my_int": 5, "my_float": 3.2, "my_decimal": None,
                     "my_date": None, "my_timestamp": None},
                 ]
            ),
            (
                [{"id": 1, "my_varchar": "a", "my_int": 1, },
                 {"id": 2, "my_varchar": "b", "my_int": 2, },
                 {"id": 3, "my_varchar": "c", "my_int": 3, }, ],
                {
                    "table_name": "table_a",
                    "primary_key": "id",
                    "intersection": set([]),
                    "delete": set([1, 2, 3, ]),
                    "insert": [{"id": 5, "my_varchar": "e", "my_int": 5, "my_float": 3.2}],
                    "update": []
                },
                [
                    {"id": 5, "my_varchar": "e", "my_int": 5, "my_float": 3.2, "my_decimal": None,
                     "my_date": None, "my_timestamp": None},
                ]
            ),
        ]
    },
}
