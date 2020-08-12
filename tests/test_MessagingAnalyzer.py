import pytest
from miner.MessagingAnalyzer import MessagingAnalyzer
from miner.utils import dt

@pytest.fixture(scope='session')
def analyzer(get_people):
    people = get_people()
    return MessagingAnalyzer(people)


def test_total_number_of_messages(analyzer):
    assert analyzer.total_number_of_messages() == 29

    assert analyzer.total_number_of_messages(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_messages(start=dt(year=2014), period='y') == 11
    assert analyzer.total_number_of_messages(start=dt(year=2018), period='y') == 3
    assert analyzer.total_number_of_messages(start=dt(year=2020), period='y') == 15

    assert analyzer.total_number_of_messages(start=dt(year=2011, month=11), period='m') == 0
    assert analyzer.total_number_of_messages(start=dt(year=2014, month=9), period='m') == 1
    assert analyzer.total_number_of_messages(start=dt(year=2014, month=11), period='m') == 8
    assert analyzer.total_number_of_messages(start=dt(year=2014, month=12), period='m') == 2

    assert analyzer.total_number_of_messages(start=dt(year=2018, month=1), period='m') == 3
    assert analyzer.total_number_of_messages(start=dt(year=2018, month=5), period='m') == 0

    assert analyzer.total_number_of_messages(start=dt(year=2020, month=2), period='m') == 10
    assert analyzer.total_number_of_messages(start=dt(year=2020, month=3), period='m') == 1  # jpg
    assert analyzer.total_number_of_messages(start=dt(year=2020, month=4), period='m') == 2
    assert analyzer.total_number_of_messages(start=dt(year=2020, month=5), period='m') == 1
    assert analyzer.total_number_of_messages(start=dt(year=2020, month=6), period='m') == 0
    assert analyzer.total_number_of_messages(start=dt(year=2020, month=8), period='m') == 1

    assert analyzer.total_number_of_messages(start=dt(year=2020, month=2, day=13), period='d') == 2
    assert analyzer.total_number_of_messages(start=dt(year=2020, month=2, day=13, hour=6), period='h') == 2

    assert analyzer.total_number_of_messages(start=dt(year=2020, month=2, day=13, hour=6), period='d') == 4


def test_total_number_of_words(analyzer):
    assert analyzer.total_number_of_words() == 86

    assert analyzer.total_number_of_words(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_words(start=dt(year=2014), period='y') == 20
    assert analyzer.total_number_of_words(start=dt(year=2018), period='y') == 32
    assert analyzer.total_number_of_words(start=dt(year=2020), period='y') == 34

    assert analyzer.total_number_of_words(start=dt(year=2014, month=9), period='m') == 6
    assert analyzer.total_number_of_words(start=dt(year=2014, month=11), period='m') == 13
    assert analyzer.total_number_of_words(start=dt(year=2014, month=12), period='m') == 1

    assert analyzer.total_number_of_words(start=dt(year=2018, month=1), period='m') == 32
    assert analyzer.total_number_of_words(start=dt(year=2018, month=2), period='m') == 0

    assert analyzer.total_number_of_words(start=dt(year=2020, month=2), period='m') == 27
    assert analyzer.total_number_of_words(start=dt(year=2020, month=3), period='m') == 0
    assert analyzer.total_number_of_words(start=dt(year=2020, month=4), period='m') == 4
    assert analyzer.total_number_of_words(start=dt(year=2020, month=5), period='m') == 1
    assert analyzer.total_number_of_words(start=dt(year=2020, month=6), period='m') == 0
    assert analyzer.total_number_of_words(start=dt(year=2020, month=8), period='m') == 2

    assert analyzer.total_number_of_words(start=dt(year=2020, month=2, day=13), period='d') == 14
    assert analyzer.total_number_of_words(start=dt(year=2020, month=2, day=13, hour=5), period='d') == 14


def test_total_number_of_characters(analyzer):
    assert analyzer.total_number_of_characters() == 379

    assert analyzer.total_number_of_characters(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_characters(start=dt(year=2014), period='y') == 69
    assert analyzer.total_number_of_characters(start=dt(year=2018), period='y') == 170
    assert analyzer.total_number_of_characters(start=dt(year=2020), period='y') == 140

    assert analyzer.total_number_of_characters(start=dt(year=2014, month=9), period='m') == 24
    assert analyzer.total_number_of_characters(start=dt(year=2014, month=11), period='m') == 42
    assert analyzer.total_number_of_characters(start=dt(year=2014, month=12), period='m') == 3

    assert analyzer.total_number_of_characters(start=dt(year=2018, month=1), period='m') == 170
    assert analyzer.total_number_of_characters(start=dt(year=2018, month=2), period='m') == 0

    assert analyzer.total_number_of_characters(start=dt(year=2020, month=2), period='m') == 114
    assert analyzer.total_number_of_characters(start=dt(year=2020, month=3), period='m') == 0
    assert analyzer.total_number_of_characters(start=dt(year=2020, month=4), period='m') == 17
    assert analyzer.total_number_of_characters(start=dt(year=2020, month=5), period='m') == 4
    assert analyzer.total_number_of_characters(start=dt(year=2020, month=6), period='m') == 0
    assert analyzer.total_number_of_characters(start=dt(year=2020, month=8), period='m') == 5


def test_total_number_of_messages_sent(analyzer):
    assert analyzer.total_number_of_messages_sent() == 17
    assert analyzer.total_number_of_messages_sent(start=dt(year=2014), period='y') == 6
    assert analyzer.total_number_of_messages_sent(start=dt(year=2018), period='y') == 2
    assert analyzer.total_number_of_messages_sent(start=dt(year=2020), period='y') == 9

    assert analyzer.total_number_of_messages_sent(start=dt(year=2014, month=9), period='m') == 1
    assert analyzer.total_number_of_messages_sent(start=dt(year=2014, month=11), period='m') == 4
    assert analyzer.total_number_of_messages_sent(start=dt(year=2014, month=12), period='m') == 1
    assert analyzer.total_number_of_messages_sent(start=dt(year=2018, month=1), period='m') == 2

    assert analyzer.total_number_of_messages_sent(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_messages_sent(start=dt(year=2011, month=11), period='m') == 0
    assert analyzer.total_number_of_messages_sent(start=dt(year=2018, month=5), period='m') == 0

    assert analyzer.total_number_of_messages_sent(start=dt(year=2020, month=2), period='m') == 6
    assert analyzer.total_number_of_messages_sent(start=dt(year=2020, month=3), period='m') == 0
    assert analyzer.total_number_of_messages_sent(start=dt(year=2020, month=4), period='m') == 2
    assert analyzer.total_number_of_messages_sent(start=dt(year=2020, month=5), period='m') == 0
    assert analyzer.total_number_of_messages_sent(start=dt(year=2020, month=6), period='m') == 0
    assert analyzer.total_number_of_messages_sent(start=dt(year=2020, month=8), period='m') == 1

    assert analyzer.total_number_of_messages_sent(start=dt(year=2020, month=2, day=13), period='d') == 1
    assert analyzer.total_number_of_messages_sent(start=dt(year=2020, month=2, day=13, hour=6), period='h') == 1
    assert analyzer.total_number_of_messages_sent(start=dt(year=2020, month=2, day=13, hour=18), period='h') == 0


def test_total_number_of_words_sent(analyzer):
    assert analyzer.total_number_of_words_sent() == 69

    assert analyzer.total_number_of_words_sent(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_words_sent(start=dt(year=2014), period='y') == 16
    assert analyzer.total_number_of_words_sent(start=dt(year=2018), period='y') == 31
    assert analyzer.total_number_of_words_sent(start=dt(year=2020), period='y') == 22

    assert analyzer.total_number_of_words_sent(start=dt(year=2014, month=9), period='m') == 6
    assert analyzer.total_number_of_words_sent(start=dt(year=2014, month=11), period='m') == 9
    assert analyzer.total_number_of_words_sent(start=dt(year=2014, month=12), period='m') == 1

    assert analyzer.total_number_of_words_sent(start=dt(year=2018, month=1), period='m') == 31
    assert analyzer.total_number_of_words_sent(start=dt(year=2018, month=2), period='m') == 0

    assert analyzer.total_number_of_words_sent(start=dt(year=2020, month=2), period='m') == 16
    assert analyzer.total_number_of_words_sent(start=dt(year=2020, month=3), period='m') == 0
    assert analyzer.total_number_of_words_sent(start=dt(year=2020, month=4), period='m') == 4
    assert analyzer.total_number_of_words_sent(start=dt(year=2020, month=5), period='m') == 0
    assert analyzer.total_number_of_words_sent(start=dt(year=2020, month=6), period='m') == 0
    assert analyzer.total_number_of_words_sent(start=dt(year=2020, month=8), period='m') == 2

    assert analyzer.total_number_of_words_sent(start=dt(year=2020, month=2, day=13), period='d') == 5
    assert analyzer.total_number_of_words_sent(start=dt(year=2020, month=2, day=13, hour=6), period='h') == 5
    assert analyzer.total_number_of_words_sent(start=dt(year=2020, month=2, day=13, hour=7), period='h') == 0


def test_total_number_of_characters_sent(analyzer):
    assert analyzer.total_number_of_characters_sent() == 311

    assert analyzer.total_number_of_characters_sent(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_characters_sent(start=dt(year=2014), period='y') == 60
    assert analyzer.total_number_of_characters_sent(start=dt(year=2018), period='y') == 167
    assert analyzer.total_number_of_characters_sent(start=dt(year=2020), period='y') == 84

    assert analyzer.total_number_of_characters_sent(start=dt(year=2014, month=9), period='m') == 24
    assert analyzer.total_number_of_characters_sent(start=dt(year=2014, month=11), period='m') == 33
    assert analyzer.total_number_of_characters_sent(start=dt(year=2014, month=12), period='m') == 3

    assert analyzer.total_number_of_characters_sent(start=dt(year=2018, month=1), period='m') == 167
    assert analyzer.total_number_of_characters_sent(start=dt(year=2018, month=2), period='m') == 0

    assert analyzer.total_number_of_characters_sent(start=dt(year=2020, month=2), period='m') == 62
    assert analyzer.total_number_of_characters_sent(start=dt(year=2020, month=3), period='m') == 0
    assert analyzer.total_number_of_characters_sent(start=dt(year=2020, month=4), period='m') == 17
    assert analyzer.total_number_of_characters_sent(start=dt(year=2020, month=5), period='m') == 0
    assert analyzer.total_number_of_characters_sent(start=dt(year=2020, month=6), period='m') == 0
    assert analyzer.total_number_of_characters_sent(start=dt(year=2020, month=8), period='m') == 5

    assert analyzer.total_number_of_characters_sent(start=dt(year=2020, month=2, day=13, hour=6), period='d') == 21
    assert analyzer.total_number_of_characters_sent(start=dt(year=2020, month=2, day=13, hour=7), period='d') == 0

    assert analyzer.total_number_of_characters_sent(start=dt(year=2020, month=2, day=13, hour=6), period='h') == 21
    assert analyzer.total_number_of_characters_sent(start=dt(year=2020, month=2, day=13, hour=7), period='h') == 0


def test_total_number_of_messages_received(analyzer):
    assert analyzer.total_number_of_messages_received() == 12
    assert analyzer.total_number_of_messages_received(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_messages_received(start=dt(year=2014), period='y') == 5
    assert analyzer.total_number_of_messages_received(start=dt(year=2018), period='y') == 1
    assert analyzer.total_number_of_messages_received(start=dt(year=2020), period='y') == 6

    assert analyzer.total_number_of_messages_received(start=dt(year=2011, month=11), period='m') == 0

    assert analyzer.total_number_of_messages_received(start=dt(year=2014, month=9), period='m') == 0
    assert analyzer.total_number_of_messages_received(start=dt(year=2014, month=11), period='m') == 4
    assert analyzer.total_number_of_messages_received(start=dt(year=2014, month=12), period='m') == 1

    assert analyzer.total_number_of_messages_received(start=dt(year=2018, month=1), period='m') == 1
    assert analyzer.total_number_of_messages_received(start=dt(year=2018, month=5), period='m') == 0

    assert analyzer.total_number_of_messages_received(start=dt(year=2020, month=2), period='m') == 4
    assert analyzer.total_number_of_messages_received(start=dt(year=2020, month=3), period='m') == 1
    assert analyzer.total_number_of_messages_received(start=dt(year=2020, month=4), period='m') == 0
    assert analyzer.total_number_of_messages_received(start=dt(year=2020, month=5), period='m') == 1
    assert analyzer.total_number_of_messages_received(start=dt(year=2020, month=8), period='m') == 0

    assert analyzer.total_number_of_messages_received(start=dt(year=2020, month=2, day=13), period='d') == 1
    assert analyzer.total_number_of_messages_received(start=dt(year=2020, month=2, day=14), period='d') == 2
    assert analyzer.total_number_of_messages_received(start=dt(year=2020, month=2, day=18), period='d') == 1


def test_total_number_of_words_received(analyzer):
    assert analyzer.total_number_of_words_received() == 17

    assert analyzer.total_number_of_words_received(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_words_received(start=dt(year=2014), period='y') == 4
    assert analyzer.total_number_of_words_received(start=dt(year=2018), period='y') == 1
    assert analyzer.total_number_of_words_received(start=dt(year=2020), period='y') == 12

    assert analyzer.total_number_of_words_received(start=dt(year=2014, month=9), period='m') == 0
    assert analyzer.total_number_of_words_received(start=dt(year=2014, month=11), period='m') == 4
    assert analyzer.total_number_of_words_received(start=dt(year=2014, month=12), period='m') == 0

    assert analyzer.total_number_of_words_received(start=dt(year=2018, month=1), period='m') == 1
    assert analyzer.total_number_of_words_received(start=dt(year=2018, month=2), period='m') == 0

    assert analyzer.total_number_of_words_received(start=dt(year=2020, month=2), period='m') == 11
    assert analyzer.total_number_of_words_received(start=dt(year=2020, month=3), period='m') == 0
    assert analyzer.total_number_of_words_received(start=dt(year=2020, month=5), period='m') == 1

    assert analyzer.total_number_of_words_received(start=dt(year=2020, month=2, day=13), period='d') == 9
    assert analyzer.total_number_of_words_received(start=dt(year=2020, month=2, day=14), period='d') == 2
    assert analyzer.total_number_of_words_received(start=dt(year=2020, month=2, day=18), period='d') == 0


def test_total_number_of_characters_received(analyzer):
    assert analyzer.total_number_of_characters_received() == 68

    assert analyzer.total_number_of_characters_received(start=dt(year=2000), period='y') == 0
    assert analyzer.total_number_of_characters_received(start=dt(year=2014), period='y') == 9
    assert analyzer.total_number_of_characters_received(start=dt(year=2018), period='y') == 3
    assert analyzer.total_number_of_characters_received(start=dt(year=2020), period='y') == 56

    assert analyzer.total_number_of_characters_received(start=dt(year=2014, month=9), period='m') == 0
    assert analyzer.total_number_of_characters_received(start=dt(year=2014, month=11), period='m') == 9
    assert analyzer.total_number_of_characters_received(start=dt(year=2014, month=12), period='m') == 0

    assert analyzer.total_number_of_characters_received(start=dt(year=2018, month=1), period='m') == 3
    assert analyzer.total_number_of_characters_received(start=dt(year=2018, month=2), period='m') == 0

    assert analyzer.total_number_of_characters_received(start=dt(year=2020, month=2), period='m') == 52
    assert analyzer.total_number_of_characters_received(start=dt(year=2020, month=3), period='m') == 0
    assert analyzer.total_number_of_characters_received(start=dt(year=2020, month=5), period='m') == 4

    assert analyzer.total_number_of_characters_received(start=dt(year=2020, month=2, day=13), period='d') == 30
    assert analyzer.total_number_of_characters_received(start=dt(year=2020, month=2, day=14), period='d') == 22
    assert analyzer.total_number_of_characters_received(start=dt(year=2020, month=2, day=18), period='d') == 0
