from collections import namedtuple
from typing import Callable, Dict, List, Union

from miner.data import FacebookData
from miner.utils import command, utils


# NOTE stats per making friends yet to be implemented
class Friends(FacebookData):
    """
    Class for reading in and storing data about our Facebook friends.
    """

    def __init__(
        self,
        path: str,
        reader: Union[None, Callable] = None,
        processors: Union[None, List[Callable]] = None,
    ) -> None:
        super().__init__(path, reader=reader, processors=processors)

    def __repr__(self) -> str:
        return f"<Storing {len(self.data)} friends>"

    def get(
        self,
        sort: str = "date",
        dates: bool = True,
        output: Union[str, None] = None,
    ) -> str:
        """
        Exposed function for getting data on our Facebook friends.

        @param sort: the column we want to sort by.
        Can be either of {date|name}. Default is `dates`.
        @param dates: boolean flag on do we want the dates column.
        Default is `True`.
        @param output: where do we want to write the return value,
        can be any of: {csv|json|/some/path.{json|csv}}.
        @return: either the data formatted as csv or json,
        or a success message about where was the data saved.
        """
        data = self.data
        if sort == "name":
            data = data.sort_values(by="name")
        if not dates:
            data.reset_index(drop=True, inplace=True)

        return utils.df_to_file(output, data)

    def _register_processors(
        self, preprocessor: command.CommandChainCreator
    ) -> command.CommandChainCreator:
        preprocessor.register_command(utils.decode_data, utils.utf8_decoder)
        preprocessor.register_command(self._set_metadata)
        preprocessor.register_command(
            self._get_dataframe, field="friends", columns=["name", "timestamp"]
        )
        preprocessor.register_command(
            self._set_date_as_index, column="timestamp"
        )
        return preprocessor

    def _set_metadata(self, data: Dict[str, Dict[str, str]]) -> Dict:
        metadata = namedtuple("metadata", ["length", "path"])
        self._metadata = metadata(
            length=len(data.get("friends")), path=self.path  # type: ignore
        )
        return data
