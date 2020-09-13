import pytest
from datetime import datetime
import numpy as np
import pandas as pd

from miner.message.messaging_analyzer import MessagingAnalyzerManager
from miner.message.conversations import Conversations
from miner.message.conversation_stats import ConversationStats
from miner import utils


@pytest.fixture
def priv_stats(priv_msg_analyzer):
    return priv_msg_analyzer.stats


@pytest.fixture(scope="module")
def group_stats(group_msg_analyzer):
    return group_msg_analyzer.stats


class TestConversationStatsForGroups:
    def test_general_stats_again(self, group_stats):
        assert isinstance(group_stats, ConversationStats)

        assert group_stats.mc == 18
        assert group_stats.media_mc == 2
        assert group_stats.wc == 40
        assert group_stats.cc == 166
        assert "marathon" in list(group_stats.channels)
        assert isinstance(group_stats.start, datetime)

    def test_filter_channel(self, group_stats):
        filtered = group_stats.filter(channel="marathon")
        assert filtered.number_of_channels == 1
        assert filtered.contributors == ["Levente Csőke", "Foo Bar", "Donald Duck"]
        assert filtered.created_by_me is True
        assert filtered.most_used_words.index[0] in ("yapp", ":d")
        assert filtered.mc == 9

    def test_filter_sender(self, group_stats):
        filtered = group_stats.filter(sender="Teflon Musk")
        assert filtered.contributors == ["Teflon Musk"]
        assert filtered.wc == 3
        assert filtered.cc == 18
        assert filtered.df.shape == (1, 6,)

    def test_filter_me(self, group_stats):
        filtered = group_stats.filter(subject="me")
        # NOTE filters out the one group where I'm not a contributor, only a participant
        assert filtered.number_of_channels == 2
        assert filtered.df.shape == (4, 6)
        assert filtered.text_mc == 4
        assert filtered.percentage_of_media_messages == 0

    def test_filter_partner(self, group_stats):
        filtered = group_stats.filter(subject="partner")
        assert filtered.number_of_channels == 3
        assert filtered.df.shape == (14, 6)
        assert filtered.text_mc == 12
        assert filtered.percentage_of_media_messages == pytest.approx(14.28, 0.1)
        assert len(filtered.contributors) == 7

    def test_filter_subject_by_name(self, group_stats):
        filtered = group_stats.filter(subject="Teflon Musk")
        assert filtered.number_of_channels == 1
        assert filtered.df.shape == (1, 6)
        assert filtered.text_mc == 1
        assert filtered.percentage_of_media_messages == 0
        assert len(filtered.contributors) == 1

    def test_filter_date(self, group_stats):
        filtered = group_stats.filter(start=utils.dt(y=2018), period="y")
        assert filtered.channels == ["marathon"]
        assert filtered.start.year == 2018
        assert filtered.start.month == 4

    def test_number_of_channels_in_stats(self, group_stats):
        assert group_stats.number_of_channels == 3

    def test_contributors(self, group_stats):
        contributors = group_stats.contributors
        assert "Foo Bar" in contributors
        assert "Facebook User" in contributors  # TODO??

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
        assert msg_lang["test"].language.code == "en"
        assert msg_lang["marathon?"].language.code == "hu"
        assert msg_lang["blabla"].reliable == False

    def test_reacted_messages(self, group_stats):
        reacted_messages = group_stats.reacted_messages
        assert len(reacted_messages) == 0

    def test_get_grouped_time_series_data(self, group_stats):
        time_series = group_stats.get_grouped_time_series_data(period="y")

        assert isinstance(time_series, pd.DataFrame)
        assert time_series.shape == (2, 5,)
        assert time_series.index.date[0].year == 2011
        assert time_series.index.date[0].month == 1
        assert time_series.index.date[0].day == 1
        assert time_series.index.date[1].year == 2018
        assert time_series.index.date[1].month == 1
        assert time_series.index.date[1].day == 1

    def test_stat_per_period(self, group_stats):
        stats_per_period = group_stats.stat_per_period(period="y")
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
        stats_per_period = group_stats.stat_per_period(period="m")
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
    def test_general_stats_again(self, priv_stats):
        assert isinstance(priv_stats, ConversationStats)

        assert priv_stats.mc == 31
        assert priv_stats.media_mc == 9
        assert priv_stats.wc == 91
        assert "Teflon Musk" in list(priv_stats.channels)
        assert isinstance(priv_stats.start, datetime)

    def test_filter_channels(self, priv_stats):
        filtered = priv_stats.filter(channel="Foo Bar")
        assert filtered.channels == ["Foo Bar"]
        assert filtered.created_by_me is True
        assert filtered.cc == 140
        assert filtered.df.shape == (15, 10)

    def test_filter_senders(self, priv_stats):
        filtered = priv_stats.filter(sender="Foo Bar")
        assert filtered.channels == ["Foo Bar"]
        assert not filtered.created_by_me
        assert filtered.cc == 56
        assert filtered.df.shape == (6, 10)

    def test_filter_subject(self):
        # TODO should be the same as filter for sender
        pass

    def test_stats_are_in_df(self, priv_msg_analyzer):
        stats_df = priv_msg_analyzer.filter(
            senders="Teflon Musk"
        ).stats._get_convos_in_numbers()

        assert "mc" in stats_df
        assert "text_mc" in stats_df
        assert "media_mc" in stats_df
        assert "wc" in stats_df
        assert "cc" in stats_df

    def test_stats_index_can_be_grouped(self, priv_msg_analyzer):
        stats = priv_msg_analyzer.filter(senders="Teflon Musk").stats
        assert stats.df.index[0].year == 2014
        assert stats.df.index[0].month == 9
        assert stats.df.index[0].day == 24
        assert stats.df.index[0].hour == 17

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
        txt = "yo Legyen az, hogy most megprobalok ekezet nelkul irni. Seems pretty easy. I need some english words in here. Right? A magyar szavak felismereset probalom tesztelni ezzekkel a mondatokkal."
        msg_lang = priv_stats.message_language_map
        assert msg_lang["are you the real teflon musk?"].language.code == "en"
        assert msg_lang["Excepteur...laborum. :D"].language.code == "la"

        assert msg_lang[txt].reliable == True
        assert msg_lang[txt].language.code == "en"
        assert msg_lang[txt].languages[0].code == "en"
        assert msg_lang[txt].languages[1].code == "hu"

    def test_reacted_messages(self, priv_stats):
        reacted_messages = priv_stats.reacted_messages
        assert len(reacted_messages) == 3
        assert sum(reacted_messages.content.notna()) == 1
        assert sum(reacted_messages.gifs.notna()) == 2

        assert reacted_messages.reactions[0][0].get("reaction") == "❤"

    def test_get_grouped_time_series_data(self, priv_msg_analyzer):
        grouped = priv_msg_analyzer.stats.get_grouped_time_series_data(period="y")
        assert len(grouped) == 3
        third_row = grouped.iloc[2]
        assert third_row.mc == 15
        assert third_row.media_mc == 7
        assert third_row.wc == 34
        assert third_row.cc == 140

        grouped = priv_msg_analyzer.stats.get_grouped_time_series_data(period="m")
        assert len(grouped) == 9

        grouped = priv_msg_analyzer.stats.get_grouped_time_series_data(period="d")
        assert len(grouped) == 16

        grouped = priv_msg_analyzer.stats.get_grouped_time_series_data(period="h")
        assert len(grouped) == 24

    def test_get_grouped_time_series_data_foo_bar(self, priv_msg_analyzer):
        stats = priv_msg_analyzer.filter(senders="Foo Bar").stats
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

    def test_stats_per_period(self, priv_msg_analyzer):
        yearly = priv_msg_analyzer.stats.stat_per_period("y", "mc")
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

        monthly = priv_msg_analyzer.stats.stat_per_period("m", "mc")
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

        daily = priv_msg_analyzer.stats.stat_per_period("d", "mc")
        assert daily == {
            "monday": 6,
            "tuesday": 2,
            "wednesday": 6,
            "thursday": 3,
            "friday": 6,
            "saturday": 3,
            "sunday": 5,
        }

        hourly = priv_msg_analyzer.stats.stat_per_period("h", "mc")
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

    def test_stats_per_period_foo_bar(self, priv_msg_analyzer):
        stats = priv_msg_analyzer.filter(senders="Foo Bar").stats
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
