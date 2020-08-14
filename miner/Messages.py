from datetime import datetime
import pandas as pd
import os

from miner.FacebookData import FacebookData
from miner import utils


class Messages(FacebookData):
    def __init__(self, json_path):
        super().__init__(json_path)
        self.to_df('messages')
        self.set_date_as_index()
        self.add_partner_column()

    @property
    def names(self):
        # TODO ugly
        try:
            return pd.DataFrame(self.participants)[0]
        except KeyError:
            return pd.Series({0: 'Facebook User'})

    @property
    def participants(self):
        participants = self.decoded.get('participants')
        # TODO I should be IN
        # but this breaks stuff at TestMessagingAnalyzer
        return [p.get('name') for p in participants if p.get('name') != 'Levente Csőke']
        # return [p.get('name') for p in participants if p.get('name')]

    @property
    def title(self):
        return self.decoded.get('title')

    @property
    def ttype(self):
        return self.decoded.get('thread_type')

    @property
    def messages_dir(self):
        thread_path = self.decoded.get('thread_path')
        if not thread_path.startswith('inbox/'):
            raise ValueError('Field `thread_path` should start with `inbox/`.')
        return thread_path.split('inbox/')[1]

    @property
    def media_dir(self):
        for media in utils.MEDIA_DIRS:
            if media in self._df.columns:
                media_in_msg = list(self._df[media][self._df[media].notnull()])
                uri = media_in_msg[0][0].get('uri')
                return os.path.dirname(os.path.dirname(uri)).split('inbox/')[1]

    def set_date_as_index(self):
        date_series = self._df.timestamp_ms.apply(self.ts_to_date)
        self._df = self._df.set_index(date_series).iloc[::-1]

    def add_partner_column(self):
        self._df['partner'] = self.title

    @staticmethod
    def ts_to_date(date):
        return datetime.fromtimestamp(date / 1000)
