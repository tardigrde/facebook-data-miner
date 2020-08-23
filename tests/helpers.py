import tempfile
import os


def lower_string(string):
    return string.lower()


def add_string(string, addition=''):
    return string + addition


def split_string(string):
    return string.split()


def tempfile_tree():
    file_names = []

    for _ in range(5):
        f_handle = tempfile.NamedTemporaryFile(delete=False)
        os.rename(f_handle.name, f'{f_handle.name}.json')
        file_names.append(f'{f_handle.name}.json')
    return file_names
