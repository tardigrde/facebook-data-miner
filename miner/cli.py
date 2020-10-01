#!/usr/bin/env python


import logging
import traceback
from typing import Any, List, Union

from fire import Fire

from miner.app import App
from miner.cli_adapters import (
    MessagingAnalyzerFacade,
    MessagingAnalyzerManagerFacade,
)
from miner.visualizer.plotter import Plotter
from miner.visualizer.table_creator import TableCreator

DATA_PATH = None


class CLI:
    """
    Entrypoint for the Command-Line Interface.
    """

    def __init__(self, app: App) -> None:
        self._app = app

    def friends(
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
        return self._app.friends.get(sort=sort, dates=dates, output=output)

    def conversations(
        self,
        kind: str = "private",
        channels: Union[str, None] = None,
        cols: Union[List[str], None] = None,
        output: Union[str, None] = None,
    ) -> str:
        """
        Conversations.

        @param kind: one of private or group,
        depending on which messaging do you want to analyze.
        @param channels: channel names you want to filter for.
        @param cols: column names you want to include in the output.
        @param output: where do we want to write the return value,
        can be any of: {csv|json|/some/path.{json|csv}}.
        @return: either the data formatted as csv or json,
        or a success message about where was the data saved.
        """
        return self._app.conversations.get(
            kind=kind, channels=channels, cols=cols, output=output
        )

    def analyzer(
        self,
        kind: Union[str, None] = None,
        channels: Union[str, None] = None,
        participants: Union[str, None] = None,
        senders: Union[str, None] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Messaging analyzer.

        @param kind: one of private or group,
        depending on which messaging do you want to analyze.
        @param channels: channel names you want to filter for.
        @param participants: participant names you want to filter for.
        @param senders: sender names you want to filter for.
        @param kwargs: further filtering parameters, can be start,
        end and/or period.
        @return: exposed function from one of
        {MessagingAnalyzerManagerFacade|MessagingAnalyzerFacade}.
        """
        if kind is None:
            return MessagingAnalyzerManagerFacade(self._app.analyzer)
        return MessagingAnalyzerFacade(
            self._app.analyzer,
            kind=kind,
            channels=channels,
            participants=participants,
            senders=senders,
            **kwargs,
        )

    def people(self) -> str:
        """
        Exposed function for getting data on people.

        @param output: where do we want to write the return value,
        can be any of: {csv|json|/some/path.{json|csv}}.
        @return: either the data formatted as csv or json,
        or a success message about where was the data saved.
        """
        return self._app.people.get()

    def report(self) -> Any:
        """

        @return: a TableCreator instance's exposed methods.
        """
        return TableCreator(self._app.analyzer, self._app.config)

    def plot(self) -> Any:
        """

        @return: a Plotter instance's exposed methods.
        """
        # NOTE saving images to output is yet to be implemented
        return Plotter(self._app.analyzer, self._app.config)


if __name__ == "__main__":
    # Fire(app, name="Facebook-Data-Miner")
    # TODO this is always created in every cli call
    try:
        app = App()
        Fire(CLI(app), name="Facebook-Data-Miner")

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logging.error(f"An exception has happened:\n{e}")
