import logging
from typing import Any, Callable


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
                    f"The following error happened while executing "
                    f"the command `{cmd}`: {e}"
                )
        return data

    def register_command(self, func: Callable, *args: Any, **kwargs: Any):
        cmd = Command(func, *args, **kwargs)
        self.commands.append(cmd)


class Command:
    def __init__(self, cmd, *args: Any, **kwargs: Any):
        self._cmd = cmd
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args: Any):
        return self._cmd(*(args + self._args), **self._kwargs)
