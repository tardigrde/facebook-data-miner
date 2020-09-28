from typing import Any, Callable, Dict, List, NamedTuple, Union

import pandas as pd

from miner.utils import command, utils


class FacebookData:
    """
    Super class for reading, processing and storing tabular Facebook Data.
    """

    def __init__(
        self,
        path: str,
        reader: Union[None, Callable] = None,
        processors: Union[None, List[Callable]] = None,
    ) -> None:
        self.path: str = path
        self._reader = reader
        self._preprocessor: command.CommandChainCreator = (
            self._get_preprocessor(processors)
        )

        self._metadata: NamedTuple
        self._data: pd.DataFrame = self._get_data()

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
    def reader(self) -> Callable:
        return utils.read_json if self._reader is None else self._reader

    def _register_processors(
        self, preprocessor: command.CommandChainCreator
    ) -> None:
        raise NotImplementedError()

    @property
    def preprocessor(self) -> command.CommandChainCreator:
        return self._preprocessor

    def _get_data(self) -> Any:
        raw_data = self._read_data(self.reader, self.path)
        return self.preprocessor(raw_data)

    def _get_preprocessor(
        self, processors: Union[None, List[Callable]]
    ) -> command.CommandChainCreator:
        preprocessor = command.CommandChainCreator()
        if processors is None:
            self._register_processors(preprocessor)
        else:
            for func, args, kwargs in processors:  # type: ignore
                preprocessor.register_command(
                    func, *args, **kwargs  # type: ignore
                )
        return preprocessor

    @staticmethod
    def _read_data(reader: Callable, path: str) -> Dict:
        return reader(path)

    @staticmethod
    def _get_dataframe(
        data: Union[pd.DataFrame, Dict[str, Any]],
        field: Union[str, None] = None,
        **kwargs: Any,
    ) -> pd.DataFrame:

        data = data.get(field) if field else data
        return pd.DataFrame(data, **kwargs)

    @staticmethod
    def _set_date_as_index(data: pd.DataFrame, column: str) -> pd.DataFrame:
        date_series = data[column].apply(utils.ts_to_date)
        data = data.drop(columns=[column])
        return data.set_index(date_series).iloc[::-1]
