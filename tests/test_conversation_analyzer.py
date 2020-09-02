import pytest

from miner.utils import dt


@pytest.fixture(scope="session")
def statistics(analyzer):
    def _stats(**kwargs):
        if any([kw in kwargs for kw in ("names", "subject", "start", "end")]):
            return analyzer.get_stats(**kwargs)
        else:
            return analyzer.priv_stats

    return _stats


@pytest.fixture(scope="session")
def stat_count(analyzer):
    return analyzer.get_stat_count


class TestGroupRelatedAnalyzerMethods:
    def test_get_all_groups_for_one_person(self, analyzer):
        list_of_groups = analyzer.get_all_groups_for_one_person("Teflon Musk")
        assert len(list_of_groups) == 2

    # def test_group_mean_size(self, analyzer):
    #     mean = analyzer.group_mean_size
    #     assert mean == 4
    #
    # def test_group_max_size(self, analyzer):
    #     max = analyzer.group_max_size
    #     assert max == 5


def test_analyzer_groups(analyzer):
    groups = analyzer.groups
    assert len(groups) == 3


def test_get_grouped_time_series_data(analyzer):
    grouped = analyzer.get_grouped_time_series_data(period="y")
    assert len(grouped) == 3
    third_row = grouped.iloc[2]
    assert third_row.mc == 15
    assert third_row.media_mc == 7
    assert third_row.wc == 34
    assert third_row.cc == 140

    grouped = analyzer.get_grouped_time_series_data(period="m")
    assert len(grouped) == 9

    grouped = analyzer.get_grouped_time_series_data(period="d")
    assert len(grouped) == 16

    grouped = analyzer.get_grouped_time_series_data(period="h")
    assert len(grouped) == 24


def test_stats_per_period(analyzer):
    yearly = analyzer.stat_per_period("y", "mc")
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

    monthly = analyzer.stat_per_period("m", "mc")
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

    daily = analyzer.stat_per_period("d", "mc")
    assert daily == {
        "monday": 6,
        "tuesday": 2,
        "wednesday": 6,
        "thursday": 3,
        "friday": 6,
        "saturday": 3,
        "sunday": 5,
    }

    hourly = analyzer.stat_per_period("h", "mc")
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

    assert stats.mc == 7
    assert stats.unique_mc == 6
    # assert stats.most_used_msgs == 0
    assert stats.wc == 11
    assert stats.unique_wc == 9
    assert stats.cc == 47
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_me(statistics):
    stats = statistics(names="Tőke Hal", subject="me")

    assert stats.mc == 4
    assert stats.unique_mc == 4
    # assert stats.most_used_msgs == 0
    assert stats.wc == 6
    assert stats.unique_wc == 5
    assert stats.cc == 22
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_partner(statistics):
    stats = statistics(names="Tőke Hal", subject="partner")

    assert stats.mc == 3
    assert stats.unique_mc == 3
    # assert stats.most_used_msgs == 0
    assert stats.wc == 5
    assert stats.unique_wc == 5
    assert stats.cc == 25
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_all_2014_11(statistics):
    stats = statistics(names="Tőke Hal", subject="all", start=dt(2014, 11), period="m")

    assert stats.mc == 6
    assert stats.unique_mc == 5
    # assert stats.most_used_msgs == 0
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_partner_2014_11(statistics):
    stats = statistics(
        names="Tőke Hal", subject="partner", start=dt(2014, 11), period="m"
    )
    assert stats.cc == 25
    assert stats.wc == 5


def test_stats_toke_hal_me_2014_11(statistics):
    stats = statistics(names="Tőke Hal", subject="me", start=dt(2014, 11), period="m")
    assert stats.unique_wc == 5


#
def test_stats_toke_hal_all_2014_12(statistics):
    stats = statistics(names="Tőke Hal", subject="all", start=dt(2014, 12), period="m")
    assert stats.mc == 1
    # assert stats.most_used_msgs == 0
    assert stats.unique_wc == 1
    assert stats.cc == 3
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_partner_2014_12(statistics):
    stats = statistics(
        names="Tőke Hal", subject="partner", start=dt(2014, 12), period="m"
    )
    assert stats.wc == 0


def test_stats_toke_hal_me_2014_12(statistics):
    stats = statistics(names="Tőke Hal", subject="me", start=dt(2014, 12), period="m")
    assert stats.unique_mc == 1


class TestGetStats:
    def test_stats_teflon_musk(self, statistics):
        stats = statistics(names="Teflon Musk")
        assert stats.mc == 6
        assert stats.unique_mc == 2
        # assert stats.most_used_msgs == 0 # TODO LATER should only return the most used or e.g. top10 most used
        assert stats.wc == 14
        assert stats.unique_wc == 7
        assert stats.cc == 52  # 23
        # assert stats.most_used_chars == 0

    def test_stats_teflon_musk_me(self, statistics):
        stats = statistics(names="Teflon Musk", subject="me")
        assert stats.mc == 3
        assert stats.unique_mc == 1
        # assert stats.most_used_msgs == 0
        assert stats.wc == 12
        assert stats.unique_wc == 6
        assert stats.cc == 48
        # assert stats.most_used_chars == 0

    def test_stats_teflon_musk_partner(self, statistics):
        stats = statistics(names="Teflon Musk", subject="partner")
        assert stats.mc == 3
        assert stats.unique_mc == 1
        # assert stats.most_used_msgs == 0
        assert stats.wc == 2
        assert stats.unique_wc == 1
        assert stats.cc == 4
        # assert stats.most_used_chars == 0

    def test_stats_teflon_musk_all_2014_9(self, statistics):
        stats = statistics(
            names="Teflon Musk", subject="all", start=dt(2014, 9), period="m"
        )
        assert stats.mc == 1
        # assert stats.most_used_msgs == 0
        assert stats.wc == 6
        # assert stats.most_used_chars == 0

    def test_stats_teflon_musk_me_2014_9(self, statistics):
        stats = statistics(
            names="Teflon Musk", subject="me", start=dt(2014, 9), period="m"
        )
        assert stats.unique_wc == 6

    def test_stats_teflon_musk_partner_2014_9(self, statistics):
        stats = statistics(
            names="Teflon Musk", subject="partner", start=dt(2014, 9), period="m"
        )
        assert stats.unique_mc == 0
        assert stats.cc == 0

    def test_stats_teflon_musk_all_2014_11(self, statistics):
        stats = statistics(
            names="Teflon Musk", subject="all", start=dt(2014, 11), period="m"
        )
        assert stats.mc == 4
        # assert stats.most_used_msgs == 0
        # assert stats.most_used_chars == 0

    def test_stats_teflon_musk_me_2014_11(self, statistics):
        stats = statistics(
            names="Teflon Musk", subject="me", start=dt(2014, 11), period="m"
        )
        assert stats.wc == 6

    def test_stats_teflon_musk_partner_2014_11(self, statistics):
        stats = statistics(
            names="Teflon Musk", subject="partner", start=dt(2014, 11), period="m"
        )
        assert stats.unique_mc == 1
        assert stats.unique_wc == 1
        assert stats.cc == 4

    def test_stats_teflon_musk_all_2014_12(self, statistics):
        stats = statistics(
            names="Teflon Musk", subject="all", start=dt(2014, 12), period="m"
        )

        assert stats.mc == 1
        assert stats.unique_mc == 0
        # assert stats.most_used_msgs == 0
        assert stats.wc == 0
        assert stats.unique_wc == 0
        assert stats.cc == 0
        # assert stats.most_used_chars == 0


class TestGetCount:
    def test_total_number_of_messages(self, stat_count):
        assert stat_count(attribute="mc",) == 31

        assert stat_count(attribute="mc", start=dt(y=2000), period="y") == 0
        assert stat_count(attribute="mc", start=dt(y=2014), period="y") == 13
        assert stat_count(attribute="mc", start=dt(y=2018), period="y") == 3
        assert stat_count(attribute="mc", start=dt(y=2020), period="y") == 15

        assert stat_count(attribute="mc", start=dt(y=2011, m=11), period="m") == 0
        assert stat_count(attribute="mc", start=dt(y=2014, m=9), period="m") == 1
        assert stat_count(attribute="mc", start=dt(y=2014, m=11), period="m") == 10
        assert stat_count(attribute="mc", start=dt(y=2014, m=12), period="m") == 2

        assert stat_count(attribute="mc", start=dt(y=2018, m=1), period="m") == 3
        assert stat_count(attribute="mc", start=dt(y=2018, m=5), period="m") == 0

        assert stat_count(attribute="mc", start=dt(y=2020, m=2), period="m") == 10
        assert stat_count(attribute="mc", start=dt(y=2020, m=3), period="m") == 1  # jpg
        assert stat_count(attribute="mc", start=dt(y=2020, m=4), period="m") == 2
        assert stat_count(attribute="mc", start=dt(y=2020, m=5), period="m") == 1
        assert stat_count(attribute="mc", start=dt(y=2020, m=6), period="m") == 0
        assert stat_count(attribute="mc", start=dt(y=2020, m=8), period="m") == 1

        assert stat_count(attribute="mc", start=dt(y=2020, m=2, d=13), period="d") == 2
        assert (
            stat_count(attribute="mc", start=dt(y=2020, m=2, d=13, h=6), period="h",)
            == 2
        )

        assert (
            stat_count(attribute="mc", start=dt(y=2020, m=2, d=13, h=6), period="d",)
            == 4
        )

    def test_total_number_of_words(self, stat_count):
        assert stat_count(attribute="wc",) == 91

        assert stat_count(attribute="wc", start=dt(y=2000), period="y") == 0
        assert stat_count(attribute="wc", start=dt(y=2014), period="y") == 25
        assert stat_count(attribute="wc", start=dt(y=2018), period="y") == 32
        assert stat_count(attribute="wc", start=dt(y=2020), period="y") == 34

        assert stat_count(attribute="wc", start=dt(y=2014, m=9), period="m") == 6
        assert stat_count(attribute="wc", start=dt(y=2014, m=11), period="m") == 18
        assert stat_count(attribute="wc", start=dt(y=2014, m=12), period="m") == 1

        assert stat_count(attribute="wc", start=dt(y=2018, m=1), period="m") == 32
        assert stat_count(attribute="wc", start=dt(y=2018, m=2), period="m") == 0

        assert stat_count(attribute="wc", start=dt(y=2020, m=2), period="m") == 27
        assert stat_count(attribute="wc", start=dt(y=2020, m=3), period="m") == 0
        assert stat_count(attribute="wc", start=dt(y=2020, m=4), period="m") == 4
        assert stat_count(attribute="wc", start=dt(y=2020, m=5), period="m") == 1
        assert stat_count(attribute="wc", start=dt(y=2020, m=6), period="m") == 0
        assert stat_count(attribute="wc", start=dt(y=2020, m=8), period="m") == 2

        assert stat_count(attribute="wc", start=dt(y=2020, m=2, d=13), period="d") == 14
        assert (
            stat_count(attribute="wc", start=dt(y=2020, m=2, d=13, h=5), period="d",)
            == 14
        )

    def test_total_number_of_characters(self, stat_count):
        assert stat_count(attribute="cc",) == 409

        assert stat_count(attribute="cc", start=dt(y=2000), period="y") == 0
        assert stat_count(attribute="cc", start=dt(y=2014), period="y") == 99
        assert stat_count(attribute="cc", start=dt(y=2018), period="y") == 170
        assert stat_count(attribute="cc", start=dt(y=2020), period="y") == 140

        assert stat_count(attribute="cc", start=dt(y=2014, m=9), period="m") == 24
        assert stat_count(attribute="cc", start=dt(y=2014, m=11), period="m") == 72
        assert stat_count(attribute="cc", start=dt(y=2014, m=12), period="m") == 3

        assert stat_count(attribute="cc", start=dt(y=2018, m=1), period="m") == 170
        assert stat_count(attribute="cc", start=dt(y=2018, m=2), period="m") == 0

        assert stat_count(attribute="cc", start=dt(y=2020, m=2), period="m") == 114
        assert stat_count(attribute="cc", start=dt(y=2020, m=3), period="m") == 0
        assert stat_count(attribute="cc", start=dt(y=2020, m=4), period="m") == 17
        assert stat_count(attribute="cc", start=dt(y=2020, m=5), period="m") == 4
        assert stat_count(attribute="cc", start=dt(y=2020, m=6), period="m") == 0
        assert stat_count(attribute="cc", start=dt(y=2020, m=8), period="m") == 5

    def test_total_number_of_messages_sent(self, stat_count):
        assert stat_count(attribute="mc", subject="me",) == 18
        assert (
            stat_count(attribute="mc", subject="me", start=dt(y=2014), period="y") == 7
        )
        assert (
            stat_count(attribute="mc", subject="me", start=dt(y=2018), period="y") == 2
        )
        assert (
            stat_count(attribute="mc", subject="me", start=dt(y=2020), period="y") == 9
        )

        assert (
            stat_count(attribute="mc", subject="me", start=dt(y=2014, m=9), period="m",)
            == 1
        )
        assert (
            stat_count(
                attribute="mc", subject="me", start=dt(y=2014, m=11), period="m",
            )
            == 5
        )
        assert (
            stat_count(
                attribute="mc", subject="me", start=dt(y=2014, m=12), period="m",
            )
            == 1
        )
        assert (
            stat_count(attribute="mc", subject="me", start=dt(y=2018, m=1), period="m",)
            == 2
        )

        assert (
            stat_count(attribute="mc", subject="me", start=dt(y=2000), period="y") == 0
        )
        assert (
            stat_count(
                attribute="mc", subject="me", start=dt(y=2011, m=11), period="m",
            )
            == 0
        )
        assert (
            stat_count(attribute="mc", subject="me", start=dt(y=2018, m=5), period="m",)
            == 0
        )

        assert (
            stat_count(attribute="mc", subject="me", start=dt(y=2020, m=2), period="m",)
            == 6
        )
        assert (
            stat_count(attribute="mc", subject="me", start=dt(y=2020, m=3), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="mc", subject="me", start=dt(y=2020, m=4), period="m",)
            == 2
        )
        assert (
            stat_count(attribute="mc", subject="me", start=dt(y=2020, m=5), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="mc", subject="me", start=dt(y=2020, m=6), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="mc", subject="me", start=dt(y=2020, m=8), period="m",)
            == 1
        )

        assert (
            stat_count(
                attribute="mc", subject="me", start=dt(y=2020, m=2, d=13), period="d",
            )
            == 1
        )
        assert (
            stat_count(
                attribute="mc",
                subject="me",
                start=dt(y=2020, m=2, d=13, h=6),
                period="h",
            )
            == 1
        )
        assert (
            stat_count(
                attribute="mc",
                subject="me",
                start=dt(y=2020, m=2, d=13, h=18),
                period="h",
            )
            == 0
        )

    def test_total_number_of_words_sent(self, stat_count):
        assert stat_count(attribute="wc", subject="me",) == 71
        assert (
            stat_count(attribute="wc", subject="me", start=dt(y=2000), period="y") == 0
        )
        assert (
            stat_count(attribute="wc", subject="me", start=dt(y=2014), period="y") == 18
        )
        assert (
            stat_count(attribute="wc", subject="me", start=dt(y=2018), period="y") == 31
        )
        assert (
            stat_count(attribute="wc", subject="me", start=dt(y=2020), period="y") == 22
        )

        assert (
            stat_count(attribute="wc", subject="me", start=dt(y=2014, m=9), period="m",)
            == 6
        )
        assert (
            stat_count(
                attribute="wc", subject="me", start=dt(y=2014, m=11), period="m",
            )
            == 11
        )
        assert (
            stat_count(
                attribute="wc", subject="me", start=dt(y=2014, m=12), period="m",
            )
            == 1
        )

        assert (
            stat_count(attribute="wc", subject="me", start=dt(y=2018, m=1), period="m",)
            == 31
        )
        assert (
            stat_count(attribute="wc", subject="me", start=dt(y=2018, m=2), period="m",)
            == 0
        )

        assert (
            stat_count(attribute="wc", subject="me", start=dt(y=2020, m=2), period="m",)
            == 16
        )
        assert (
            stat_count(attribute="wc", subject="me", start=dt(y=2020, m=3), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="wc", subject="me", start=dt(y=2020, m=4), period="m",)
            == 4
        )
        assert (
            stat_count(attribute="wc", subject="me", start=dt(y=2020, m=5), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="wc", subject="me", start=dt(y=2020, m=6), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="wc", subject="me", start=dt(y=2020, m=8), period="m",)
            == 2
        )

        assert (
            stat_count(
                attribute="wc", subject="me", start=dt(y=2020, m=2, d=13), period="d",
            )
            == 5
        )
        assert (
            stat_count(
                attribute="wc",
                subject="me",
                start=dt(y=2020, m=2, d=13, h=6),
                period="h",
            )
            == 5
        )
        assert (
            stat_count(
                attribute="wc",
                subject="me",
                start=dt(y=2020, m=2, d=13, h=7),
                period="h",
            )
            == 0
        )

    def test_total_number_of_characters_sent(self, stat_count):
        assert stat_count(attribute="cc", subject="me",) == 321

        assert (
            stat_count(attribute="cc", subject="me", start=dt(y=2000), period="y") == 0
        )
        assert (
            stat_count(attribute="cc", subject="me", start=dt(y=2014), period="y") == 70
        )
        assert (
            stat_count(attribute="cc", subject="me", start=dt(y=2018), period="y")
            == 167
        )
        assert (
            stat_count(attribute="cc", subject="me", start=dt(y=2020), period="y") == 84
        )

        assert (
            stat_count(attribute="cc", subject="me", start=dt(y=2014, m=9), period="m",)
            == 24
        )
        assert (
            stat_count(
                attribute="cc", subject="me", start=dt(y=2014, m=11), period="m",
            )
            == 43
        )
        assert (
            stat_count(
                attribute="cc", subject="me", start=dt(y=2014, m=12), period="m",
            )
            == 3
        )

        assert (
            stat_count(attribute="cc", subject="me", start=dt(y=2018, m=1), period="m",)
            == 167
        )
        assert (
            stat_count(attribute="cc", subject="me", start=dt(y=2018, m=2), period="m",)
            == 0
        )

        assert (
            stat_count(attribute="cc", subject="me", start=dt(y=2020, m=2), period="m",)
            == 62
        )
        assert (
            stat_count(attribute="cc", subject="me", start=dt(y=2020, m=3), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="cc", subject="me", start=dt(y=2020, m=4), period="m",)
            == 17
        )
        assert (
            stat_count(attribute="cc", subject="me", start=dt(y=2020, m=5), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="cc", subject="me", start=dt(y=2020, m=6), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="cc", subject="me", start=dt(y=2020, m=8), period="m",)
            == 5
        )

        assert (
            stat_count(
                attribute="cc",
                subject="me",
                start=dt(y=2020, m=2, d=13, h=6),
                period="d",
            )
            == 21
        )
        assert (
            stat_count(
                attribute="cc",
                subject="me",
                start=dt(y=2020, m=2, d=13, h=7),
                period="d",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="cc",
                subject="me",
                start=dt(y=2020, m=2, d=13, h=6),
                period="h",
            )
            == 21
        )
        assert (
            stat_count(
                attribute="cc",
                subject="me",
                start=dt(y=2020, m=2, d=13, h=7),
                period="h",
            )
            == 0
        )

    def test_total_number_of_messages_received(self, stat_count):
        assert stat_count(attribute="mc", subject="partner",) == 13
        assert (
            stat_count(attribute="mc", subject="partner", start=dt(y=2000), period="y",)
            == 0
        )
        assert (
            stat_count(attribute="mc", subject="partner", start=dt(y=2014), period="y",)
            == 6
        )
        assert (
            stat_count(attribute="mc", subject="partner", start=dt(y=2018), period="y",)
            == 1
        )
        assert (
            stat_count(attribute="mc", subject="partner", start=dt(y=2020), period="y",)
            == 6
        )

        assert (
            stat_count(
                attribute="mc", subject="partner", start=dt(y=2011, m=11), period="m",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="mc", subject="partner", start=dt(y=2014, m=9), period="m",
            )
            == 0
        )
        assert (
            stat_count(
                attribute="mc", subject="partner", start=dt(y=2014, m=11), period="m",
            )
            == 5
        )
        assert (
            stat_count(
                attribute="mc", subject="partner", start=dt(y=2014, m=12), period="m",
            )
            == 1
        )

        assert (
            stat_count(
                attribute="mc", subject="partner", start=dt(y=2018, m=1), period="m",
            )
            == 1
        )
        assert (
            stat_count(
                attribute="mc", subject="partner", start=dt(y=2018, m=5), period="m",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="mc", subject="partner", start=dt(y=2020, m=2), period="m",
            )
            == 4
        )
        assert (
            stat_count(
                attribute="mc", subject="partner", start=dt(y=2020, m=3), period="m",
            )
            == 1
        )
        assert (
            stat_count(
                attribute="mc", subject="partner", start=dt(y=2020, m=4), period="m",
            )
            == 0
        )
        assert (
            stat_count(
                attribute="mc", subject="partner", start=dt(y=2020, m=5), period="m",
            )
            == 1
        )
        assert (
            stat_count(
                attribute="mc", subject="partner", start=dt(y=2020, m=8), period="m",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="mc",
                subject="partner",
                start=dt(y=2020, m=2, d=13),
                period="d",
            )
            == 1
        )
        assert (
            stat_count(
                attribute="mc",
                subject="partner",
                start=dt(y=2020, m=2, d=14),
                period="d",
            )
            == 2
        )
        assert (
            stat_count(
                attribute="mc",
                subject="partner",
                start=dt(y=2020, m=2, d=18),
                period="d",
            )
            == 1
        )

    def test_total_number_of_words_received(self, stat_count):
        assert stat_count(attribute="wc", subject="partner",) == 20

        assert (
            stat_count(attribute="wc", subject="partner", start=dt(y=2000), period="y",)
            == 0
        )
        assert (
            stat_count(attribute="wc", subject="partner", start=dt(y=2014), period="y",)
            == 7
        )
        assert (
            stat_count(attribute="wc", subject="partner", start=dt(y=2018), period="y",)
            == 1
        )
        assert (
            stat_count(attribute="wc", subject="partner", start=dt(y=2020), period="y",)
            == 12
        )

        assert (
            stat_count(
                attribute="wc", subject="partner", start=dt(y=2014, m=9), period="m",
            )
            == 0
        )
        assert (
            stat_count(
                attribute="wc", subject="partner", start=dt(y=2014, m=11), period="m",
            )
            == 7
        )
        assert (
            stat_count(
                attribute="wc", subject="partner", start=dt(y=2014, m=12), period="m",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="wc", subject="partner", start=dt(y=2018, m=1), period="m",
            )
            == 1
        )
        assert (
            stat_count(
                attribute="wc", subject="partner", start=dt(y=2018, m=2), period="m",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="wc", subject="partner", start=dt(y=2020, m=2), period="m",
            )
            == 11
        )
        assert (
            stat_count(
                attribute="wc", subject="partner", start=dt(y=2020, m=3), period="m",
            )
            == 0
        )
        assert (
            stat_count(
                attribute="wc", subject="partner", start=dt(y=2020, m=5), period="m",
            )
            == 1
        )

        assert (
            stat_count(
                attribute="wc",
                subject="partner",
                start=dt(y=2020, m=2, d=13),
                period="d",
            )
            == 9
        )
        assert (
            stat_count(
                attribute="wc",
                subject="partner",
                start=dt(y=2020, m=2, d=14),
                period="d",
            )
            == 2
        )
        assert (
            stat_count(
                attribute="wc",
                subject="partner",
                start=dt(y=2020, m=2, d=18),
                period="d",
            )
            == 0
        )

    def test_total_number_of_characters_received(self, stat_count):
        assert stat_count(attribute="cc", subject="partner",) == 88

        assert (
            stat_count(attribute="cc", subject="partner", start=dt(y=2000), period="y",)
            == 0
        )
        assert (
            stat_count(attribute="cc", subject="partner", start=dt(y=2014), period="y",)
            == 29
        )
        assert (
            stat_count(attribute="cc", subject="partner", start=dt(y=2018), period="y",)
            == 3
        )
        assert (
            stat_count(attribute="cc", subject="partner", start=dt(y=2020), period="y",)
            == 56
        )

        assert (
            stat_count(
                attribute="cc", subject="partner", start=dt(y=2014, m=9), period="m",
            )
            == 0
        )
        assert (
            stat_count(
                attribute="cc", subject="partner", start=dt(y=2014, m=11), period="m",
            )
            == 29
        )
        assert (
            stat_count(
                attribute="cc", subject="partner", start=dt(y=2014, m=12), period="m",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="cc", subject="partner", start=dt(y=2018, m=1), period="m",
            )
            == 3
        )
        assert (
            stat_count(
                attribute="cc", subject="partner", start=dt(y=2018, m=2), period="m",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="cc", subject="partner", start=dt(y=2020, m=2), period="m",
            )
            == 52
        )
        assert (
            stat_count(
                attribute="cc", subject="partner", start=dt(y=2020, m=3), period="m",
            )
            == 0
        )
        assert (
            stat_count(
                attribute="cc", subject="partner", start=dt(y=2020, m=5), period="m",
            )
            == 4
        )

        assert (
            stat_count(
                attribute="cc",
                subject="partner",
                start=dt(y=2020, m=2, d=13),
                period="d",
            )
            == 30
        )
        assert (
            stat_count(
                attribute="cc",
                subject="partner",
                start=dt(y=2020, m=2, d=14),
                period="d",
            )
            == 22
        )
        assert (
            stat_count(
                attribute="cc",
                subject="partner",
                start=dt(y=2020, m=2, d=18),
                period="d",
            )
            == 0
        )
