import pytest
from ConversationAnalyzer import ConversationAnalyzer
from People import People
from utils import dt

TEST_DATA_PATH = '/home/levente/projects/facebook-data-miner/tests/test_data'


# @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
# def test_eval(test_input, expected):
#     assert eval(test_input) == expected

# get\(\'.*\'\)\.


@pytest.fixture(scope='session')
def person(people):
    def _person(name):
        return people.individuals[name]

    return _person


@pytest.fixture(scope='session')
def analyze(person):
    def _analyze(name):
        individual = person(name)
        return ConversationAnalyzer(name, individual.messages)

    return _analyze


@pytest.fixture(scope='session')
def statistics(person, analyze):
    def _stats(name, **kwargs):
        individual = person(name)
        analyzer = analyze(name)
        if 'subject' in kwargs or 'start' in kwargs or 'end' in kwargs:  # and others
            return analyzer.get_stats(individual.messages, **kwargs)
        else:
            return analyzer.stats

    return _stats


# TODO extend all functions with all the data
def test_stats_toke_hal_all(statistics):
    stats = statistics('Tőke Hal')

    assert stats.msg_count == 5
    assert stats.unique_msg_count == 4
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 6
    assert stats.unique_word_count == 4
    # assert stats.word_frequency == 0
    assert stats.char_count == 17
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_me(statistics):
    stats = statistics('Tőke Hal', subject='me')

    assert stats.msg_count == 3
    assert stats.unique_msg_count == 3
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 4
    assert stats.unique_word_count == 3
    # assert stats.word_frequency == 0
    assert stats.char_count == 12
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_partner(statistics):
    stats = statistics('Tőke Hal', subject='partner')

    assert stats.msg_count == 2
    assert stats.unique_msg_count == 2
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 2
    assert stats.unique_word_count == 2
    # assert stats.word_frequency == 0
    assert stats.char_count == 5
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_all_2014_11(statistics):
    stats = statistics('Tőke Hal', subject='all', start=dt(2014, 11), period='m')

    assert stats.msg_count == 4
    assert stats.unique_msg_count == 3
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    # assert stats.word_frequency == 0
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_partner_2014_11(statistics):
    stats = statistics('Tőke Hal', subject='partner', start=dt(2014, 11), period='m')
    assert stats.char_count == 5
    assert stats.word_count == 2


def test_stats_toke_hal_me_2014_11(statistics):
    stats = statistics('Tőke Hal', subject='me', start=dt(2014, 11), period='m')
    assert stats.unique_word_count == 3


#
def test_stats_toke_hal_all_2014_12(statistics):
    stats = statistics('Tőke Hal', subject='all', start=dt(2014, 12), period='m')
    assert stats.msg_count == 1
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.unique_word_count == 1
    # assert stats.word_frequency == 0
    assert stats.char_count == 3
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_partner_2014_12(statistics):
    stats = statistics('Tőke Hal', subject='partner', start=dt(2014, 12), period='m')
    assert stats.word_count == 0


def test_stats_toke_hal_me_2014_12(statistics):
    stats = statistics('Tőke Hal', subject='me', start=dt(2014, 12), period='m')
    assert stats.unique_msg_count == 1


def test_stats_teflon_musk(statistics):
    stats = statistics('Teflon Musk')
    assert stats.msg_count == 6
    assert stats.unique_msg_count == 2  # TODO this does not count media messages
    # assert stats.most_used_msgs == 0 # TODO should only return the most used or e.g. top10 most used
    # assert stats.msg_frequency == 0
    assert stats.word_count == 14
    assert stats.unique_word_count == 7
    # assert stats.word_frequency == 0
    assert stats.char_count == 52  # 23
    # assert stats.most_used_chars == 0


def test_stats_teflon_musk_me(statistics):
    stats = statistics('Teflon Musk', subject='me')
    assert stats.msg_count == 3
    assert stats.unique_msg_count == 1
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 12
    assert stats.unique_word_count == 6
    # assert stats.word_frequency == 0
    assert stats.char_count == 48
    # assert stats.most_used_chars == 0


def test_stats_teflon_musk_partner(statistics):
    stats = statistics('Teflon Musk', subject='partner')
    assert stats.msg_count == 3
    assert stats.unique_msg_count == 1
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 2
    assert stats.unique_word_count == 1
    # assert stats.word_frequency == 0
    assert stats.char_count == 4
    # assert stats.most_used_chars == 0


def test_stats_teflon_musk_all_2014_9(statistics):
    stats = statistics('Teflon Musk', subject='all', start=dt(2014, 9), period='m')
    assert stats.msg_count == 1
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 6
    # assert stats.word_frequency == 0
    # assert stats.most_used_chars == 0


def test_stats_teflon_musk_me_2014_9(statistics):
    stats = statistics('Teflon Musk', subject='me', start=dt(2014, 9), period='m')
    assert stats.unique_word_count == 6


def test_stats_teflon_musk_partner_2014_9(statistics):
    stats = statistics('Teflon Musk', subject='partner', start=dt(2014, 9), period='m')
    assert stats.unique_msg_count == 0
    assert stats.char_count == 0


def test_stats_teflon_musk_all_2014_11(statistics):
    stats = statistics('Teflon Musk', subject='all', start=dt(2014, 11), period='m')
    assert stats.msg_count == 4
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    # assert stats.word_frequency == 0
    # assert stats.most_used_chars == 0


def test_stats_teflon_musk_me_2014_11(statistics):
    stats = statistics('Teflon Musk', subject='me', start=dt(2014, 11), period='m')
    assert stats.word_count == 6


def test_stats_teflon_musk_partner_2014_11(statistics):
    stats = statistics('Teflon Musk', subject='partner', start=dt(2014, 11), period='m')
    assert stats.unique_msg_count == 1
    assert stats.unique_word_count == 1
    assert stats.char_count == 4


def test_stats_teflon_musk_all_2014_12(statistics):
    stats = statistics('Teflon Musk', subject='all', start=dt(2014, 12), period='m')

    assert stats.msg_count == 1
    assert stats.unique_msg_count == 0
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 0
    assert stats.unique_word_count == 0
    # assert stats.word_frequency == 0
    assert stats.char_count == 0
    # assert stats.most_used_chars == 0


def test_time_series_analysis_for_user(analyze):
    analyzer = analyze('Teflon Musk')
    analyzer.get_time_series_data(subject='all')
    assert 1
