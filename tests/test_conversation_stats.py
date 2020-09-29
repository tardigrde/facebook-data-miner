from datetime import datetime

import pandas as pd
import pytest

from miner.message.conversation_stats import ConversationStats
from miner.utils import utils


class TestConversationStatsForGroups:
    def test_general_properties(self, group_stats):
        assert isinstance(group_stats, ConversationStats)
        assert repr(group_stats) == "ConversationStats for 3 channels"
        assert isinstance(group_stats.messages, pd.DataFrame)
        assert group_stats.messages.shape == (18, 6,)
        assert group_stats.number_of_channels == 3

    def test_some_stats(self, group_stats):
        assert group_stats.mc == 18
        assert group_stats.media_mc == 2
        assert group_stats.wc == 40
        assert group_stats.cc == 166
        assert "marathon" in list(group_stats.channels)

    def test_too_many_channels(self, group_stats, caplog):
        assert group_stats.creator == ""
        assert caplog.messages[0] == "Too many `channels` to calculate this."

    def test_start_end(self, group_stats):
        assert isinstance(group_stats.start, datetime)
        assert isinstance(group_stats.end, datetime)

    def test_filter_channels(self, group_stats):
        filtered = group_stats.filter(channels="marathon")
        assert filtered.number_of_channels == 1
        assert filtered.contributors == [
            "Jenő Rejtő",
            "Foo Bar",
            "Donald Duck",
        ]
        assert filtered.created_by_me is True
        assert filtered.most_used_words.iloc[0]["unique_values"] in (
            "yapp",
            ":d",
        )
        assert filtered.most_used_words.iloc[0]["counts"] == 2
        assert filtered.mc == 9

    def test_filter_senders(self, group_stats):
        filtered = group_stats.filter(senders="Bugs Bunny")
        assert filtered.contributors == ["Bugs Bunny"]
        assert filtered.wc == 3
        assert filtered.cc == 18
        assert filtered.df.shape == (1, 4,)

    def test_filter_me(self, group_stats):
        filtered = group_stats.filter(senders="me")
        # NOTE filters out the one group where I'm not a contributor,
        # only a participant
        assert filtered.number_of_channels == 2
        assert filtered.df.shape == (4, 4)
        assert filtered.text_mc == 4
        assert filtered.percentage_of_media_messages == 0

    def test_filter_partner(self, group_stats):
        filtered = group_stats.filter(senders="partner")
        assert filtered.number_of_channels == 3
        assert filtered.df.shape == (14, 6)
        assert filtered.text_mc == 12
        assert filtered.percentage_of_media_messages == pytest.approx(
            14.28, 0.1
        )
        assert len(filtered.contributors) == 7

    def test_filter_subject_by_name(self, group_stats):
        filtered = group_stats.filter(senders="Bugs Bunny")
        assert filtered.number_of_channels == 1
        assert filtered.df.shape == (1, 4)
        assert filtered.text_mc == 1
        assert filtered.percentage_of_media_messages == 0
        assert len(filtered.contributors) == 1

    def test_filter_date(self, group_stats):
        filtered = group_stats.filter(start=utils.dt(y=2018), period="y")
        assert filtered.channels == ["marathon"]
        assert filtered.start.year == 2018
        assert filtered.start.month == 4

    def test_contributors(self, group_stats):
        contributors = group_stats.contributors
        assert "Foo Bar" in contributors
        assert "Facebook User" in contributors
        assert group_stats.number_of_contributors == 8

    def test_average_word_length(self, group_stats):
        avg = group_stats.average_word_length
        assert avg == pytest.approx(4.15, 0.01)

    def test_wc_in_messages(self, group_stats):
        wcs = group_stats.wc_in_messages
        assert max(wcs) == 7
        assert min(wcs) == 1
        assert sum(wcs) / len(wcs) == pytest.approx(2.5, 0.01)

    def test_cc_in_messages(self, group_stats):
        ccs = group_stats.cc_in_messages
        assert max(ccs) == 31
        assert min(ccs) == 2
        assert sum(ccs) / len(ccs) == pytest.approx(11.875, 0.01)

    def test_message_language_map(self, group_stats):
        msg_lang = group_stats.message_language_map
        assert msg_lang["test"].get("lang") == "English"
        assert msg_lang["marathon?"].get("lang") == "Hungarian"

    def test_reacted_messages(self, group_stats):
        reacted_messages = group_stats.reacted_messages
        assert len(reacted_messages) == 0

    def test_get_grouped_time_series_data(self, group_stats):
        time_series = group_stats.get_grouped_time_series_data(timeframe="y")

        assert isinstance(time_series, pd.DataFrame)
        assert time_series.shape == (2, 5,)
        assert time_series.index.date[0].year == 2011
        assert time_series.index.date[0].month == 1
        assert time_series.index.date[0].day == 1
        assert time_series.index.date[1].year == 2018
        assert time_series.index.date[1].month == 1
        assert time_series.index.date[1].day == 1

    def test_stat_per_period(self, group_stats):
        stats_per_period = group_stats.stats_per_timeframe(timeframe="y")
        assert stats_per_period == {
            2009: 0,
            2010: 0,
            2011: 9,
            2012: 0,
            2013: 0,
            2014: 0,
            2015: 0,
            2016: 0,
            2017: 0,
            2018: 9,
            2019: 0,
            2020: 0,
        }
        stats_per_period = group_stats.stats_per_timeframe(timeframe="m")
        assert stats_per_period == {
            "january": 0,
            "february": 0,
            "march": 0,
            "april": 9,
            "may": 0,
            "june": 0,
            "july": 9,
            "august": 0,
            "september": 0,
            "october": 0,
            "november": 0,
            "december": 0,
        }


class TestConversationStatsForPrivate:
    def test_some_stats(self, priv_stats):
        assert isinstance(priv_stats, ConversationStats)

        assert priv_stats.mc == 31
        assert priv_stats.media_mc == 9
        assert priv_stats.wc == 91
        assert "Bugs Bunny" in list(priv_stats.channels)
        assert isinstance(priv_stats.start, datetime)
        assert priv_stats.percentage_of_reacted_messages == pytest.approx(
            9.67, 0.01
        )

    def test_media(self, priv_stats):
        assert isinstance(priv_stats.media, pd.DataFrame)
        assert len(priv_stats.files) == 2
        assert len(priv_stats.photos) == 3
        assert len(priv_stats.videos) == 1
        assert len(priv_stats.audios) == 1
        assert len(priv_stats.gifs) == 2

    def test_filter_channels(self, priv_stats):
        filtered = priv_stats.filter(channels="Foo Bar")
        assert filtered.channels == ["Foo Bar"]
        assert filtered.created_by_me is True
        assert filtered.cc == 140
        assert filtered.df.shape == (15, 10)

    def test_filter_senders(self, priv_stats):
        filtered = priv_stats.filter(senders="Foo Bar")
        assert filtered.channels == ["Foo Bar"]
        assert not filtered.created_by_me
        assert filtered.cc == 56
        assert filtered.df.shape == (6, 8)

    def test_stats_are_in_df(self, panalyzer):
        stats_df = panalyzer.filter(
            participants="Bugs Bunny"
        )._stats._get_convos_in_numbers()

        assert "mc" in stats_df
        assert "text_mc" in stats_df
        assert "media_mc" in stats_df
        assert "wc" in stats_df
        assert "cc" in stats_df

    def test_stats_index_can_be_grouped(self, panalyzer):
        stats = panalyzer.filter(participants="Bugs Bunny")._stats
        assert stats.df.index[0].year == 2014
        assert stats.df.index[0].month == 9
        assert stats.df.index[0].day == 24
        assert stats.df.index[0].hour == 15

    def test_properties(self, priv_stats):
        percentage_of_media_msgs = priv_stats.percentage_of_media_messages
        assert percentage_of_media_msgs == pytest.approx(29.03, 0.1)

    def test_average_word_length(self, priv_stats):
        avg = priv_stats.average_word_length
        assert avg == pytest.approx(4.49, 0.01)

    def test_wc_in_messages(self, priv_stats):
        wcs = priv_stats.wc_in_messages
        assert max(wcs) == 29
        assert min(wcs) == 1
        assert sum(wcs) / len(wcs) == pytest.approx(4.13, 0.01)

    def test_cc_in_messages(self, priv_stats):
        ccs = priv_stats.cc_in_messages
        assert max(ccs) == 188
        assert min(ccs) == 2
        assert sum(ccs) / len(ccs) == pytest.approx(21.72, 0.01)

    def test_message_language_map(self, priv_stats):
        txt = (
            "yo Legyen az, hogy most megprobalok ekezet nelkul irni. "
            "Seems pretty easy. "
            "I need some english words in here. Right? "
            "A magyar szavak felismereset probalom tesztelni "
            "ezzekkel a mondatokkal."
        )
        msg_lang = priv_stats.message_language_map
        assert (
            msg_lang["are you the real Bugs Bunny?"].get("lang") == "English"
        )
        assert msg_lang["Excepteur...laborum. :D"].get("lang") == "Latin"

        assert msg_lang[txt].get("lang") == "English"

    def test_reacted_messages(self, priv_stats):
        reacted_messages = priv_stats.reacted_messages
        assert len(reacted_messages) == 3
        assert sum(reacted_messages.content.notna()) == 1
        assert sum(reacted_messages.gifs.notna()) == 2

        assert reacted_messages.reactions[0][0].get("reaction") == "❤"

    def test_get_grouped_time_series_data(self, panalyzer):
        grouped = panalyzer._stats.get_grouped_time_series_data(timeframe="y")
        assert len(grouped) == 3
        third_row = grouped.iloc[2]
        assert third_row.mc == 15
        assert third_row.media_mc == 7
        assert third_row.wc == 34
        assert third_row.cc == 140

        grouped = panalyzer._stats.get_grouped_time_series_data(timeframe="m")
        assert len(grouped) == 9

        grouped = panalyzer._stats.get_grouped_time_series_data(timeframe="d")
        assert len(grouped) == 17

        grouped = panalyzer._stats.get_grouped_time_series_data(timeframe="h")
        assert len(grouped) == 24

    def test_get_grouped_time_series_data_foo_bar(self, panalyzer):
        stats = panalyzer.filter(participants="Foo Bar")._stats
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
        assert len(grouped) == 10

        grouped = stats.get_grouped_time_series_data("h")
        assert len(grouped) == 14

    def test_stats_per_period(self, panalyzer):
        yearly = panalyzer._stats.stats_per_timeframe("y", "mc")
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

        monthly = panalyzer._stats.stats_per_timeframe("m", "mc")
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

        daily = panalyzer._stats.stats_per_timeframe("d", "mc")
        assert daily == {
            "monday": 7,
            "tuesday": 1,
            "wednesday": 6,
            "thursday": 3,
            "friday": 6,
            "saturday": 3,
            "sunday": 5,
        }

        hourly = panalyzer._stats.stats_per_timeframe("h", "mc")
        assert hourly == {
            0: 1,
            1: 1,
            2: 0,
            3: 1,
            4: 0,
            5: 2,
            6: 0,
            7: 1,
            8: 1,
            9: 0,
            10: 2,
            11: 6,
            12: 1,
            13: 0,
            14: 1,
            15: 2,
            16: 0,
            17: 1,
            18: 3,
            19: 2,
            20: 0,
            21: 3,
            22: 2,
            23: 1,
        }

    def test_stats_per_period_ifiltered_for_foo_bar(self, panalyzer):
        stats = panalyzer.filter(participants="Foo Bar")._stats
        yearly = stats.stats_per_timeframe("y", "mc")
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

        monthly = stats.stats_per_timeframe("m", "mc")
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

        daily = stats.stats_per_timeframe("d", "mc")
        assert daily == {
            "monday": 2,
            "tuesday": 1,
            "wednesday": 1,
            "thursday": 3,
            "friday": 5,
            "saturday": 2,
            "sunday": 1,
        }
        hourly = stats.stats_per_timeframe("h", "mc")
        assert hourly == {
            0: 1,
            1: 0,
            2: 0,
            3: 1,
            4: 0,
            5: 2,
            6: 0,
            7: 1,
            8: 0,
            9: 0,
            10: 2,
            11: 1,
            12: 1,
            13: 0,
            14: 1,
            15: 0,
            16: 0,
            17: 1,
            18: 2,
            19: 0,
            20: 0,
            21: 1,
            22: 0,
            23: 1,
        }
