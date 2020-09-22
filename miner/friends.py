from collections import namedtuple
from typing import List, Dict, Callable

from miner.data import FacebookData
from miner.utils import utils, decorators


# TODO rate of making friends
class Friends(FacebookData):
    def __init__(
        self, path: str, reader: Callable = None, processors: List[Callable] = None
    ) -> None:
        super().__init__(path, reader=reader, processors=processors)

    def get(self, sort="date", dates=True, output=None):
        data = self.data
        if sort == "name":
            data = data.sort_values(by="name")
        if not dates:
            data.reset_index(drop=True, inplace=True)

        return utils.df_to_file(output, data)

    def _register_processors(self, preprocessor):
        preprocessor.register_command(utils.decode_data, utils.utf8_decoder)
        preprocessor.register_command(self._set_metadata)
        preprocessor.register_command(
            self._get_dataframe, field="friends", columns=["name", "timestamp"]
        )
        preprocessor.register_command(self._set_date_as_index, column="timestamp")
        return preprocessor

    def _set_metadata(self, data: Dict) -> Dict:
        metadata = namedtuple("metadata", ["length", "path"])
        self._metadata = metadata(length=len(data.get("friends")), path=self.path)
        return data
