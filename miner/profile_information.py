import os
from datetime import datetime
from typing import Any, Union

import pytz

from miner.utils import const, utils


class ProfileInformation:
    """
    Class for reading and storing profile information about the user.
    """

    def __init__(self, path: str):
        self.path = os.path.join(path, *const.PROFILE_INFORMATION_PATH)
        self.data: Any = self._read()

    @property
    def name(self) -> Union[str, None]:
        """

        @return: name of the user.
        """
        return self.data.get("profile").get("name").get("full_name")

    @property
    def registration_timestamp(self) -> Union[None, datetime]:
        """

        @return: the date when the user registered to Facebook.
        """

        return utils.ts_to_date(
            self.data.get("profile").get("registration_timestamp"), tz=pytz.UTC
        )

    def _read(self) -> Any:
        return utils.decode_data(
            utils.read_json(self.path), utils.utf8_decoder
        )
