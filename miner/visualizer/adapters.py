from typing import List, Dict, Tuple

import numpy as np
import pandas as pd

from miner.message.conversation_stats import ConversationStats
from miner.utils import utils, const, decorators


# TODO make this somehow more generic
def outputter(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)

        if not len(res):
            return
        return utils.df_to_file(kwargs.get("output"), res)

    return wrapper


class GenericAnalyzerFacade:
    def __init__(self, analyzer):
        self._analyzer = analyzer
        self._private = self._analyzer.private
        self._group = self._analyzer.group
        pass

    def people_i_have_private_convo_with(self) -> List[str]:
        return self._analyzer.people_i_have_private_convo_with

    def people_i_have_group_convo_with(self) -> List[str]:
        return self._analyzer.people_i_have_group_convo_with

    def get_who_i_have_private_convo_with_from_a_group(
        self, group_name: str
    ) -> List[str]:
        return self._analyzer.get_who_i_have_private_convo_with_from_a_group(
            group_name=group_name
        )

    def how_much_i_speak_in_private_with_group_members(
        self, group_name: str
    ) -> Dict[str, int]:
        return self._analyzer.how_much_i_speak_in_private_with_group_members(
            group_name=group_name
        )

    def is_priv_msg_first_then_group(self, name: str) -> bool:
        return self._analyzer.is_priv_msg_first_then_group(name=name)


class AnalyzerFacade:
    @decorators.kind_checker
    def __init__(
        self,
        analyzer,
        kind: str = "private",
        channels="",
        participants="",
        senders="",
        start=None,
        end=None,
        period=None,
    ):
        self.__analyzer = getattr(analyzer, kind).filter(
            channels=channels, participants=participants
        )
        self.__stats = self._analyzer.stats.filter(
            channels=channels, senders=senders, start=start, end=end, period=period
        )

    def __repr__(self):
        return "AnalyzerFacade"

    @property
    def _analyzer(self):
        return self.__analyzer

    @property
    def _stats(self):
        return self.__stats

    def is_group(self) -> bool:
        return self._analyzer.is_group

    def group_convo_map(self) -> Dict[str, List[str]]:
        return self._analyzer.group_convo_map

    def number_of_convos_created_by_me(self) -> int:
        return self._analyzer.number_of_convos_created_by_me

    def participants(self) -> List[str]:
        return self._analyzer.participants

    def max_channel_size(self) -> int:
        return self._analyzer.max_channel_size

    def mean_channel_size(self) -> int:
        return self._analyzer.mean_channel_size

    def min_channel_size(self) -> int:
        return self._analyzer.min_channel_size

    def all_channels(self, name: str = None) -> List[str]:
        """

        @param name: a partner name.
        @return: all channels for this partner (private and groups).
        """
        if not name:
            return self.channels()
        return self._analyzer.get_all_channels_for_one_person(name)

    def ranking_by_statistic(
        self, by="mc", ranking="percent", top=20
    ) -> Dict[str, float]:
        return self._analyzer.get_ranking_of_senders_by_convo_stats(
            statistic=by, top=top
        ).get(ranking)

    ##########################################################################

    def channels(self) -> List[str]:
        return self._stats.channels

    def number_of_channels(self) -> int:
        return self._stats.number_of_channels

    def contributors(self) -> List[str]:
        """
        @return:
        """
        return self._stats.contributors

    def number_of_contributors(self) -> int:
        return self._stats.number_of_contributors

    def creator(self) -> str:
        return self._stats.creator

    def created_by_me(self) -> bool:
        return self._stats.created_by_me

    def start(self) -> np.datetime64:
        return self._stats.start

    def end(self) -> np.datetime64:
        return self._stats.end

    @outputter
    def messages(self, output: str = None) -> pd.Series:
        return self._stats.messages

    @outputter
    def text(self, output: str = None) -> pd.Series:
        return self._stats.text  # TODO

    @outputter
    def media(self, output: str = None) -> pd.Series:
        return self._stats.media

    @outputter
    def words(self, output: str = None) -> pd.Series:
        return self._stats.words

    def mc(self) -> int:
        return self._stats.mc

    def wc(self) -> int:
        return self._stats.wc

    def cc(self) -> int:
        return self._stats.cc

    def text_mc(self) -> int:
        return self._stats.text_mc

    def media_mc(self) -> int:
        return self._stats.media_mc

    def unique_mc(self) -> int:
        return self._stats.unique_mc

    def unique_wc(self) -> int:
        return self._stats.unique_wc

    def percentage_of_text_messages(self) -> float:
        return self._stats.percentage_of_text_messages

    def percentage_of_media_messages(self) -> float:
        return self._stats.percentage_of_media_messages

    @outputter
    def most_used_msgs(self, output: str = None) -> pd.Series:
        return self._stats.most_used_msgs

    @outputter
    def most_used_words(self, output: str = None) -> pd.Series:
        return self._stats.most_used_words

    @outputter
    def reacted_messages(self, output: str = None) -> pd.DataFrame:
        return self._stats.reacted_messages

    @outputter
    def files(self, output: str = None) -> pd.Series:
        return self._stats.files

    @outputter
    def photos(self, output: str = None) -> pd.Series:
        return self._stats.photos

    @outputter
    def videos(self, output: str = None) -> pd.Series:
        return self._stats.videos

    @outputter
    def audios(self, output: str = None) -> pd.Series:
        return self._stats.audios

    @outputter
    def gifs(self, output: str = None) -> pd.Series:
        return self._stats.gifs

    def average_word_length(self):
        return self._stats.average_word_length

    def message_language_map(self):
        """
        TODO better error handling
        TODO better
        WARNING:polyglot.detect.base:Detector is not able to detect the language reliably.
        WARNING:polyglot.detect.base:Detector is not able to detect the language reliably.
        WARNING:polyglot.detect.base:Detector is not able to detect the language reliably.
        WARNING:polyglot.detect.base:Detector is not able to detect the language reliably.
        WARNING:polyglot.detect.base:Detector is not able to detect the language reliably.
        WARNING:polyglot.detect.base:Detector is not able to detect the language reliably.
        WARNING:polyglot.detect.base:Detector is not able to detect the language reliably.
        test:                            Prediction is reliable: False Language 1: name: English     code: en       confidence:  83.0 read bytes:  1228 Language 2: name: un          code: un       confidence:   0.0 read bytes:     0 Language 3: name: un          code: un       confidence:   0.0 read bytes:     0
        what do you test:                Prediction is reliable: True Language 1: name: English     code: en       confidence:  94.0 read bytes:  2048 Language 2: name: un          code: un       confidence:   0.0 read bytes:     0 Language 3: name: un          code: un       confidence:   0.0 read bytes:     0
        basic group messages:            Prediction is reliable: True Language 1: name: English     code: en       confidence:  95.0 read bytes:  1511 Language 2: name: un          code: un       confidence:   0.0 read bytes:     0 Language 3: name: un          code: un       confidence:   0.0 read bytes:     0
        blabla:                          Prediction is reliable: False Language 1: name: French      code: fr       confidence:  87.0 read bytes:  1462 Language 2: name: un          code: un       confidence:   0.0 read bytes:     0 Language 3: name: un          code: un       confidence:   0.0 read bytes:     0
        ok:                              null
        marathon?:                       Prediction is reliable: False Language 1: name: Hungarian   code: hu       confidence:  90.0 read bytes:   455 Language 2: name: un          code: un       confidence:   0.0 read bytes:     0 Language 3: name: un          code: un       confidence:   0.0 read bytes:     0
        yapp yapp :D:                    Prediction is reliable: False Language 1: name: Wolof       code: wo       confidence:  92.0 read bytes:   341 Language 2: name: un          code: un       confidence:   0.0 read bytes:     0 Language 3: name: un          code: un       confidence:   0.0 read bytes:     0
        You named the group marathon.:   Prediction is reliable: True Language 1: name: English     code: en       confidence:  96.0 read bytes:  1412 Language 2: name: un          code: un       confidence:   0.0 read bytes:     0 Language 3: name: un          code: un       confidence:   0.0 read bytes:     0
        i start today:                   Prediction is reliable: False Language 1: name: English     code: en       confidence:  93.0 read bytes:  1389 Language 2: name: un          code: un       confidence:   0.0 read bytes:     0 Language 3: name: un          code: un       confidence:   0.0 read bytes:     0
        we could go but running is free: Prediction is reliable: True Language 1: name: English     code: en       confidence:  96.0 read bytes:  1504 Language 2: name: un          code: un       confidence:   0.0 read bytes:     0 Language 3: name: un          code: un       confidence:   0.0 read bytes:     0
        hmmm:                            Prediction is reliable: False Language 1: name: English     code: en       confidence:  83.0 read bytes:   204 Language 2: name: un          code: un       confidence:   0.0 read bytes:     0 Language 3: name: un          code: un       confidence:   0.0 read bytes:     0
        :D:
        @return:
        """
        # TODO expose a higher level function here. like calculate the ratios
        return self._stats.message_language_map

    # TODO portion of reacted
    @outputter
    def media_message_extractor(self, media_type: str, output: str = None) -> pd.Series:
        # TODO do we need this????? we have them separately
        return self._stats.media_message_extractor(media_type)

    @outputter
    def get_grouped_time_series_data(
        self, period: str = "y", output: str = None
    ) -> pd.DataFrame:
        return self._stats.get_grouped_time_series_data(period=period)

    def stat_per_period(self, period: str, statistic: str = "mc") -> Dict:
        return self._stats.stat_per_period(period, statistic=statistic)


class DataAdapter:
    def __init__(self, analyzer, config):
        self.analyzer = analyzer
        self.config = config

    @property
    def private(self):
        return self.analyzer.private

    @property
    def group(self):
        return self.analyzer.group

    def get_private_stats(self, channels=None, senders=None, **kwargs):
        return self.private.filter(channels=channels, senders=senders).stats.filter(
            **kwargs
        )

    def get_group_stats(self, channels=None, senders=None, **kwargs):
        return self.group.filter(channels=channels, senders=senders).stats.filter(
            **kwargs
        )


class TableDataAdapter(DataAdapter):
    def __init__(self, analyzer, config):
        super().__init__(analyzer, config)

    def get_basic_stats(self, kind: str = "private"):
        stat_names = [
            "mc",
            "text_mc",
            "media_mc",
            "wc",
            "cc",
        ]
        titles = []
        stats = []
        for name in stat_names:
            readable = const.STAT_MAP.get(name)
            stat = getattr(getattr(self.analyzer, kind).stats, name)
            titles.append(readable)
            stats.append(stat)
        return titles, stats

    def get_unique_stats(self, kind: str = "private"):
        analyzer = getattr(self.analyzer, kind)
        return (
            ["Unique message", "Unique word"],
            [analyzer.stats.unique_mc, analyzer.stats.unique_wc,],
        )

    def get_stat_per_period_data(
        self, kind: str = "private", period: str = "y", stat: str = "mc"
    ):
        dates, counts = [""], [const.STAT_MAP.get(stat)]
        data = getattr(self.analyzer, kind).stats.stat_per_period(
            period, statistic=stat
        )
        for date, count in data.items():
            dates.append(date)
            counts.append(count)
        return dates, counts


class PlotDataAdapter(DataAdapter):
    """
    Class for adopting statistics data for Visualizer to use.
    """

    def __init__(self, analyzer, config):
        super().__init__(analyzer, config)

    def set_up_time_series_data(self, period, stat="text_mc", **kwargs):
        stats = self.analyzer.stats.filter(**kwargs)
        return stats.get_grouped_time_series_data(period)[stat]

    def get_time_series_data(
        self, kind: str = "private", period: str = "y", stat=None, **kwargs
    ):
        index, me, partner = self.get_stat_per_time_data(
            kind=kind, period=period, stat=stat, **kwargs
        )
        utils.generate_date_series(
            self.config.get("profile").registration_timestamp,
            period,
            start=index[0],
            end=index[-1],
        )

    def get_stat_per_time_data(
        self, kind: str = "private", period: str = "y", stat: str = "mc", **kwargs
    ):
        # TODO correct filtering
        analyzer = getattr(self.analyzer, kind)
        me_stat = analyzer.stats.filter(senders="me", **kwargs).stat_per_period(
            period, statistic=stat
        )
        partner_stat = analyzer.stats.filter(
            senders="partner", **kwargs
        ).stat_per_period(period, statistic=stat)
        return list(me_stat.keys()), list(me_stat.values()), list(partner_stat.values())

    def get_ranking_of_friends_by_message_stats(self, kind: str = "private", stat="mc"):
        analyzer = getattr(self.analyzer, kind)
        ranking = analyzer.get_ranking_of_senders_by_convo_stats(statistic=stat)
        sorted_dict = utils.sort_dict(
            ranking.get("count"), func=lambda item: item[1], reverse=True,
        )
        sliced_dict = (
            utils.slice_dict(sorted_dict, 20) if len(sorted_dict) > 20 else sorted_dict
        )
        cleared_dict = utils.remove_items_where_value_is_falsible(sliced_dict)

        df = pd.DataFrame(cleared_dict, index=[0])
        return list(df.columns), df.iloc[0]
