from miner.utils import utils


class ProfileInformation:
    """
    Class for storing basic data about the user
    """

    def __init__(self, path):
        self.path = path + "/profile_information/profile_information.json"
        self.data = self.read()

    @property
    def name(self):
        return self.data.get("profile").get("name").get("full_name")

    @property
    def registration_timestamp(self):
        return utils.ts_to_date(self.data.get("profile").get("registration_timestamp"))

    def read(self):
        return utils.decode_data(utils.read_json(self.path), utils.utf8_decoder)
