import pytest

from miner.message.messaging_analyzer import MessagingAnalyzerManager, MessagingAnalyzer
from miner.message.conversation_stats import ConversationStats

from miner.utils.utils import dt


@pytest.fixture(scope="session")
def stat_count(priv_msg_analyzer):
    return priv_msg_analyzer.get_stat_count


class TestMessagingAnalyzerManager:
    def test_private_and_group(self, analyzer):
        isinstance(analyzer, MessagingAnalyzerManager)
        isinstance(analyzer.private, MessagingAnalyzer)
        isinstance(analyzer.group, MessagingAnalyzer)

    def test_people_i_have_private_and_group__convo_with(self, analyzer):
        assert len(analyzer.people_i_have_private_convo_with) == 4
        assert len(analyzer.people_i_have_group_convo_with) == 8

    def test_get_who_i_have_private_convo_with_from_a_group(self, analyzer):
        have = analyzer.get_who_i_have_private_convo_with_from_a_group("marathon")
        assert have == ["Foo Bar", "Teflon Musk"]

    def test_how_much_i_speak_in_private_with_group_members(self, analyzer):
        spoke = analyzer.how_much_i_speak_in_private_with_group_members("marathon")
        assert spoke == {"Foo Bar": 15, "Teflon Musk": 6}

    def test_all_interactions(self, analyzer):
        private, group = analyzer.all_interactions("Teflon Musk")
        assert private._stats.channels == ["Teflon Musk"]
        assert group._stats.channels == [
            "Foo Bar, John Doe and Teflon Musk",
            "marathon",
        ]

    def test_is_priv_msg_first_then_group(self, analyzer):
        is_priv = analyzer.is_priv_msg_first_then_group("Teflon Musk")
        assert is_priv is True

        is_priv = analyzer.is_priv_msg_first_then_group("Benedek Elek")
        assert is_priv is True  # only has private

        is_priv = analyzer.is_priv_msg_first_then_group("Foo Bar")
        assert is_priv is True

        is_priv = analyzer.is_priv_msg_first_then_group("Tőke Hal")
        assert is_priv is True

    def test_get_stats_together(self, analyzer):
        stats = analyzer.get_stats_together("Foo Bar")
        assert stats.channels == [
            "Tőke Hal, Foo Bar, Donald Duck and 2 others",
            "Foo Bar, John Doe and Teflon Musk",
            "marathon",
            "Foo Bar",
        ]
        assert stats.contributors == ["Foo Bar"]
        assert stats.df.shape == (9, 8)


class TestMessagingAnalyzerMethodsForGroups:
    def test_analyzer_groups(self, group_msg_analyzer):
        groups = group_msg_analyzer.data
        assert len(groups) == 3

    def test_filter_by_sender(self, group_msg_analyzer):
        filtered = group_msg_analyzer.filter(participants=["Teflon Musk"])
        assert isinstance(filtered, MessagingAnalyzer)
        assert len(filtered.data) == 2
        assert len(filtered.group_convo_map.get("Teflon Musk")) == 2

        filtered = group_msg_analyzer.filter(participants="Teflon Musk")
        assert len(filtered.data) == 2

    def test_filter_by_channels(self, group_msg_analyzer):
        filtered = group_msg_analyzer.filter(channels=["marathon"])
        assert filtered.data.get("marathon")
        assert len(filtered.data) == 1
        assert len(filtered.group_convo_map) == 4

        filtered = group_msg_analyzer.filter(channels="marathon")
        assert len(filtered.data) == 1

    def test_filter_by_channels_and_sender(self, group_msg_analyzer):
        filtered = group_msg_analyzer.filter(
            channels=["marathon"], participants="Teflon Musk"
        )
        assert filtered.data.get("marathon")
        assert len(filtered.data) == 1
        assert len(filtered.group_convo_map) == 4

        filtered = group_msg_analyzer.filter(
            channels=["marathon"], participants="Benedek Elek"
        )

        assert not len(filtered)

        filtered = group_msg_analyzer.filter(channels=["gibberish"])

        assert not len(filtered)

    def test_get_stats_per_channel(self, group_msg_analyzer):
        stats_per_channel = group_msg_analyzer._get_stats_per_channel()

        assert len(stats_per_channel) == 3
        assert list(group_msg_analyzer.data.keys()) == list(stats_per_channel.keys())
        assert all(
            [
                isinstance(stats, ConversationStats)
                for stats in stats_per_channel.values()
            ]
        )

    def test_get_stats_per_sender(self, group_msg_analyzer):
        stats_per_partner = group_msg_analyzer._get_stats_per_participant()

        assert len(stats_per_partner) == 8
        assert list(group_msg_analyzer.participants) == sorted(
            list(stats_per_partner.keys())
        )
        assert all(
            [
                isinstance(stats, ConversationStats)
                for stats in stats_per_partner.values()
            ]
        )

    def test_get_all_channels_for_one_person(self, group_msg_analyzer):
        list_of_groups = group_msg_analyzer.get_all_channels_for_one_person(
            "Teflon Musk"
        )
        assert len(list_of_groups) == 2

    def test_min_group_size(self, group_msg_analyzer):
        minimum = group_msg_analyzer.min_channel_size
        assert minimum == 4

    def test_mean_group_size(self, group_msg_analyzer):
        mean = group_msg_analyzer.mean_channel_size
        assert mean == pytest.approx(4.66, 0.1)

    def test_max_group_size(self, group_msg_analyzer):
        maximum = group_msg_analyzer.max_channel_size
        assert maximum == 6

    def test_number_of_convos_created_by_me(self, group_msg_analyzer):
        created_by_me = group_msg_analyzer.number_of_convos_created_by_me
        assert created_by_me == 2

    def test_get_ranking_of_partners_by_convo_stats(self, group_msg_analyzer):
        ranking = group_msg_analyzer.get_ranking_of_senders_by_convo_stats()
        assert ranking.get("count") == {
            "Donald Duck": 6,
            "Levente Csőke": 4,
            "Foo Bar": 3,
            "Dér Dénes": 1,
            "Facebook User": 1,
            "John Doe": 1,
            "Teflon Musk": 1,
            "Tőke Hal": 1,
        }

    # def test_portion_of_contribution(self, group_msg_analyzer):
    #     contrib = group_msg_analyzer.get_portion_of_contribution()
    #     assert isinstance(contrib, dict)
    #     assert len(contrib)
    #     assert contrib["Foo Bar"] == pytest.approx(16.66, 0.1)
    #     assert contrib["Teflon Musk"] == pytest.approx(5.55, 0.1)
    #
    #     assert group_msg_analyzer.most_contributed == (
    #         "Donald Duck",
    #         pytest.approx(33.33, 0.1),
    #     )
    #
    #     least_contrib = group_msg_analyzer.least_contributed
    #     assert least_contrib[0] in (
    #         "Tőke Hal",
    #         "John Doe",
    #         "Teflon Musk",
    #         "Facebook User",
    #         "Dér Dénes",
    #     )
    #     assert least_contrib[1] == pytest.approx(5.55, 0.1)


class TestMessagingAnalyzerMethodsForPrivates:
    def test_filter_by_sender(self, priv_msg_analyzer):
        filtered = priv_msg_analyzer.filter(participants=["Teflon Musk"])
        assert isinstance(filtered, MessagingAnalyzer)
        assert len(filtered.data) == 1
        assert len(filtered.group_convo_map.get("Teflon Musk")) == 1

    def test_filter_by_channels(self, priv_msg_analyzer):
        filtered = priv_msg_analyzer.filter(channels="Teflon Musk")
        assert filtered.data.get("Teflon Musk")
        assert len(filtered.data) == 1
        assert len(filtered.group_convo_map) == 2

    def test_filter_by_channels_and_sender(self, priv_msg_analyzer):
        filtered = priv_msg_analyzer.filter(
            channels="Teflon Musk", participants="Teflon Musk"
        )
        assert len(filtered.data) == 1
        assert len(filtered.group_convo_map) == 2

        filtered = priv_msg_analyzer.filter(
            channels=["marathon"], participants="Benedek Elek"
        )

        assert not len(filtered)

        filtered = priv_msg_analyzer.filter(channels=["gibberish"])

        assert not len(filtered)

    def test_get_stats_per_channel(self, priv_msg_analyzer):
        stats_per_channel = priv_msg_analyzer._get_stats_per_channel()

        assert len(stats_per_channel) == 4
        assert list(priv_msg_analyzer.data.keys()) == list(stats_per_channel.keys())
        assert all(
            [
                isinstance(stats, ConversationStats)
                for stats in stats_per_channel.values()
            ]
        )

    def test_get_stats_per_sender(self, priv_msg_analyzer):
        stats_per_sender = priv_msg_analyzer._get_stats_per_participant()

        assert len(stats_per_sender) == 5
        assert list(priv_msg_analyzer.participants) == sorted(
            list(stats_per_sender.keys())
        )
        assert all(
            [
                isinstance(stats, ConversationStats)
                for stats in stats_per_sender.values()
            ]
        )

    def test_get_all_channels_for_one_person(self, priv_msg_analyzer):
        list_of_groups = priv_msg_analyzer.get_all_channels_for_one_person(
            "Teflon Musk"
        )
        assert len(list_of_groups) == 1

    def test_group_size(self, priv_msg_analyzer):
        minimum = priv_msg_analyzer.min_channel_size
        assert minimum == 2
        mean = priv_msg_analyzer.mean_channel_size
        assert mean == 2

        maximum = priv_msg_analyzer.max_channel_size
        assert maximum == 2

    def test_number_of_convos_created_by_me(self, priv_msg_analyzer):
        created_by_me = priv_msg_analyzer.number_of_convos_created_by_me
        assert created_by_me == 4

    def test_get_ranking_of_partners_by_convo_stats(self, priv_msg_analyzer):
        ranking = priv_msg_analyzer.get_ranking_of_senders_by_convo_stats()
        assert ranking.get("count") == {
            "Foo Bar": 15,
            "Tőke Hal": 7,
            "Teflon Musk": 6,
            "Benedek Elek": 3,
        }

    # def test_portion_of_contribution(self, priv_msg_analyzer):
    #     contrib = priv_msg_analyzer.get_portion_of_contribution()
    #     assert isinstance(contrib, dict)
    #     assert len(contrib)
    #     assert contrib["Foo Bar"] == pytest.approx(48.38, 0.1)
    #     assert contrib["Teflon Musk"] == pytest.approx(19.35, 0.1)
    #
    #     assert priv_msg_analyzer.most_contributed == (
    #         "Foo Bar",
    #         pytest.approx(48.38, 0.1),
    #     )
    #
    #     least_contrib = priv_msg_analyzer.least_contributed
    #     assert least_contrib[0] in ("Benedek Elek",)
    #     assert least_contrib[1] == pytest.approx(9.67, 0.1)


class TestGetCount:
    def test_total_number_of_messages(self, stat_count):
        assert stat_count(attribute="mc") == 31

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
        assert stat_count(attribute="mc", senders="me",) == 18
        assert (
            stat_count(attribute="mc", senders="me", start=dt(y=2014), period="y") == 7
        )
        assert (
            stat_count(attribute="mc", senders="me", start=dt(y=2018), period="y") == 2
        )
        assert (
            stat_count(attribute="mc", senders="me", start=dt(y=2020), period="y") == 9
        )

        assert (
            stat_count(attribute="mc", senders="me", start=dt(y=2014, m=9), period="m",)
            == 1
        )
        assert (
            stat_count(
                attribute="mc", senders="me", start=dt(y=2014, m=11), period="m",
            )
            == 5
        )
        assert (
            stat_count(
                attribute="mc", senders="me", start=dt(y=2014, m=12), period="m",
            )
            == 1
        )
        assert (
            stat_count(attribute="mc", senders="me", start=dt(y=2018, m=1), period="m",)
            == 2
        )

        assert (
            stat_count(attribute="mc", senders="me", start=dt(y=2000), period="y") == 0
        )
        assert (
            stat_count(
                attribute="mc", senders="me", start=dt(y=2011, m=11), period="m",
            )
            == 0
        )
        assert (
            stat_count(attribute="mc", senders="me", start=dt(y=2018, m=5), period="m",)
            == 0
        )

        assert (
            stat_count(attribute="mc", senders="me", start=dt(y=2020, m=2), period="m",)
            == 6
        )
        assert (
            stat_count(attribute="mc", senders="me", start=dt(y=2020, m=3), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="mc", senders="me", start=dt(y=2020, m=4), period="m",)
            == 2
        )
        assert (
            stat_count(attribute="mc", senders="me", start=dt(y=2020, m=5), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="mc", senders="me", start=dt(y=2020, m=6), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="mc", senders="me", start=dt(y=2020, m=8), period="m",)
            == 1
        )

        assert (
            stat_count(
                attribute="mc", senders="me", start=dt(y=2020, m=2, d=13), period="d",
            )
            == 1
        )
        assert (
            stat_count(
                attribute="mc",
                senders="me",
                start=dt(y=2020, m=2, d=13, h=6),
                period="h",
            )
            == 1
        )
        assert (
            stat_count(
                attribute="mc",
                senders="me",
                start=dt(y=2020, m=2, d=13, h=18),
                period="h",
            )
            == 0
        )

    def test_total_number_of_words_sent(self, stat_count):
        assert stat_count(attribute="wc", senders="me",) == 71
        assert (
            stat_count(attribute="wc", senders="me", start=dt(y=2000), period="y") == 0
        )
        assert (
            stat_count(attribute="wc", senders="me", start=dt(y=2014), period="y") == 18
        )
        assert (
            stat_count(attribute="wc", senders="me", start=dt(y=2018), period="y") == 31
        )
        assert (
            stat_count(attribute="wc", senders="me", start=dt(y=2020), period="y") == 22
        )

        assert (
            stat_count(attribute="wc", senders="me", start=dt(y=2014, m=9), period="m",)
            == 6
        )
        assert (
            stat_count(
                attribute="wc", senders="me", start=dt(y=2014, m=11), period="m",
            )
            == 11
        )
        assert (
            stat_count(
                attribute="wc", senders="me", start=dt(y=2014, m=12), period="m",
            )
            == 1
        )

        assert (
            stat_count(attribute="wc", senders="me", start=dt(y=2018, m=1), period="m",)
            == 31
        )
        assert (
            stat_count(attribute="wc", senders="me", start=dt(y=2018, m=2), period="m",)
            == 0
        )

        assert (
            stat_count(attribute="wc", senders="me", start=dt(y=2020, m=2), period="m",)
            == 16
        )
        assert (
            stat_count(attribute="wc", senders="me", start=dt(y=2020, m=3), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="wc", senders="me", start=dt(y=2020, m=4), period="m",)
            == 4
        )
        assert (
            stat_count(attribute="wc", senders="me", start=dt(y=2020, m=5), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="wc", senders="me", start=dt(y=2020, m=6), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="wc", senders="me", start=dt(y=2020, m=8), period="m",)
            == 2
        )

        assert (
            stat_count(
                attribute="wc", senders="me", start=dt(y=2020, m=2, d=13), period="d",
            )
            == 5
        )
        assert (
            stat_count(
                attribute="wc",
                senders="me",
                start=dt(y=2020, m=2, d=13, h=6),
                period="h",
            )
            == 5
        )
        assert (
            stat_count(
                attribute="wc",
                senders="me",
                start=dt(y=2020, m=2, d=13, h=7),
                period="h",
            )
            == 0
        )

    def test_total_number_of_characters_sent(self, stat_count):
        assert stat_count(attribute="cc", senders="me",) == 321

        assert (
            stat_count(attribute="cc", senders="me", start=dt(y=2000), period="y") == 0
        )
        assert (
            stat_count(attribute="cc", senders="me", start=dt(y=2014), period="y") == 70
        )
        assert (
            stat_count(attribute="cc", senders="me", start=dt(y=2018), period="y")
            == 167
        )
        assert (
            stat_count(attribute="cc", senders="me", start=dt(y=2020), period="y") == 84
        )

        assert (
            stat_count(attribute="cc", senders="me", start=dt(y=2014, m=9), period="m",)
            == 24
        )
        assert (
            stat_count(
                attribute="cc", senders="me", start=dt(y=2014, m=11), period="m",
            )
            == 43
        )
        assert (
            stat_count(
                attribute="cc", senders="me", start=dt(y=2014, m=12), period="m",
            )
            == 3
        )

        assert (
            stat_count(attribute="cc", senders="me", start=dt(y=2018, m=1), period="m",)
            == 167
        )
        assert (
            stat_count(attribute="cc", senders="me", start=dt(y=2018, m=2), period="m",)
            == 0
        )

        assert (
            stat_count(attribute="cc", senders="me", start=dt(y=2020, m=2), period="m",)
            == 62
        )
        assert (
            stat_count(attribute="cc", senders="me", start=dt(y=2020, m=3), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="cc", senders="me", start=dt(y=2020, m=4), period="m",)
            == 17
        )
        assert (
            stat_count(attribute="cc", senders="me", start=dt(y=2020, m=5), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="cc", senders="me", start=dt(y=2020, m=6), period="m",)
            == 0
        )
        assert (
            stat_count(attribute="cc", senders="me", start=dt(y=2020, m=8), period="m",)
            == 5
        )

        assert (
            stat_count(
                attribute="cc",
                senders="me",
                start=dt(y=2020, m=2, d=13, h=6),
                period="d",
            )
            == 21
        )
        assert (
            stat_count(
                attribute="cc",
                senders="me",
                start=dt(y=2020, m=2, d=13, h=7),
                period="d",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="cc",
                senders="me",
                start=dt(y=2020, m=2, d=13, h=6),
                period="h",
            )
            == 21
        )
        assert (
            stat_count(
                attribute="cc",
                senders="me",
                start=dt(y=2020, m=2, d=13, h=7),
                period="h",
            )
            == 0
        )

    def test_total_number_of_messages_received(self, stat_count):
        assert stat_count(attribute="mc", senders="partner",) == 13
        assert (
            stat_count(attribute="mc", senders="partner", start=dt(y=2000), period="y",)
            == 0
        )
        assert (
            stat_count(attribute="mc", senders="partner", start=dt(y=2014), period="y",)
            == 6
        )
        assert (
            stat_count(attribute="mc", senders="partner", start=dt(y=2018), period="y",)
            == 1
        )
        assert (
            stat_count(attribute="mc", senders="partner", start=dt(y=2020), period="y",)
            == 6
        )

        assert (
            stat_count(
                attribute="mc", senders="partner", start=dt(y=2011, m=11), period="m",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="mc", senders="partner", start=dt(y=2014, m=9), period="m",
            )
            == 0
        )
        assert (
            stat_count(
                attribute="mc", senders="partner", start=dt(y=2014, m=11), period="m",
            )
            == 5
        )
        assert (
            stat_count(
                attribute="mc", senders="partner", start=dt(y=2014, m=12), period="m",
            )
            == 1
        )

        assert (
            stat_count(
                attribute="mc", senders="partner", start=dt(y=2018, m=1), period="m",
            )
            == 1
        )
        assert (
            stat_count(
                attribute="mc", senders="partner", start=dt(y=2018, m=5), period="m",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="mc", senders="partner", start=dt(y=2020, m=2), period="m",
            )
            == 4
        )
        assert (
            stat_count(
                attribute="mc", senders="partner", start=dt(y=2020, m=3), period="m",
            )
            == 1
        )
        assert (
            stat_count(
                attribute="mc", senders="partner", start=dt(y=2020, m=4), period="m",
            )
            == 0
        )
        assert (
            stat_count(
                attribute="mc", senders="partner", start=dt(y=2020, m=5), period="m",
            )
            == 1
        )
        assert (
            stat_count(
                attribute="mc", senders="partner", start=dt(y=2020, m=8), period="m",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="mc",
                senders="partner",
                start=dt(y=2020, m=2, d=13),
                period="d",
            )
            == 1
        )
        assert (
            stat_count(
                attribute="mc",
                senders="partner",
                start=dt(y=2020, m=2, d=14),
                period="d",
            )
            == 2
        )
        assert (
            stat_count(
                attribute="mc",
                senders="partner",
                start=dt(y=2020, m=2, d=18),
                period="d",
            )
            == 1
        )

    def test_total_number_of_words_received(self, stat_count):
        assert stat_count(attribute="wc", senders="partner",) == 20

        assert (
            stat_count(attribute="wc", senders="partner", start=dt(y=2000), period="y",)
            == 0
        )
        assert (
            stat_count(attribute="wc", senders="partner", start=dt(y=2014), period="y",)
            == 7
        )
        assert (
            stat_count(attribute="wc", senders="partner", start=dt(y=2018), period="y",)
            == 1
        )
        assert (
            stat_count(attribute="wc", senders="partner", start=dt(y=2020), period="y",)
            == 12
        )

        assert (
            stat_count(
                attribute="wc", senders="partner", start=dt(y=2014, m=9), period="m",
            )
            == 0
        )
        assert (
            stat_count(
                attribute="wc", senders="partner", start=dt(y=2014, m=11), period="m",
            )
            == 7
        )
        assert (
            stat_count(
                attribute="wc", senders="partner", start=dt(y=2014, m=12), period="m",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="wc", senders="partner", start=dt(y=2018, m=1), period="m",
            )
            == 1
        )
        assert (
            stat_count(
                attribute="wc", senders="partner", start=dt(y=2018, m=2), period="m",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="wc", senders="partner", start=dt(y=2020, m=2), period="m",
            )
            == 11
        )
        assert (
            stat_count(
                attribute="wc", senders="partner", start=dt(y=2020, m=3), period="m",
            )
            == 0
        )
        assert (
            stat_count(
                attribute="wc", senders="partner", start=dt(y=2020, m=5), period="m",
            )
            == 1
        )

        assert (
            stat_count(
                attribute="wc",
                senders="partner",
                start=dt(y=2020, m=2, d=13),
                period="d",
            )
            == 9
        )
        assert (
            stat_count(
                attribute="wc",
                senders="partner",
                start=dt(y=2020, m=2, d=14),
                period="d",
            )
            == 2
        )
        assert (
            stat_count(
                attribute="wc",
                senders="partner",
                start=dt(y=2020, m=2, d=18),
                period="d",
            )
            == 0
        )

    def test_total_number_of_characters_received(self, stat_count):
        assert stat_count(attribute="cc", senders="partner",) == 88

        assert (
            stat_count(attribute="cc", senders="partner", start=dt(y=2000), period="y",)
            == 0
        )
        assert (
            stat_count(attribute="cc", senders="partner", start=dt(y=2014), period="y",)
            == 29
        )
        assert (
            stat_count(attribute="cc", senders="partner", start=dt(y=2018), period="y",)
            == 3
        )
        assert (
            stat_count(attribute="cc", senders="partner", start=dt(y=2020), period="y",)
            == 56
        )

        assert (
            stat_count(
                attribute="cc", senders="partner", start=dt(y=2014, m=9), period="m",
            )
            == 0
        )
        assert (
            stat_count(
                attribute="cc", senders="partner", start=dt(y=2014, m=11), period="m",
            )
            == 29
        )
        assert (
            stat_count(
                attribute="cc", senders="partner", start=dt(y=2014, m=12), period="m",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="cc", senders="partner", start=dt(y=2018, m=1), period="m",
            )
            == 3
        )
        assert (
            stat_count(
                attribute="cc", senders="partner", start=dt(y=2018, m=2), period="m",
            )
            == 0
        )

        assert (
            stat_count(
                attribute="cc", senders="partner", start=dt(y=2020, m=2), period="m",
            )
            == 52
        )
        assert (
            stat_count(
                attribute="cc", senders="partner", start=dt(y=2020, m=3), period="m",
            )
            == 0
        )
        assert (
            stat_count(
                attribute="cc", senders="partner", start=dt(y=2020, m=5), period="m",
            )
            == 4
        )

        assert (
            stat_count(
                attribute="cc",
                senders="partner",
                start=dt(y=2020, m=2, d=13),
                period="d",
            )
            == 30
        )
        assert (
            stat_count(
                attribute="cc",
                senders="partner",
                start=dt(y=2020, m=2, d=14),
                period="d",
            )
            == 22
        )
        assert (
            stat_count(
                attribute="cc",
                senders="partner",
                start=dt(y=2020, m=2, d=18),
                period="d",
            )
            == 0
        )
