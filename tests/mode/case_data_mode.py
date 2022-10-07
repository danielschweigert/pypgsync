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
        ]
    },
}
