import pytest
import pandas as pd
from miner.utils import dt

from miner.message.conversation_analyzer import (
    MessagingAnalyzerManager,
    GroupMessagingAnalyzer,
)
from miner.message.conversations import Conversations
from miner.message.conversation_stats import (
    ConversationStats,
    PrivateConversationStats,
    GroupConversationStats,
)


@pytest.fixture(scope="session")
def stat_count(priv_msg_analyzer):
    return priv_msg_analyzer.get_stat_count


class TestGroupMessagingAnalyzerMethods:
    def test_analyzer_groups(self, group_msg_analyzer):
        groups = group_msg_analyzer.data
        assert len(groups) == 3

    def test_filter(self, group_msg_analyzer):
        filtered = group_msg_analyzer.filter(names=["Teflon Musk"])
        assert isinstance(filtered, GroupMessagingAnalyzer)
        assert len(filtered.data) == 2
        assert len(filtered.group_convo_map.get("Teflon Musk")) == 2

        filtered = group_msg_analyzer.filter(names="Teflon Musk")
        assert len(filtered.data) == 2

    def test_filter_by_groups(self, group_msg_analyzer):
        filtered = group_msg_analyzer.filter(groups=["marathon"])
        assert filtered.data.get("marathon")
        assert len(filtered.data) == 1
        assert len(filtered.group_convo_map) == 4

        filtered = group_msg_analyzer.filter(groups="marathon")
        assert len(filtered.data) == 1

    def test_get_stats_per_conversation(self, group_msg_analyzer):
        stats_per_conversation = group_msg_analyzer.get_stats_per_conversation()

        assert len(stats_per_conversation) == 3
        assert list(group_msg_analyzer.data.keys()) == list(
            stats_per_conversation.keys()
        )
        assert all(
            [
                isinstance(stats, GroupConversationStats)
                for stats in stats_per_conversation.values()
            ]
        )

    def test_get_stats_per_partner(self, group_msg_analyzer):
        stats_per_partner = group_msg_analyzer.get_stats_per_partner()

        assert len(stats_per_partner) == 8
        assert list(group_msg_analyzer.participants) == sorted(
            list(stats_per_partner.keys())
        )
        assert all(
            [
                isinstance(stats, GroupConversationStats)
                for stats in stats_per_partner.values()
            ]
        )

    def test_get_all_groups_for_one_person(self, group_msg_analyzer):
        list_of_groups = group_msg_analyzer.get_all_groups_for_one_person("Teflon Musk")
        assert len(list_of_groups) == 2

    def test_min_group_size(self, group_msg_analyzer):
        minimum = group_msg_analyzer.min_group_size
        assert minimum == 4

    def test_mean_group_size(self, group_msg_analyzer):
        mean = group_msg_analyzer.mean_group_size
        assert mean == pytest.approx(4.66, 0.1)

    def test_max_group_size(self, group_msg_analyzer):
        maximum = group_msg_analyzer.max_group_size
        assert maximum == 6

    def test_number_of_convos_created_by_me(self, group_msg_analyzer):
        created_by_me = group_msg_analyzer.number_of_convos_created_by_me
        assert created_by_me == 2

    def test_get_ranking_of_partners_by_convo_stats(self):
        pass  # TODO

    def test_portion_of_contribution(self, group_msg_analyzer):
        contrib = group_msg_analyzer.portion_of_contribution
        assert isinstance(contrib, dict)
        assert len(contrib)
        assert contrib["Foo Bar"] == pytest.approx(16.66, 0.1)
        assert contrib["Teflon Musk"] == pytest.approx(5.55, 0.1)

        assert group_msg_analyzer.most_contributed == (
            "Donald Duck",
            pytest.approx(33.33, 0.1),
        )

        least_contrib = group_msg_analyzer.least_contributed
        assert least_contrib[0] in (
            "Tőke Hal",
            "John Doe",
            "Teflon Musk",
            "Facebook User",
            "Dér Dénes",
        )
        assert least_contrib[1] == pytest.approx(5.55, 0.1)


class TestPrivateMessagingAnalyzerMethods:
    def test_stats_per_partner(self):
        pass  # TODO


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
