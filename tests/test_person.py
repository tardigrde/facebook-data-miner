import pytest
from miner.person import Person


def test_add_two_person():
    one = Person("Test Test", compact_name="testtest")
    two = Person("Test Test", friend=True)
    onetwo = one + two

    assert onetwo.name == "Test Test"
    assert onetwo.friend == True
    assert onetwo.compact_name == "testtest"


def testadd_two_person_with_different_name():
    one = Person("Test Test", compact_name="testtest")
    two = Person("This gets ignored", friend=True)
    with pytest.raises(ValueError):
        onetwo = one + two
