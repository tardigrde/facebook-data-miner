import pandas as pd
from pathlib import Path
from utils import read_json, decode_text, accents_map


class FacebookData:
    def __init__(self, json_path):
        self.json_path = json_path
        self._df = None

    @property
    def df(self):
        return self._df

    @property
    def decoded(self):
        return decode_text(self.json)

    @property
    def json(self):
        return read_json(self.json_path)

    @property
    def compact_names(self):
        # NOTE this is the place where we change pd/np to builtin
        # do we have to do this?
        name_list = list(self.without_accent_and_whitespace(self.lower_names(self.names)))
        return name_list[0] if len(name_list) == 1 else name_list

    @staticmethod
    def lower_names(col):
        return col.str.lower()

    @staticmethod
    def without_accent_and_whitespace(col):
        def replace_accents(text):
            for char in accents_map.keys():
                if char in text:
                    text = text.replace(char, accents_map[char])
            return text.replace(' ', '')

        return col.apply(replace_accents)
