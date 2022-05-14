"""
Three A's of unit testing:
    Arrange
    Action
    Assert
"""
import _dates

import datetime
import pytest

cases_dates = (
    ("Date: Mon, 11 Sep 2000 02:19:00 -0700 (PDT)", datetime.datetime(2000, 9, 11, 2, 19), 6, 37),
    ("Content-Type: text/plain; charset=us-ascii", None, -1, -1),
    ("Mime-Version: 1.0 Content-Type: text/plain; charset=us-ascii", None, -1, -1),
    (r"\Phillip_Allen_Jan2002_1\Allen,", datetime.datetime(2022, 1, 1), 0, 31),
    ("Jan2002", datetime.datetime(2002, 1, datetime.datetime.now().day), 0, 7),
    ("Jan20021", None, -1, -1),
    ("Jan200201", datetime.datetime(2022, 1, datetime.datetime.now().day, 20, 2, 1), 0, 9),
    ("2002 Jan01", datetime.datetime(2002, datetime.datetime.now().month, datetime.datetime.now().day, 0, 2, 1), 0, 4),
)

cases_clean_dates = (
    ("Date: Mon, 11 Sep 2000 02:19:00 -0700 (PDT)", "Date: [date] (PDT)", []),
    ("Content-Type: text/plain; charset=us-ascii", "Content-Type: text/plain; charset=us-ascii", []),
    ("Mime-Version: 1.0 Content-Type: text/plain; charset=us-ascii", "Mime-Version: 1.0 Content-Type: text/plain; charset=us-ascii", []),
    (r"\Phillip_Allen_Jan2002_1\Allen,", "[date]", []),
)

cases_digits = (
    ('1.0', 2),
    ('100', 3),
    ('abcd', 0),
)

@pytest.mark.parametrize('string, expected_dt, expected_start, expected_end', cases_dates)
def test_parse_dates_sliding(string, expected_dt, expected_start, expected_end):
    dt, index_start, index_end = _dates.parse_dates_sliding(string)
    if dt:
        print(dt)
        assert dt.year == expected_dt.year
        assert dt.month == expected_dt.month
        assert dt.day == expected_dt.day
        assert dt.hour == expected_dt.hour
    else: # could be None, empty
        assert dt is None
        assert dt == expected_dt
    assert index_start == expected_start
    assert index_end == expected_end

@pytest.mark.parametrize('string, expected_string, expected_list', cases_clean_dates)
def test_clean_dates(string, expected_string, expected_list):
    actual_string, actual_list = _dates.clean_dates(string)
    assert actual_string == expected_string

@pytest.mark.parametrize('string, expected', cases_digits)
def test_count_digits(string, expected):
    assert _dates.count_digits(string) == expected