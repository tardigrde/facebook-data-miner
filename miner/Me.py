from miner.FacebookData import FacebookData


class Me(FacebookData):
    """
    Class for storing basic data about the user
    """

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def name(self):
        return ''
