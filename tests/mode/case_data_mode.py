"""
Case data for tests in util package
"""
case_data = {
    "primarykey": {
        "test_row_delta_by_primary_key": [
            ([(1, 1), ], [(1, 1), ], {1}, set(), set()),
            ([(1, 1), (2, 1), (4, 1)], [(1, 1), (3, 1), ], {1}, {3}, {2, 4}),
            ([(1, 1), (2, 1), (4, 1)], [(1, 2), (3, 2), ], {1}, {3}, {2, 4}),
            ([], [], set(), set(), set()),
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
                    "insert": set(),
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
                    "insert": set(),
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
                    "insert": set(),
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
                    "insert": set(),
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
                    "insert": set([4, ]),
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
                    "insert": set([4, ]),
                    "update": [{"id": 2, "my_int": 2}, {"id": 3, "my_int": 3}, ]
                }
            )
        ],
    },
}
