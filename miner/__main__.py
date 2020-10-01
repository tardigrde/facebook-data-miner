import logging
import traceback

from fire import Fire

from miner.app import App
from miner.cli import CLI

if __name__ == "__main__":
    try:
        app = App()
        Fire(CLI(app), name="Facebook-Data-Miner")

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logging.error(f"An exception has happened:\n{e}")
