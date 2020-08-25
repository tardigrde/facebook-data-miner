from typing import Union, List, Dict, Callable, Any
from collections import namedtuple

from miner.data import FacebookData
from miner import utils


class Friends(FacebookData):
    def __init__(
        self, path: str, reader: Callable = None, processors: List[Callable] = None
    ) -> None:
        super().__init__(path, reader=reader, processors=processors)

    def register_processors(self, preprocessor):
        preprocessor.register_command(utils.decode_data, utils.utf8_decoder)
        preprocessor.register_command(self.set_metadata)
        preprocessor.register_command(
            self.get_dataframe, field="friends", columns=["name", "timestamp"]
        )
        preprocessor.register_command(self.set_date_as_index, column="timestamp")
        return preprocessor

    def set_metadata(self, data: Dict) -> Dict:
        metadata = namedtuple("metadata", ["length", "path"])
        self._metadata = metadata(length=len(data.get("friends")), path=self.path)
        return data
