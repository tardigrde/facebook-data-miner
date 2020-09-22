from typing import Any
import logging


class CommandChainCreator:
    def __init__(self):
        self.commands = []

    def __call__(self, data: Any) -> Any:
        for cmd in self.commands:
            try:
                data = cmd(data)
            except Exception as e:
                logging.exception(e)
                logging.error(
                    f"The following error happened while executing the command `{cmd}`: {e}"
                )
        return data

    def register_command(self, func, *args, **kwargs):
        cmd = Command(func, *args, **kwargs)
        self.commands.append(cmd)


class Command:
    def __init__(self, cmd, *args, **kwargs):
        self._cmd = cmd
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args):
        return self._cmd(*(args + self._args), **self._kwargs)
