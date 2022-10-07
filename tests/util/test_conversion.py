"""
Unit tests for conversion module
"""
import decimal
import datetime
from pypgsync.util.conversion import convert_return_value_to_python_type


def test_convert_return_value_to_python_type():

    test_cases = [
        (2.3, 2.3),
        (decimal.Decimal("2.3"), 2.3),
        ("a", "a"),
        (datetime.datetime(2022, 10, 1, 16, 47, 16), "2022-10-01T16:47:16"),
        (datetime.date(2022, 10, 1), "2022-10-01"),
    ]

    for _input, _expected in test_cases:
        assert convert_return_value_to_python_type(_input) == _expected
