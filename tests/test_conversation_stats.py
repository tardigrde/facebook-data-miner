import pytest


def test_stats_are_in_df(analyzer):
    stats_df = analyzer.get_stats(names="Teflon Musk").get_conversation_statistics()

    assert "mc" in stats_df
    assert "text_mc" in stats_df
    assert "media_mc" in stats_df
    assert "wc" in stats_df
    assert "cc" in stats_df


def test_stats_index_can_be_grouped(analyzer):
    stats = analyzer.get_stats(names="Teflon Musk")
    assert stats.df.index[0].year == 2014
    assert stats.df.index[0].month == 9
    assert stats.df.index[0].day == 24
    assert stats.df.index[0].hour == 17


def test_get_time_series_data(analyzer):
    stats = analyzer.get_stats(names="Foo Bar")
    grouped = stats.get_grouped_time_series_data("y")
    assert len(grouped) == 1
    first_row = grouped.iloc[0]
    assert first_row.mc == 15
    assert first_row.media_mc == 7
    assert first_row.wc == 34
    assert first_row.cc == 140

    grouped = stats.get_grouped_time_series_data("m")
    assert len(grouped) == 5

    grouped = stats.get_grouped_time_series_data("d")
    assert len(grouped) == 9

    grouped = stats.get_grouped_time_series_data("h")
    assert len(grouped) == 14


def test_stats_per_period(analyzer):
    stats = analyzer.get_stats(names="Foo Bar")
    yearly = stats.stat_per_period("y", "mc")
    assert yearly == {
        2009: 0,
        2010: 0,
        2011: 0,
        2012: 0,
        2013: 0,
        2014: 0,
        2015: 0,
        2016: 0,
        2017: 0,
        2018: 0,
        2019: 0,
        2020: 15,
    }

    monthly = stats.stat_per_period("m", "mc")
    assert monthly == {
        "january": 0,
        "february": 10,
        "march": 1,
        "april": 2,
        "may": 1,
        "june": 0,
        "july": 0,
        "august": 1,
        "september": 0,
        "october": 0,
        "november": 0,
        "december": 0,
    }

    daily = stats.stat_per_period("d", "mc")
    assert daily == {
        "monday": 1,
        "tuesday": 2,
        "wednesday": 1,
        "thursday": 3,
        "friday": 5,
        "saturday": 2,
        "sunday": 1,
    }
    hourly = stats.stat_per_period("h", "mc")
    assert hourly == {
        0: 1,
        1: 1,
        2: 0,
        3: 0,
        4: 1,
        5: 0,
        6: 2,
        7: 0,
        8: 1,
        9: 0,
        10: 0,
        11: 1,
        12: 2,
        13: 1,
        14: 0,
        15: 1,
        16: 0,
        17: 0,
        18: 1,
        19: 0,
        20: 2,
        21: 0,
        22: 0,
        23: 1,
    }


def test_ranking(analyzer):
    ranking = analyzer.priv_stats.get_ranking_of_partners_by_messages()
    assert ranking == {
        "Foo Bar": 15,
        "Tőke Hal": 7,
        "Teflon Musk": 6,
        "Benedek Elek": 3,
    }


def test_properties(analyzer):
    stats = analyzer.priv_stats
    percentage_of_media_msgs = stats.percentage_of_media_messages
    print()
    assert percentage_of_media_msgs == pytest.approx(29.03, 0.1)
