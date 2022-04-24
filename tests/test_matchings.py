"""
Three A's of unit testing:
    Arrange
    Action
    Assert
"""

import _import
import pytest

@pytest.fixture(scope='module')
def patterns():
    yield _import.read_json_to_dict('patterns.json')

def test_read_json_as_dict(patterns):
    assert isinstance(patterns, list)
    assert isinstance(patterns[0], dict)