import pytest
from MessagingAnalyzer import MessagingAnalyzer
from People import People

TEST_DATA_PATH = '/home/levente/projects/facebook-data-miner/tests/test_data'


# TODO
# extend test data
# more tests


@pytest.fixture()
def people():
    # TODO solve paths
    p = People(path=TEST_DATA_PATH)
    p.to_individuals()
    return p


# def test_total_number_of_messages(people):
#     analyzer = MessagingAnalyzer(people.names, people.individuals)
#
#     assert analyzer.total_number_of_messages() == 14
#     assert analyzer.total_number_of_messages(year=2014) == 11
#     assert analyzer.total_number_of_messages(year=2018) == 3
#
#     assert analyzer.total_number_of_messages(year=2014, month=9) == 1
#     assert analyzer.total_number_of_messages(year=2014, month=11) == 8
#     assert analyzer.total_number_of_messages(year=2014, month=12) == 2
#     assert analyzer.total_number_of_messages(year=2018, month=1) == 3
#
#     assert analyzer.total_number_of_messages(year=2000) == 0
#     assert analyzer.total_number_of_messages(year=2011, month=11) == 0
#     assert analyzer.total_number_of_messages(year=2018, month=5) == 0
#
#
# def test_total_number_of_words(people):
#     analyzer = MessagingAnalyzer(people.names, people.individuals)
#
#     assert analyzer.total_number_of_words() == 24
#
#     assert analyzer.total_number_of_words(year=2000) == 0
#     assert analyzer.total_number_of_words(year=2014) == 20
#     assert analyzer.total_number_of_words(year=2018) == 4
#
#     assert analyzer.total_number_of_words(year=2014, month=9) == 6
#     assert analyzer.total_number_of_words(year=2014, month=11) == 13
#     assert analyzer.total_number_of_words(year=2014, month=12) == 1
#
#     assert analyzer.total_number_of_words(year=2018, month=1) == 4
#     assert analyzer.total_number_of_words(year=2018, month=2) == 0
#
#
# def test_total_number_of_characters(people):
#     analyzer = MessagingAnalyzer(people.names, people.individuals)
#
#     assert analyzer.total_number_of_characters() == 81
#
#     assert analyzer.total_number_of_characters(year=2000) == 0
#     assert analyzer.total_number_of_characters(year=2014) == 69
#     assert analyzer.total_number_of_characters(year=2018) == 12
#
#     assert analyzer.total_number_of_characters(year=2014, month=9) == 24
#     assert analyzer.total_number_of_characters(year=2014, month=11) == 42
#     assert analyzer.total_number_of_characters(year=2014, month=12) == 3
#
#     assert analyzer.total_number_of_characters(year=2018, month=1) == 12
#     assert analyzer.total_number_of_characters(year=2018, month=2) == 0
#
#
# def test_total_number_of_messages_sent(people):
#     analyzer = MessagingAnalyzer(people.names, people.individuals)
#     assert analyzer.total_number_of_messages_sent() == 8
#     assert analyzer.total_number_of_messages_sent(year=2014) == 6
#     assert analyzer.total_number_of_messages_sent(year=2018) == 2
#
#     assert analyzer.total_number_of_messages_sent(year=2014, month=9) == 1
#     assert analyzer.total_number_of_messages_sent(year=2014, month=11) == 4
#     assert analyzer.total_number_of_messages_sent(year=2014, month=12) == 1
#     assert analyzer.total_number_of_messages_sent(year=2018, month=1) == 2
#
#     assert analyzer.total_number_of_messages_sent(year=2000) == 0
#     assert analyzer.total_number_of_messages_sent(year=2011, month=11) == 0
#     assert analyzer.total_number_of_messages_sent(year=2018, month=5) == 0
#
#
# def test_total_number_of_words_sent(people):
#     analyzer = MessagingAnalyzer(people.names, people.individuals)
#
#     assert analyzer.total_number_of_words_sent() == 19
#
#     assert analyzer.total_number_of_words_sent(year=2000) == 0
#     assert analyzer.total_number_of_words_sent(year=2014) == 16
#     assert analyzer.total_number_of_words_sent(year=2018) == 3
#
#     assert analyzer.total_number_of_words_sent(year=2014, month=9) == 6
#     assert analyzer.total_number_of_words_sent(year=2014, month=11) == 9
#     assert analyzer.total_number_of_words_sent(year=2014, month=12) == 1
#
#     assert analyzer.total_number_of_words_sent(year=2018, month=1) == 3
#     assert analyzer.total_number_of_words_sent(year=2018, month=2) == 0
#
#
# def test_total_number_of_characters_sent(people):
#     analyzer = MessagingAnalyzer(people.names, people.individuals)
#
#     assert analyzer.total_number_of_characters_sent() == 69
#
#     assert analyzer.total_number_of_characters_sent(year=2000) == 0
#     assert analyzer.total_number_of_characters_sent(year=2014) == 60
#     assert analyzer.total_number_of_characters_sent(year=2018) == 9
#
#     assert analyzer.total_number_of_characters_sent(year=2014, month=9) == 24
#     assert analyzer.total_number_of_characters_sent(year=2014, month=11) == 33
#     assert analyzer.total_number_of_characters_sent(year=2014, month=12) == 3
#
#     assert analyzer.total_number_of_characters_sent(year=2018, month=1) == 9
#     assert analyzer.total_number_of_characters_sent(year=2018, month=2) == 0
#
#
# def test_total_number_of_messages_received(people):
#     analyzer = MessagingAnalyzer(people.names, people.individuals)
#     assert analyzer.total_number_of_messages_received() == 6
#     assert analyzer.total_number_of_messages_received(year=2014) == 5
#     assert analyzer.total_number_of_messages_received(year=2018) == 1
#
#     assert analyzer.total_number_of_messages_received(year=2014, month=9) == 0
#     assert analyzer.total_number_of_messages_received(year=2014, month=11) == 4
#     assert analyzer.total_number_of_messages_received(year=2014, month=12) == 1
#     assert analyzer.total_number_of_messages_received(year=2018, month=1) == 1
#
#     assert analyzer.total_number_of_messages_received(year=2000) == 0
#     assert analyzer.total_number_of_messages_received(year=2011, month=11) == 0
#     assert analyzer.total_number_of_messages_received(year=2018, month=5) == 0
#
#
# def test_total_number_of_words_received(people):
#     analyzer = MessagingAnalyzer(people.names, people.individuals)
#
#     assert analyzer.total_number_of_words_received() == 5
#
#     assert analyzer.total_number_of_words_received(year=2000) == 0
#     assert analyzer.total_number_of_words_received(year=2014) == 4
#     assert analyzer.total_number_of_words_received(year=2018) == 1
#
#     assert analyzer.total_number_of_words_received(year=2014, month=9) == 0
#     assert analyzer.total_number_of_words_received(year=2014, month=11) == 4
#     assert analyzer.total_number_of_words_received(year=2014, month=12) == 0
#
#     assert analyzer.total_number_of_words_received(year=2018, month=1) == 1
#     assert analyzer.total_number_of_words_received(year=2018, month=2) == 0
#
#
# def test_total_number_of_characters_received(people):
#     analyzer = MessagingAnalyzer(people.names, people.individuals)
#
#     assert analyzer.total_number_of_characters_received() == 12
#
#     assert analyzer.total_number_of_characters_received(year=2000) == 0
#     assert analyzer.total_number_of_characters_received(year=2014) == 9
#     assert analyzer.total_number_of_characters_received(year=2018) == 3
#
#     assert analyzer.total_number_of_characters_received(year=2014, month=9) == 0
#     assert analyzer.total_number_of_characters_received(year=2014, month=11) == 9
#     assert analyzer.total_number_of_characters_received(year=2014, month=12) == 0
#
#     assert analyzer.total_number_of_characters_received(year=2018, month=1) == 3
#     assert analyzer.total_number_of_characters_received(year=2018, month=2) == 0


def test_time_series_analysis(people):
    analyzer = MessagingAnalyzer(people.names, people.individuals)

    analyzer.time_series_analysis_for_user(name='Tőke Hal')
    #master_df = analyzer.stack_all_dfs()
    #assert len(master_df) == 14
