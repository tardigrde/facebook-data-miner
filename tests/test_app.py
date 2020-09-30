from miner.friends import Friends
from miner.message.conversations import Conversations
from miner.message.messaging_analyzer import MessagingAnalyzerManager
from miner.people import People
from miner.profile_information import ProfileInformation


class TestApp:
    def test_friends(self, app):
        friends = app.friends
        assert isinstance(friends, Friends)

    def test_conversations(self, app):
        conversations = app.conversations
        assert isinstance(conversations, Conversations)

    def test_analyzer(self, app):
        analyzer = app.analyzer
        assert isinstance(analyzer, MessagingAnalyzerManager)

    def test_people(self, app):
        people = app.people
        assert isinstance(people, People)

    def test_config(self, app):
        config = app.config
        assert isinstance(config, dict)
        assert "profile" in config

    def test_profile_information(self, app):
        pi = app.profile_information
        assert isinstance(pi, ProfileInformation)
