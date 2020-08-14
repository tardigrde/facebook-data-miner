from miner import utils
import pandas as pd


class FacebookData:
    def __init__(self, json_path):
        self.json_path = json_path
        self._df = None

    @property
    def df(self):
        return self._df

    @property
    def decoded(self):
        return utils.decode_text(self.json)

    @property
    def json(self):
        return utils.read_json(self.json_path)

    @property
    def compact_names(self):
        name_list = list(utils.without_accent_and_whitespace(utils.lower_names(self.names)))  # should be just fine
        return name_list[0] if len(name_list) == 1 else name_list

    def to_df(self, field=None):
        self._df = pd.DataFrame(self.decoded.get(field))
