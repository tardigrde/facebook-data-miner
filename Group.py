# TODO LATER groups should be searched by looking into jsons unfortunately :(
# because of directory says others
# maybe we dont use groups right away?


class Group:
    def __init__(self, name=None, title=None, messages=None, compact=None, messages_dir=None, media_dir=None,
                 members=None):
        self._name = name
        self._title = title
        self._messages = messages
        self._compact_name = compact
        self._messages_dir = messages_dir
        self._media_dir = media_dir
        self._members = members

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._title

    @property
    def messages(self):
        return self._messages

    # @property
    # def get_message_jsons(self):
    #     return self._messages

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
    def members(self):
        return self._members
