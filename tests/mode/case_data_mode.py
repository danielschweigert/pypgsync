"""
Case data for tests in util package
"""
case_data = {
    "primarykey": {
        "test_primary_key_delta": [
                             ([(1, 1), ], [(1, 1), ], {1}, set(), set()),
                             ([(1, 1), (2, 1), (4, 1)], [(1, 1), (3, 1), ], {1}, {3}, {2, 4}),
                             ([(1, 1), (2, 1), (4, 1)], [(1, 2), (3, 2), ], {1}, {3}, {2, 4}),
                             ([], [], set(), set(), set()),
                          ]
    },
}
