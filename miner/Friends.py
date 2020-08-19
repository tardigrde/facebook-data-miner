from miner.FacebookData import  FacebookData
from miner import utils
import pandas as pd
from typing import Union, List, Dict, Callable, Any

# TODO all the other jsons whic are in friends as subclasses
class Friends(FacebookData):
    sub_path = 'friends'

    def __init__(self, path: str, reader: Callable = None, processors: List[Callable] = None) -> None:
        self.path: str = path
        self._reader: Callable = reader
        self._processors: List[Callable] = processors
        super().__init__()

    @property
    def reader(self) -> Callable:
        return utils.read_json if not self._reader else self._reader

    @property
    def processors(self) -> Any:
        if self._processors:
            return self._processors
        return [self.decode_text, self.get_dataframe]


    @staticmethod
    def get_dataframe(data: Dict) -> pd.DataFrame:
        return pd.DataFrame(data.get('friends'), columns=['name', 'timestamp'])



# class Friends(TabularFacebookData):
#     """
#     Class for storing data in friends.json
#     """
#
#     def __init__(self, *args):
#         super().__init__(*args)
#         self.to_df('friends')
#
#     def get_people(self, name=None):
#         # TODO make this iterable
#         names = {}
#         for full_name, compact in zip(self.names, self.compact_names):
#             if name is not None and name != full_name:  # filtering for name
#                 continue
#             names[full_name] = Individual(
#                 name=full_name,
#                 compact=compact,
#                 friend=True,
#             )
#         return names
#
#     @property
#     def names(self):
#         return self.df.name
