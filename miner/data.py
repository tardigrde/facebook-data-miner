from miner import utils
import pandas as pd
import os
from typing import Union, List, Dict, Callable, Any, NamedTuple

DATA_PATH = f'{os.getcwd()}/data'


class FacebookData:

    def __init__(self, path: str, reader: Callable = None, processors: List[Callable] = None) -> None:
        self.path: str = path
        self._reader: Callable = reader
        self._preprocessor: Callable = self.get_preprocessor(processors)

        self._metadata: NamedTuple
        self._data = self.get_data()

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @data.setter
    def data(self, df: pd.DataFrame) -> None:
        self._data = df

    @property
    def metadata(self) -> NamedTuple:
        return self._metadata

    @property
    def reader(self):
        return utils.read_json if self._reader is None else self._reader

    @property
    def preprocessor(self):
        return self._preprocessor

    def register_processors(self, preprocessor):
        raise NotImplementedError()

    def get_data(self, ) -> Any:
        raw_data = self.read_data(self.reader, self.path)
        return self.preprocessor(raw_data)

    def get_preprocessor(self, processors):
        preprocessor = utils.CommandChainCreator()
        if processors is None:
            self.register_processors(preprocessor)
        else:
            for func, args, kwargs in processors:
                preprocessor.register_command(func, *args, **kwargs)
        return preprocessor

    @staticmethod
    def read_data(reader: Callable, path: str) -> Dict:
        return reader(path)

    @staticmethod
    def get_dataframe(data, field=None, **kwargs):
        data = data.get(field) if field else data
        return pd.DataFrame(data, **kwargs)

    @staticmethod
    def set_date_as_index(data: pd.DataFrame, column: str) -> pd.DataFrame:
        date_series = data[column].apply(utils.ts_to_date)
        data = data.drop(columns=[column])
        return data.set_index(date_series).iloc[::-1]
