from FacebookData import FacebookData


class Me(FacebookData):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def name(self):
        return 'Levente Csőke'
