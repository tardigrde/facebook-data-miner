from datetime import datetime
from typing import Union, List, Dict

from miner.utils import utils


class ProfileInformation:
    """
    Class for reading and storing profile information about the user.
    """

    def __init__(self, path: str):
        self.path = path + "/profile_information/profile_information.json"
        self.data = self._read()

    @property
    def name(self) -> str:
        """

        @return: name of the user.
        """
        return self.data.get("profile").get("name").get("full_name")

    @property
    def registration_timestamp(self) -> datetime:
        """

        @return: the date when the user registered to Facebook.
        """

        return utils.ts_to_date(self.data.get("profile").get("registration_timestamp"))

    def _read(self) -> Union[str, List, Dict]:
        return utils.decode_data(utils.read_json(self.path), utils.utf8_decoder)
