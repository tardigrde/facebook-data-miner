import pytest
from MessagingAnalyzer import MessagingAnalyzer
from utils import dt


@pytest.fixture(scope='session')
def analyzer(people):
    return MessagingAnalyzer(people.names, people.individuals)


def test_total_number_of_messages(analyzer):
    assert analyzer.total_number_of_messages() == 14
    assert analyzer.total_number_of_messages(start=dt(year=2014), period='y') == 11
    assert analyzer.total_number_of_messages(start=dt(year=2018), period='y') == 3

    assert analyzer.total_number_of_messages(start=dt(year=2014, month=9), period='m') == 1
    assert analyzer.total_number_of_messages(start=dt(year=2014, month=11), period='m') == 8
    assert analyzer.total_number_of_messages(start=dt(year=2014, month=12), period='m') == 2
    assert analyzer.total_number_of_messages(start=dt(year=2018, month=1), period='m') == 3

    assert analyzer.total_number_of_messages(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_messages(start=dt(year=2011, month=11), period='m') == 0
    assert analyzer.total_number_of_messages(start=dt(year=2018, month=5), period='m') == 0


def test_total_number_of_words(analyzer):
    assert analyzer.total_number_of_words() == 24

    assert analyzer.total_number_of_words(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_words(start=dt(year=2014), period='y') == 20
    assert analyzer.total_number_of_words(start=dt(year=2018), period='y') == 4

    assert analyzer.total_number_of_words(start=dt(year=2014, month=9), period='m') == 6
    assert analyzer.total_number_of_words(start=dt(year=2014, month=11), period='m') == 13
    assert analyzer.total_number_of_words(start=dt(year=2014, month=12), period='m') == 1

    assert analyzer.total_number_of_words(start=dt(year=2018, month=1), period='m') == 4
    assert analyzer.total_number_of_words(start=dt(year=2018, month=2), period='m') == 0


def test_total_number_of_characters(analyzer):
    assert analyzer.total_number_of_characters() == 81

    assert analyzer.total_number_of_characters(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_characters(start=dt(year=2014), period='y') == 69
    assert analyzer.total_number_of_characters(start=dt(year=2018), period='y') == 12

    assert analyzer.total_number_of_characters(start=dt(year=2014, month=9), period='m') == 24
    assert analyzer.total_number_of_characters(start=dt(year=2014, month=11), period='m') == 42
    assert analyzer.total_number_of_characters(start=dt(year=2014, month=12), period='m') == 3

    assert analyzer.total_number_of_characters(start=dt(year=2018, month=1), period='m') == 12
    assert analyzer.total_number_of_characters(start=dt(year=2018, month=2), period='m') == 0


def test_total_number_of_messages_sent(analyzer):
    assert analyzer.total_number_of_messages_sent() == 8
    assert analyzer.total_number_of_messages_sent(start=dt(year=2014), period='y') == 6
    assert analyzer.total_number_of_messages_sent(start=dt(year=2018), period='y') == 2

    assert analyzer.total_number_of_messages_sent(start=dt(year=2014, month=9), period='m') == 1
    assert analyzer.total_number_of_messages_sent(start=dt(year=2014, month=11), period='m') == 4
    assert analyzer.total_number_of_messages_sent(start=dt(year=2014, month=12), period='m') == 1
    assert analyzer.total_number_of_messages_sent(start=dt(year=2018, month=1), period='m') == 2

    assert analyzer.total_number_of_messages_sent(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_messages_sent(start=dt(year=2011, month=11), period='m') == 0
    assert analyzer.total_number_of_messages_sent(start=dt(year=2018, month=5), period='m') == 0


def test_total_number_of_words_sent(analyzer):
    assert analyzer.total_number_of_words_sent() == 19

    assert analyzer.total_number_of_words_sent(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_words_sent(start=dt(year=2014), period='y') == 16
    assert analyzer.total_number_of_words_sent(start=dt(year=2018), period='y') == 3

    assert analyzer.total_number_of_words_sent(start=dt(year=2014, month=9), period='m') == 6
    assert analyzer.total_number_of_words_sent(start=dt(year=2014, month=11), period='m') == 9
    assert analyzer.total_number_of_words_sent(start=dt(year=2014, month=12), period='m') == 1

    assert analyzer.total_number_of_words_sent(start=dt(year=2018, month=1), period='m') == 3
    assert analyzer.total_number_of_words_sent(start=dt(year=2018, month=2), period='m') == 0


def test_total_number_of_characters_sent(analyzer):
    assert analyzer.total_number_of_characters_sent() == 69

    assert analyzer.total_number_of_characters_sent(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_characters_sent(start=dt(year=2014), period='y') == 60
    assert analyzer.total_number_of_characters_sent(start=dt(year=2018), period='y') == 9

    assert analyzer.total_number_of_characters_sent(start=dt(year=2014, month=9), period='m') == 24
    assert analyzer.total_number_of_characters_sent(start=dt(year=2014, month=11), period='m') == 33
    assert analyzer.total_number_of_characters_sent(start=dt(year=2014, month=12), period='m') == 3

    assert analyzer.total_number_of_characters_sent(start=dt(year=2018, month=1), period='m') == 9
    assert analyzer.total_number_of_characters_sent(start=dt(year=2018, month=2), period='m') == 0


def test_total_number_of_messages_received(analyzer):
    assert analyzer.total_number_of_messages_received() == 6
    assert analyzer.total_number_of_messages_received(start=dt(year=2014), period='y') == 5
    assert analyzer.total_number_of_messages_received(start=dt(year=2018), period='y') == 1

    assert analyzer.total_number_of_messages_received(start=dt(year=2014, month=9), period='m') == 0
    assert analyzer.total_number_of_messages_received(start=dt(year=2014, month=11), period='m') == 4
    assert analyzer.total_number_of_messages_received(start=dt(year=2014, month=12), period='m') == 1
    assert analyzer.total_number_of_messages_received(start=dt(year=2018, month=1), period='m') == 1

    assert analyzer.total_number_of_messages_received(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_messages_received(start=dt(year=2011, month=11), period='m') == 0
    assert analyzer.total_number_of_messages_received(start=dt(year=2018, month=5), period='m') == 0


def test_total_number_of_words_received(analyzer):
    assert analyzer.total_number_of_words_received() == 5

    assert analyzer.total_number_of_words_received(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_words_received(start=dt(year=2014), period='y') == 4
    assert analyzer.total_number_of_words_received(start=dt(year=2018), period='y') == 1

    assert analyzer.total_number_of_words_received(start=dt(year=2014, month=9), period='m') == 0
    assert analyzer.total_number_of_words_received(start=dt(year=2014, month=11), period='m') == 4
    assert analyzer.total_number_of_words_received(start=dt(year=2014, month=12), period='m') == 0

    assert analyzer.total_number_of_words_received(start=dt(year=2018, month=1), period='m') == 1
    assert analyzer.total_number_of_words_received(start=dt(year=2018, month=2), period='m') == 0


def test_total_number_of_characters_received(analyzer):
    assert analyzer.total_number_of_characters_received() == 12

    assert analyzer.total_number_of_characters_received(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_characters_received(start=dt(year=2014), period='y') == 9
    assert analyzer.total_number_of_characters_received(start=dt(year=2018), period='y') == 3

    assert analyzer.total_number_of_characters_received(start=dt(year=2014, month=9), period='m') == 0
    assert analyzer.total_number_of_characters_received(start=dt(year=2014, month=11), period='m') == 9
    assert analyzer.total_number_of_characters_received(start=dt(year=2014, month=12), period='m') == 0

    assert analyzer.total_number_of_characters_received(start=dt(year=2018, month=1), period='m') == 3
    assert analyzer.total_number_of_characters_received(start=dt(year=2018, month=2), period='m') == 0
