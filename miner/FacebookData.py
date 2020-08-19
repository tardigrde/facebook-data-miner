from miner import utils
import pandas as pd
import os
from typing import Union, List, Dict, Callable, Any, NamedTuple

DATA_PATH = f'{os.getcwd()}/data'


class FacebookData:
    def __init__(self) -> None:
        self._metadata: NamedTuple = None
        self._data = self.get_data(reader=self.reader, processors=self.processors)

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @data.setter
    def data(self, df: pd.DataFrame) -> None:
        self._data = df

    @property
    def metadata(self) -> NamedTuple:
        return self._metadata

    def get_data(self, reader: Callable, processors: List[Callable]) -> Any:
        raw_data = self.read_data(reader, self.path)
        return self.preprocess(processors, raw_data)

    @staticmethod
    def read_data(reader: Callable, path: str) -> Dict:
        return reader(path)

    @staticmethod
    def preprocess(processors: List[Callable], data: Union[List, Dict]) -> Union[Dict, pd.DataFrame]:
        for func in processors:
            if not callable(func):
                raise SystemExit(f'Processor {func} is not callable.')
            try:  # TODO should we use try except
                data = func(data)
            except TypeError:
                print('Not good function')  # TODO
        return data

    def decode_text(self, obj: Union[str, List, Dict]) -> Union[str, List, Dict]:
        if isinstance(obj, str):
            return obj.encode('latin_1').decode('utf-8')

        if isinstance(obj, list):
            return [self.decode_text(o) for o in obj]

        if isinstance(obj, dict):
            return {key: self.decode_text(item) for key, item in obj.items()}

        return obj

    @staticmethod
    def get_dataframe(data: Union[List, Dict]) -> pd.DataFrame:
        return pd.DataFrame(data)

# class TabularFacebookData(FacebookData):
#     """
#     Base class for reading in tabular data from JSONs.
#     """
#
#     # TODO general FBData should have read write ..... get
#     # TODO FBTabularData should have to_df
#     # TODO all the propertys could be iterators
#
#     def __init__(self, json_path):
#         super().__init__()
#         self.json_path = json_path
#         self._df = None
#
#     @property
#     def df(self):
#         return self._df
#
#     @property
#     def decoded(self):
#         # TODO maybe add decoder as a dependecy
#         return utils.decode_text(self.json)
#
#     @property
#     def json(self):
#         # TODO make this more general. get_data or add the data getter as a dep
#         return utils.read_json(self.json_path)
#
#     @property
#     def compact_names(self):
#         # TODO PD dont switch this to simple list
#         name_list = list(utils.without_accent_and_whitespace(utils.lower_names(self.names)))
#         return name_list[0] if len(name_list) == 1 else name_list
#
#     def to_df(self, field=None):
#         # TODO geralize? maybe put this into the construcor
#         self._df = pd.DataFrame(self.decoded.get(field))
