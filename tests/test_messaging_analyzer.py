import pytest

from miner.message.conversation_stats import ConversationStats
from miner.message.messaging_analyzer import MessagingAnalyzerManager, MessagingAnalyzer


class TestMessagingAnalyzerManager:
    def test_private_and_group_instances(self, analyzer):
        isinstance(analyzer, MessagingAnalyzerManager)
        isinstance(analyzer.private, MessagingAnalyzer)
        isinstance(analyzer.group, MessagingAnalyzer)

    def test_people_i_have_private_and_group__convo_with(self, analyzer):
        assert len(analyzer.people_i_have_private_convo_with) == 4
        assert len(analyzer.people_i_have_group_convo_with) == 8

    def test_get_who_i_have_private_convo_with_from_a_group(self, analyzer):
        have = analyzer.get_who_i_have_private_convo_with_from_a_group("marathon")
        assert have == ["Bugs Bunny", "Foo Bar"]

    def test_how_much_i_speak_in_private_with_group_members(self, analyzer):
        spoke = analyzer.how_much_i_speak_in_private_with_group_members("marathon")
        assert spoke == {"Foo Bar": 15, "Bugs Bunny": 6}

    def test_all_interactions(self, analyzer):
        private, group = analyzer.all_interactions("Bugs Bunny")
        assert private._stats.channels == ["Bugs Bunny"]
        assert group._stats.channels == [
            "Foo Bar, John Doe and Bugs Bunny",
            "marathon",
        ]

    def test_is_priv_msg_first_then_group(self, analyzer):
        is_priv = analyzer.is_private_convo_first_then_group("Bugs Bunny")
        assert is_priv is True

        is_priv = analyzer.is_private_convo_first_then_group("Benedek Elek")
        assert is_priv is True  # only has private

        is_priv = analyzer.is_private_convo_first_then_group("Foo Bar")
        assert is_priv is True

        is_priv = analyzer.is_private_convo_first_then_group("Tőke Hal")
        assert is_priv is True

    def test_get_stats_together(self, analyzer):
        stats = analyzer.get_stats_together("Foo Bar")
        assert stats.channels == [
            "Tőke Hal, Foo Bar, Donald Duck and 2 others",
            "Foo Bar, John Doe and Bugs Bunny",
            "marathon",
            "Foo Bar",
        ]
        assert stats.contributors == ["Foo Bar"]
        assert stats.df.shape == (9, 8)


class TestMessagingAnalyzerMethodsForGroups:
    def test_analyzer_groups(self, ganalyzer):
        groups = ganalyzer.data
        assert len(groups) == 3

    def test_filter_by_participants(self, ganalyzer):
        filtered = ganalyzer.filter(participants=["Bugs Bunny"])
        assert isinstance(filtered, MessagingAnalyzer)
        assert len(filtered.data) == 2
        assert len(filtered.participant_to_channel_map.get("Bugs Bunny")) == 2

        filtered = ganalyzer.filter(participants="Bugs Bunny")
        assert len(filtered.data) == 2

    def test_filter_by_channels(self, ganalyzer):
        filtered = ganalyzer.filter(channels=["marathon"])
        assert filtered.data.get("marathon")
        assert len(filtered.data) == 1
        assert len(filtered.participant_to_channel_map) == 4

        filtered = ganalyzer.filter(channels="marathon")
        assert len(filtered.data) == 1

    def test_filter_by_channels_and_participants(self, ganalyzer):
        filtered = ganalyzer.filter(channels=["marathon"], participants="Bugs Bunny")
        assert filtered.data.get("marathon")
        assert len(filtered.data) == 1
        assert len(filtered.participant_to_channel_map) == 4

        filtered = ganalyzer.filter(channels=["marathon"], participants="Benedek Elek")

        assert not len(filtered)

        filtered = ganalyzer.filter(channels=["gibberish"])

        assert not len(filtered)

    def test_get_stats_per_channel(self, ganalyzer):
        stats_per_channel = ganalyzer._get_stats_per_channel()

        assert len(stats_per_channel) == 3
        assert list(ganalyzer.data.keys()) == list(stats_per_channel.keys())
        assert all(
            [
                isinstance(stats, ConversationStats)
                for stats in stats_per_channel.values()
            ]
        )

    def test_get_stats_per_participant(self, ganalyzer):
        stats_per_partner = ganalyzer._get_stats_per_participant()

        assert len(stats_per_partner) == 8
        assert list(ganalyzer.participants) == sorted(list(stats_per_partner.keys()))
        assert all(
            [
                isinstance(stats, ConversationStats)
                for stats in stats_per_partner.values()
            ]
        )

    def test_get_all_channels_for_one_person(self, ganalyzer):
        list_of_groups = ganalyzer.get_all_channels_for_one_person("Bugs Bunny")
        assert len(list_of_groups) == 2

    def test_min_group_size(self, ganalyzer):
        minimum = ganalyzer.min_channel_size
        assert minimum == 4

    def test_mean_group_size(self, ganalyzer):
        mean = ganalyzer.mean_channel_size
        assert mean == pytest.approx(4.66, 0.1)

    def test_max_group_size(self, ganalyzer):
        maximum = ganalyzer.max_channel_size
        assert maximum == 6

    def test_number_of_convos_created_by_me(self, ganalyzer):
        created_by_me = ganalyzer.number_of_convos_created_by_me
        assert created_by_me == 2

    def test_get_ranking_of_partners_by_convo_stats(self, ganalyzer):
        ranking = ganalyzer.get_ranking_of_people_by_convo_stats()
        assert ranking.get("count") == {
            "Donald Duck": 6,
            "Jenő Rejtő": 4,
            "Foo Bar": 3,
            "Dér Dénes": 1,
            "Facebook User": 1,
            "John Doe": 1,
            "Bugs Bunny": 1,
            "Tőke Hal": 1,
        }


class TestMessagingAnalyzerMethodsForPrivates:
    def test_filter_by_participants(self, panalyzer):
        filtered = panalyzer.filter(participants=["Bugs Bunny"])
        assert isinstance(filtered, MessagingAnalyzer)
        assert len(filtered.data) == 1
        assert len(filtered.participant_to_channel_map.get("Bugs Bunny")) == 1

    def test_filter_by_channels(self, panalyzer):
        filtered = panalyzer.filter(channels="Bugs Bunny")
        assert filtered.data.get("Bugs Bunny")
        assert len(filtered.data) == 1
        assert len(filtered.participant_to_channel_map) == 2

    def test_filter_by_channels_and_participants(self, panalyzer):
        filtered = panalyzer.filter(channels="Bugs Bunny", participants="Bugs Bunny")
        assert len(filtered.data) == 1
        assert len(filtered.participant_to_channel_map) == 2

        filtered = panalyzer.filter(channels=["marathon"], participants="Benedek Elek")

        assert not len(filtered)

        filtered = panalyzer.filter(channels=["gibberish"])

        assert not len(filtered)

    def test_get_stats_per_channel(self, panalyzer):
        stats_per_channel = panalyzer._get_stats_per_channel()

        assert len(stats_per_channel) == 4
        assert list(panalyzer.data.keys()) == list(stats_per_channel.keys())
        assert all(
            [
                isinstance(stats, ConversationStats)
                for stats in stats_per_channel.values()
            ]
        )

    def test_get_stats_per_participant(self, panalyzer):
        stats_per_sender = panalyzer._get_stats_per_participant()

        assert len(stats_per_sender) == 5
        assert list(panalyzer.participants) == sorted(list(stats_per_sender.keys()))
        assert all(
            [
                isinstance(stats, ConversationStats)
                for stats in stats_per_sender.values()
            ]
        )

    def test_get_all_channels_for_one_person(self, panalyzer):
        list_of_groups = panalyzer.get_all_channels_for_one_person("Bugs Bunny")
        assert len(list_of_groups) == 1

    def test_group_size(self, panalyzer):
        minimum = panalyzer.min_channel_size
        assert minimum == 2
        mean = panalyzer.mean_channel_size
        assert mean == 2

        maximum = panalyzer.max_channel_size
        assert maximum == 2

    def test_number_of_convos_created_by_me(self, panalyzer):
        created_by_me = panalyzer.number_of_convos_created_by_me
        assert created_by_me == 4

    def test_get_ranking_of_partners_by_convo_stats(self, panalyzer):
        ranking = panalyzer.get_ranking_of_people_by_convo_stats()
        assert ranking.get("count") == {
            "Foo Bar": 15,
            "Tőke Hal": 7,
            "Bugs Bunny": 6,
            "Benedek Elek": 3,
        }
