#!/home/levente/anaconda3/envs/fb/bin/python
# TODO change hashbang

import logging
import traceback
from typing import List, Union

from fire import Fire

from miner.app import App
from miner.cli_adapters import AnalyzerFacade, GenericAnalyzerFacade
from miner.visualizer.plotter import Plotter
from miner.visualizer.table_creator import TableCreator

DATA_PATH = None


class CLI:
    def __init__(self, app):
        self._app = app

    def friends(self, sort="date", dates=True, output=None):
        """


        @param sort: a
        @param dates: b
        @param output: c
        @return: list of friends, sorted by @sort, with dates of making friend if @dates is True,
        saved in a csv or json file if @output is a valid path.
        """
        return self._app.friends.get(sort=sort, dates=dates, output=output)

    def conversations(
        self,
        kind: str = "private",
        channels: str = None,
        cols: List[str] = None,
        output: str = None,
    ):
        """

        @param kind:
        @param channels:
        @param cols:
        @param output:
        @return:
        """
        return self._app.conversations.get(
            kind=kind, channels=channels, cols=cols, output=output
        )

    def analyzer(
        self,
        kind: str = None,
        channels: str = None,
        participants: str = None,
        senders: str = None,
        **kwargs,
    ) -> Union[GenericAnalyzerFacade, AnalyzerFacade]:
        if kind is None:
            return GenericAnalyzerFacade(self._app.analyzer)
        return AnalyzerFacade(
            self._app.analyzer,
            kind=kind,
            channels=channels,
            participants=participants,
            senders=senders,
            **kwargs,
        )

    def people(self):
        return self._app.people.get()

    def report(self) -> TableCreator:
        return TableCreator(self._app.analyzer, self._app.config)

    def plot(self) -> Plotter:
        # NOTE saving images to output is yet to be implemented
        return Plotter(self._app.analyzer, self._app.config)


def main(path: str = DATA_PATH):
    global DATA_PATH
    DATA_PATH = path

    if not DATA_PATH:
        return "You need to provide a path variable."


if __name__ == "__main__":
    # Fire(app, name="Facebook-Data-Miner")
    # TODO this is always created in every cli call
    try:
        app = App()
        Fire(CLI(app), name="Facebook-Data-Miner")

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logging.error(f"An exception has happened:\n{e}")
