from kvmdash.contrib import kvmdash_client
import pytest

pytestmark = [pytest.mark.client]

def test_foo():
    foo = 1
    assert foo == "not implemented yet"
