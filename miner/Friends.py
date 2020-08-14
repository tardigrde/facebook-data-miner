from miner.FacebookData import FacebookData
from miner.Individual import Individual


class Friends(FacebookData):

    def __init__(self, *args):
        super().__init__(*args)
        self.to_df('friends')

    def get_people(self, name=None):
        names = {}
        for full_name, compact in zip(self.names, self.compact_names):
            if name is not None and name != full_name:  # filtering for name
                continue
            names[full_name] = Individual(
                name=full_name,
                compact=compact,
                friend=True,
            )
        return names

    @property
    def names(self):
        return self.df.name
