from typing import List, Dict, Callable, Any, NamedTuple, Union

import pandas as pd

from miner.utils import utils, command


class FacebookData:
    """
    Super class for reading, processing and storing tabular Facebook Data.
    """

    def __init__(
        self, path: str, reader: Callable = None, processors: List[Callable] = None
    ) -> None:
        self.path: str = path
        self._reader: Callable = reader
        self._preprocessor: Callable = self._get_preprocessor(processors)

        self._metadata: NamedTuple
        self._data = self._get_data()

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
    def reader(self) -> Union[Dict, List]:
        return utils.read_json if self._reader is None else self._reader

    @property
    def preprocessor(self) -> command.CommandChainCreator:
        return self._preprocessor

    def _get_data(self) -> Any:
        raw_data = self._read_data(self.reader, self.path)
        return self.preprocessor(raw_data)

    def _get_preprocessor(
        self, processors: List[Callable]
    ) -> command.CommandChainCreator:
        preprocessor = command.CommandChainCreator()
        if processors is None:
            self._register_processors(preprocessor)
        else:
            for func, args, kwargs in processors:
                preprocessor.register_command(func, *args, **kwargs)
        return preprocessor

    @staticmethod
    def _read_data(reader: Callable, path: str) -> Dict:
        return reader(path)

    @staticmethod
    def _get_dataframe(data, field: str = None, **kwargs) -> pd.DataFrame:
        data = data.get(field) if field else data
        return pd.DataFrame(data, **kwargs)

    @staticmethod
    def _set_date_as_index(data: pd.DataFrame, column: str) -> pd.DataFrame:
        date_series = data[column].apply(utils.ts_to_date)
        data = data.drop(columns=[column])
        return data.set_index(date_series).iloc[::-1]
