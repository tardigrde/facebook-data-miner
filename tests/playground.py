import pytest
from pytest_cases import parametrize, fixture, fixture_ref, lazy_value
# @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
# def test_eval(test_input, expected):
#     assert eval(test_input) == expected

@pytest.fixture
def world_str():
    return 'world'


def whatfun():
    return 'what'


@fixture
@parametrize('who', [fixture_ref(world_str),
                     'you'])
def greetings(who):
    return 'hello ' + who


@parametrize('main_msg', ['nothing',
                          fixture_ref(world_str),
                          lazy_value(whatfun),
                          fixture_ref(greetings)])
@pytest.mark.parametrize('ending', ['?', '!'])
def test_prints(main_msg, ending):
    print(main_msg + ending)
