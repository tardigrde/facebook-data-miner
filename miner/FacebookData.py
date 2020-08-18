from miner import utils
import pandas as pd


class FacebookData:
    """
    Base class for reading in tabular data from JSONs.
    """
    # TODO general FBData should have read write ..... get
    # TODO FBTabularData should have to_df
    # TODO all the propertys could be iterators

    def __init__(self, json_path):
        self.json_path = json_path
        self._df = None

    @property
    def df(self):
        return self._df

    @property
    def decoded(self):
        # TODO maybe add decoder as a dependecy
        return utils.decode_text(self.json)

    @property
    def json(self):
        # TODO make this more general. get_data or add the data getter as a dep
        return utils.read_json(self.json_path)

    @property
    def compact_names(self):
        # TODO PD dont switch this to simple list
        name_list = list(utils.without_accent_and_whitespace(utils.lower_names(self.names)))
        return name_list[0] if len(name_list) == 1 else name_list

    def to_df(self, field=None):
        # TODO geralize? maybe put this into the construcor
        self._df = pd.DataFrame(self.decoded.get(field))
