class Individual:
    def __init__(self, name=None, title=None,compact=None, messages=None, friend=None, messages_dir=None, media_dir=None,
                 member_of=None):
        self._name = name
        self._title = title
        self._compact_name = compact
        self._messages = messages
        self._friend = friend
        self._messages_dir = messages_dir
        self._media_dir = media_dir
        self._member_of = member_of


    def __repr__(self):
        return self.name

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._title

    @property
    def messages(self):
        return self._messages

    @property
    def friend(self):
        return self._friend

    @property
    def media_dir(self):
        return self._media_dir

    @property
    def messages_dir(self):
        return self._messages_dir

    @property
    def compact_name(self):
        return self._compact_name

    @property
    def member_of(self):
        return self._member_of
