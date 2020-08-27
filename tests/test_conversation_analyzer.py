import pytest

from miner.utils import dt


@pytest.fixture(scope="session")
def statistics(analyzer):
    def _stats(**kwargs):
        if any([kw in kwargs for kw in ("names", "subject", "start", "end")]):
            return analyzer.get_stats(**kwargs)
        else:
            return analyzer.stats

    return _stats


def test_get_grouped_time_series_data(analyzer):
    grouped = analyzer.get_grouped_time_series_data(period="y")
    assert len(grouped) == 3
    third_row = grouped.iloc[2]
    assert third_row.msg_count == 15
    assert third_row.media_count == 7
    assert third_row.word_count == 34
    assert third_row.char_count == 140

    grouped = analyzer.get_grouped_time_series_data(period="m")
    assert len(grouped) == 9

    grouped = analyzer.get_grouped_time_series_data(period="d")
    assert len(grouped) == 16

    grouped = analyzer.get_grouped_time_series_data(period="h")
    assert len(grouped) == 24


def test_stats_per_period(analyzer):
    yearly = analyzer.stat_per_period("y", "msg_count")
    assert yearly == {
        2009: 0,
        2010: 0,
        2011: 0,
        2012: 0,
        2013: 0,
        2014: 13,
        2015: 0,
        2016: 0,
        2017: 0,
        2018: 3,
        2019: 0,
        2020: 15,
    }

    monthly = analyzer.stat_per_period("m", "msg_count")
    assert monthly == {
        "january": 3,
        "february": 10,
        "march": 1,
        "april": 2,
        "may": 1,
        "june": 0,
        "july": 0,
        "august": 1,
        "september": 1,
        "october": 0,
        "november": 10,
        "december": 2,
    }

    daily = analyzer.stat_per_period("d", "msg_count")
    assert daily == {
        "monday": 6,
        "tuesday": 2,
        "wednesday": 6,
        "thursday": 3,
        "friday": 6,
        "saturday": 3,
        "sunday": 5,
    }

    hourly = analyzer.stat_per_period("h", "msg_count")
    assert hourly == {
        0: 1,
        1: 1,
        2: 1,
        3: 0,
        4: 1,
        5: 0,
        6: 2,
        7: 0,
        8: 1,
        9: 1,
        10: 0,
        11: 1,
        12: 7,
        13: 1,
        14: 0,
        15: 1,
        16: 1,
        17: 1,
        18: 1,
        19: 1,
        20: 4,
        21: 0,
        22: 2,
        23: 3,
    }


def test_ranking(analyzer):
    ranking = analyzer.get_ranking_of_partners_by_messages()
    assert ranking == {
        "Foo Bar": 15,
        "Tőke Hal": 7,
        "Teflon Musk": 6,
        "Benedek Elek": 3,
    }


def test_stats_toke_hal_all(statistics):
    stats = statistics(names="Tőke Hal")

    assert stats.msg_count == 7
    assert stats.unique_msg_count == 6
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 11
    assert stats.unique_word_count == 9
    # assert stats.word_frequency == 0
    assert stats.char_count == 47
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_me(statistics):
    stats = statistics(names="Tőke Hal", subject="me")

    assert stats.msg_count == 4
    assert stats.unique_msg_count == 4
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 6
    assert stats.unique_word_count == 5
    # assert stats.word_frequency == 0
    assert stats.char_count == 22
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_partner(statistics):
    stats = statistics(names="Tőke Hal", subject="partner")

    assert stats.msg_count == 3
    assert stats.unique_msg_count == 3
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 5
    assert stats.unique_word_count == 5
    # assert stats.word_frequency == 0
    assert stats.char_count == 25
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_all_2014_11(statistics):
    stats = statistics(names="Tőke Hal", subject="all", start=dt(2014, 11), period="m")

    assert stats.msg_count == 6
    assert stats.unique_msg_count == 5
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    # assert stats.word_frequency == 0
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_partner_2014_11(statistics):
    stats = statistics(
        names="Tőke Hal", subject="partner", start=dt(2014, 11), period="m"
    )
    assert stats.char_count == 25
    assert stats.word_count == 5


def test_stats_toke_hal_me_2014_11(statistics):
    stats = statistics(names="Tőke Hal", subject="me", start=dt(2014, 11), period="m")
    assert stats.unique_word_count == 5


#
def test_stats_toke_hal_all_2014_12(statistics):
    stats = statistics(names="Tőke Hal", subject="all", start=dt(2014, 12), period="m")
    assert stats.msg_count == 1
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.unique_word_count == 1
    # assert stats.word_frequency == 0
    assert stats.char_count == 3
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_partner_2014_12(statistics):
    stats = statistics(
        names="Tőke Hal", subject="partner", start=dt(2014, 12), period="m"
    )
    assert stats.word_count == 0


def test_stats_toke_hal_me_2014_12(statistics):
    stats = statistics(names="Tőke Hal", subject="me", start=dt(2014, 12), period="m")
    assert stats.unique_msg_count == 1


class TestGetStats:
    def test_stats_teflon_musk(self, statistics):
        stats = statistics(names="Teflon Musk")
        assert stats.msg_count == 6
        assert stats.unique_msg_count == 2
        # assert stats.most_used_msgs == 0 # TODO LATER should only return the most used or e.g. top10 most used
        # assert stats.msg_frequency == 0
        assert stats.word_count == 14
        assert stats.unique_word_count == 7
        # assert stats.word_frequency == 0
        assert stats.char_count == 52  # 23
        # assert stats.most_used_chars == 0

    def test_stats_teflon_musk_me(self, statistics):
        stats = statistics(names="Teflon Musk", subject="me")
        assert stats.msg_count == 3
        assert stats.unique_msg_count == 1
        # assert stats.most_used_msgs == 0
        # assert stats.msg_frequency == 0
        assert stats.word_count == 12
        assert stats.unique_word_count == 6
        # assert stats.word_frequency == 0
        assert stats.char_count == 48
        # assert stats.most_used_chars == 0

    def test_stats_teflon_musk_partner(self, statistics):
        stats = statistics(names="Teflon Musk", subject="partner")
        assert stats.msg_count == 3
        assert stats.unique_msg_count == 1
        # assert stats.most_used_msgs == 0
        # assert stats.msg_frequency == 0
        assert stats.word_count == 2
        assert stats.unique_word_count == 1
        # assert stats.word_frequency == 0
        assert stats.char_count == 4
        # assert stats.most_used_chars == 0

    def test_stats_teflon_musk_all_2014_9(self, statistics):
        stats = statistics(
            names="Teflon Musk", subject="all", start=dt(2014, 9), period="m"
        )
        assert stats.msg_count == 1
        # assert stats.most_used_msgs == 0
        # assert stats.msg_frequency == 0
        assert stats.word_count == 6
        # assert stats.word_frequency == 0
        # assert stats.most_used_chars == 0

    def test_stats_teflon_musk_me_2014_9(self, statistics):
        stats = statistics(
            names="Teflon Musk", subject="me", start=dt(2014, 9), period="m"
        )
        assert stats.unique_word_count == 6

    def test_stats_teflon_musk_partner_2014_9(self, statistics):
        stats = statistics(
            names="Teflon Musk", subject="partner", start=dt(2014, 9), period="m"
        )
        assert stats.unique_msg_count == 0
        assert stats.char_count == 0

    def test_stats_teflon_musk_all_2014_11(self, statistics):
        stats = statistics(
            names="Teflon Musk", subject="all", start=dt(2014, 11), period="m"
        )
        assert stats.msg_count == 4
        # assert stats.most_used_msgs == 0
        # assert stats.msg_frequency == 0
        # assert stats.word_frequency == 0
        # assert stats.most_used_chars == 0

    def test_stats_teflon_musk_me_2014_11(self, statistics):
        stats = statistics(
            names="Teflon Musk", subject="me", start=dt(2014, 11), period="m"
        )
        assert stats.word_count == 6

    def test_stats_teflon_musk_partner_2014_11(self, statistics):
        stats = statistics(
            names="Teflon Musk", subject="partner", start=dt(2014, 11), period="m"
        )
        assert stats.unique_msg_count == 1
        assert stats.unique_word_count == 1
        assert stats.char_count == 4

    def test_stats_teflon_musk_all_2014_12(self, statistics):
        stats = statistics(
            names="Teflon Musk", subject="all", start=dt(2014, 12), period="m"
        )

        assert stats.msg_count == 1
        assert stats.unique_msg_count == 0
        # assert stats.most_used_msgs == 0
        # assert stats.msg_frequency == 0
        assert stats.word_count == 0
        assert stats.unique_word_count == 0
        # assert stats.word_frequency == 0
        assert stats.char_count == 0
        # assert stats.most_used_chars == 0


class TestGetCount:
    def test_total_number_of_messages(self, analyzer):
        assert analyzer.get_stat_count(attribute="msg_count",) == 31

        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2000), period="y"
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2014), period="y"
            )
            == 13
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2018), period="y"
            )
            == 3
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2020), period="y"
            )
            == 15
        )

        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2011, month=11), period="m"
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2014, month=9), period="m"
            )
            == 1
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2014, month=11), period="m"
            )
            == 10
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2014, month=12), period="m"
            )
            == 2
        )

        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2018, month=1), period="m"
            )
            == 3
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2018, month=5), period="m"
            )
            == 0
        )

        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2020, month=2), period="m"
            )
            == 10
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2020, month=3), period="m"
            )
            == 1
        )  # jpg
        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2020, month=4), period="m"
            )
            == 2
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2020, month=5), period="m"
            )
            == 1
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2020, month=6), period="m"
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2020, month=8), period="m"
            )
            == 1
        )

        assert (
            analyzer.get_stat_count(
                attribute="msg_count", start=dt(year=2020, month=2, day=13), period="d"
            )
            == 2
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                start=dt(year=2020, month=2, day=13, hour=6),
                period="h",
            )
            == 2
        )

        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                start=dt(year=2020, month=2, day=13, hour=6),
                period="d",
            )
            == 4
        )

    def test_total_number_of_words(self, analyzer):
        assert analyzer.get_stat_count(attribute="word_count",) == 91

        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2000), period="y"
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2014), period="y"
            )
            == 25
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2018), period="y"
            )
            == 32
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2020), period="y"
            )
            == 34
        )

        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2014, month=9), period="m"
            )
            == 6
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2014, month=11), period="m"
            )
            == 18
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2014, month=12), period="m"
            )
            == 1
        )

        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2018, month=1), period="m"
            )
            == 32
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2018, month=2), period="m"
            )
            == 0
        )

        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2020, month=2), period="m"
            )
            == 27
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2020, month=3), period="m"
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2020, month=4), period="m"
            )
            == 4
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2020, month=5), period="m"
            )
            == 1
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2020, month=6), period="m"
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2020, month=8), period="m"
            )
            == 2
        )

        assert (
            analyzer.get_stat_count(
                attribute="word_count", start=dt(year=2020, month=2, day=13), period="d"
            )
            == 14
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                start=dt(year=2020, month=2, day=13, hour=5),
                period="d",
            )
            == 14
        )

    def test_total_number_of_characters(self, analyzer):
        assert analyzer.get_stat_count(attribute="char_count",) == 409

        assert (
            analyzer.get_stat_count(
                attribute="char_count", start=dt(year=2000), period="y"
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count", start=dt(year=2014), period="y"
            )
            == 99
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count", start=dt(year=2018), period="y"
            )
            == 170
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count", start=dt(year=2020), period="y"
            )
            == 140
        )

        assert (
            analyzer.get_stat_count(
                attribute="char_count", start=dt(year=2014, month=9), period="m"
            )
            == 24
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count", start=dt(year=2014, month=11), period="m"
            )
            == 72
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count", start=dt(year=2014, month=12), period="m"
            )
            == 3
        )

        assert (
            analyzer.get_stat_count(
                attribute="char_count", start=dt(year=2018, month=1), period="m"
            )
            == 170
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count", start=dt(year=2018, month=2), period="m"
            )
            == 0
        )

        assert (
            analyzer.get_stat_count(
                attribute="char_count", start=dt(year=2020, month=2), period="m"
            )
            == 114
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count", start=dt(year=2020, month=3), period="m"
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count", start=dt(year=2020, month=4), period="m"
            )
            == 17
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count", start=dt(year=2020, month=5), period="m"
            )
            == 4
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count", start=dt(year=2020, month=6), period="m"
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count", start=dt(year=2020, month=8), period="m"
            )
            == 5
        )

    def test_total_number_of_messages_sent(self, analyzer):
        assert analyzer.get_stat_count(attribute="msg_count", subject="me",) == 18
        assert (
            analyzer.get_stat_count(
                attribute="msg_count", subject="me", start=dt(year=2014), period="y"
            )
            == 7
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count", subject="me", start=dt(year=2018), period="y"
            )
            == 2
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count", subject="me", start=dt(year=2020), period="y"
            )
            == 9
        )

        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="me",
                start=dt(year=2014, month=9),
                period="m",
            )
            == 1
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="me",
                start=dt(year=2014, month=11),
                period="m",
            )
            == 5
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="me",
                start=dt(year=2014, month=12),
                period="m",
            )
            == 1
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="me",
                start=dt(year=2018, month=1),
                period="m",
            )
            == 2
        )

        assert (
            analyzer.get_stat_count(
                attribute="msg_count", subject="me", start=dt(year=2000), period="y"
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="me",
                start=dt(year=2011, month=11),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="me",
                start=dt(year=2018, month=5),
                period="m",
            )
            == 0
        )

        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="me",
                start=dt(year=2020, month=2),
                period="m",
            )
            == 6
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="me",
                start=dt(year=2020, month=3),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="me",
                start=dt(year=2020, month=4),
                period="m",
            )
            == 2
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="me",
                start=dt(year=2020, month=5),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="me",
                start=dt(year=2020, month=6),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="me",
                start=dt(year=2020, month=8),
                period="m",
            )
            == 1
        )

        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="me",
                start=dt(year=2020, month=2, day=13),
                period="d",
            )
            == 1
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="me",
                start=dt(year=2020, month=2, day=13, hour=6),
                period="h",
            )
            == 1
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="me",
                start=dt(year=2020, month=2, day=13, hour=18),
                period="h",
            )
            == 0
        )

    def test_total_number_of_words_sent(self, analyzer):
        assert analyzer.get_stat_count(attribute="word_count", subject="me",) == 71

        assert (
            analyzer.get_stat_count(
                attribute="word_count", subject="me", start=dt(year=2000), period="y"
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count", subject="me", start=dt(year=2014), period="y"
            )
            == 18
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count", subject="me", start=dt(year=2018), period="y"
            )
            == 31
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count", subject="me", start=dt(year=2020), period="y"
            )
            == 22
        )

        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="me",
                start=dt(year=2014, month=9),
                period="m",
            )
            == 6
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="me",
                start=dt(year=2014, month=11),
                period="m",
            )
            == 11
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="me",
                start=dt(year=2014, month=12),
                period="m",
            )
            == 1
        )

        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="me",
                start=dt(year=2018, month=1),
                period="m",
            )
            == 31
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="me",
                start=dt(year=2018, month=2),
                period="m",
            )
            == 0
        )

        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="me",
                start=dt(year=2020, month=2),
                period="m",
            )
            == 16
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="me",
                start=dt(year=2020, month=3),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="me",
                start=dt(year=2020, month=4),
                period="m",
            )
            == 4
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="me",
                start=dt(year=2020, month=5),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="me",
                start=dt(year=2020, month=6),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="me",
                start=dt(year=2020, month=8),
                period="m",
            )
            == 2
        )

        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="me",
                start=dt(year=2020, month=2, day=13),
                period="d",
            )
            == 5
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="me",
                start=dt(year=2020, month=2, day=13, hour=6),
                period="h",
            )
            == 5
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="me",
                start=dt(year=2020, month=2, day=13, hour=7),
                period="h",
            )
            == 0
        )

    def test_total_number_of_characters_sent(self, analyzer):
        assert analyzer.get_stat_count(attribute="char_count", subject="me",) == 321

        assert (
            analyzer.get_stat_count(
                attribute="char_count", subject="me", start=dt(year=2000), period="y"
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count", subject="me", start=dt(year=2014), period="y"
            )
            == 70
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count", subject="me", start=dt(year=2018), period="y"
            )
            == 167
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count", subject="me", start=dt(year=2020), period="y"
            )
            == 84
        )

        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="me",
                start=dt(year=2014, month=9),
                period="m",
            )
            == 24
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="me",
                start=dt(year=2014, month=11),
                period="m",
            )
            == 43
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="me",
                start=dt(year=2014, month=12),
                period="m",
            )
            == 3
        )

        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="me",
                start=dt(year=2018, month=1),
                period="m",
            )
            == 167
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="me",
                start=dt(year=2018, month=2),
                period="m",
            )
            == 0
        )

        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="me",
                start=dt(year=2020, month=2),
                period="m",
            )
            == 62
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="me",
                start=dt(year=2020, month=3),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="me",
                start=dt(year=2020, month=4),
                period="m",
            )
            == 17
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="me",
                start=dt(year=2020, month=5),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="me",
                start=dt(year=2020, month=6),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="me",
                start=dt(year=2020, month=8),
                period="m",
            )
            == 5
        )

        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="me",
                start=dt(year=2020, month=2, day=13, hour=6),
                period="d",
            )
            == 21
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="me",
                start=dt(year=2020, month=2, day=13, hour=7),
                period="d",
            )
            == 0
        )

        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="me",
                start=dt(year=2020, month=2, day=13, hour=6),
                period="h",
            )
            == 21
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="me",
                start=dt(year=2020, month=2, day=13, hour=7),
                period="h",
            )
            == 0
        )

    def test_total_number_of_messages_received(self, analyzer):
        assert analyzer.get_stat_count(attribute="msg_count", subject="partner",) == 13
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2000),
                period="y",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2014),
                period="y",
            )
            == 6
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2018),
                period="y",
            )
            == 1
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2020),
                period="y",
            )
            == 6
        )

        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2011, month=11),
                period="m",
            )
            == 0
        )

        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2014, month=9),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2014, month=11),
                period="m",
            )
            == 5
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2014, month=12),
                period="m",
            )
            == 1
        )

        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2018, month=1),
                period="m",
            )
            == 1
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2018, month=5),
                period="m",
            )
            == 0
        )

        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2020, month=2),
                period="m",
            )
            == 4
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2020, month=3),
                period="m",
            )
            == 1
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2020, month=4),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2020, month=5),
                period="m",
            )
            == 1
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2020, month=8),
                period="m",
            )
            == 0
        )

        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2020, month=2, day=13),
                period="d",
            )
            == 1
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2020, month=2, day=14),
                period="d",
            )
            == 2
        )
        assert (
            analyzer.get_stat_count(
                attribute="msg_count",
                subject="partner",
                start=dt(year=2020, month=2, day=18),
                period="d",
            )
            == 1
        )

    def test_total_number_of_words_received(self, analyzer):
        assert analyzer.get_stat_count(attribute="word_count", subject="partner",) == 20

        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="partner",
                start=dt(year=2000),
                period="y",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="partner",
                start=dt(year=2014),
                period="y",
            )
            == 7
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="partner",
                start=dt(year=2018),
                period="y",
            )
            == 1
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="partner",
                start=dt(year=2020),
                period="y",
            )
            == 12
        )

        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="partner",
                start=dt(year=2014, month=9),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="partner",
                start=dt(year=2014, month=11),
                period="m",
            )
            == 7
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="partner",
                start=dt(year=2014, month=12),
                period="m",
            )
            == 0
        )

        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="partner",
                start=dt(year=2018, month=1),
                period="m",
            )
            == 1
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="partner",
                start=dt(year=2018, month=2),
                period="m",
            )
            == 0
        )

        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="partner",
                start=dt(year=2020, month=2),
                period="m",
            )
            == 11
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="partner",
                start=dt(year=2020, month=3),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="partner",
                start=dt(year=2020, month=5),
                period="m",
            )
            == 1
        )

        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="partner",
                start=dt(year=2020, month=2, day=13),
                period="d",
            )
            == 9
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="partner",
                start=dt(year=2020, month=2, day=14),
                period="d",
            )
            == 2
        )
        assert (
            analyzer.get_stat_count(
                attribute="word_count",
                subject="partner",
                start=dt(year=2020, month=2, day=18),
                period="d",
            )
            == 0
        )

    def test_total_number_of_characters_received(self, analyzer):
        assert analyzer.get_stat_count(attribute="char_count", subject="partner",) == 88

        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="partner",
                start=dt(year=2000),
                period="y",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="partner",
                start=dt(year=2014),
                period="y",
            )
            == 29
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="partner",
                start=dt(year=2018),
                period="y",
            )
            == 3
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="partner",
                start=dt(year=2020),
                period="y",
            )
            == 56
        )

        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="partner",
                start=dt(year=2014, month=9),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="partner",
                start=dt(year=2014, month=11),
                period="m",
            )
            == 29
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="partner",
                start=dt(year=2014, month=12),
                period="m",
            )
            == 0
        )

        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="partner",
                start=dt(year=2018, month=1),
                period="m",
            )
            == 3
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="partner",
                start=dt(year=2018, month=2),
                period="m",
            )
            == 0
        )

        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="partner",
                start=dt(year=2020, month=2),
                period="m",
            )
            == 52
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="partner",
                start=dt(year=2020, month=3),
                period="m",
            )
            == 0
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="partner",
                start=dt(year=2020, month=5),
                period="m",
            )
            == 4
        )

        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="partner",
                start=dt(year=2020, month=2, day=13),
                period="d",
            )
            == 30
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="partner",
                start=dt(year=2020, month=2, day=14),
                period="d",
            )
            == 22
        )
        assert (
            analyzer.get_stat_count(
                attribute="char_count",
                subject="partner",
                start=dt(year=2020, month=2, day=18),
                period="d",
            )
            == 0
        )
