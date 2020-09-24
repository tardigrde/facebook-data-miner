import os

from fire import Fire

from miner.app import App

DATA_PATH = f"{os.getcwd()}/tests/test_data"

if __name__ == "__main__":
    app = App(DATA_PATH)
    Fire(app, name="Facebook Data Miner")
