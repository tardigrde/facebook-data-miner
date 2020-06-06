import unittest
from utils import *
from pathlib import Path
import reusables
from reusables.cli import *


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.test_data_path = Path(f'{pwd()}/test_data')

    def test_read_json(self):
        dummy1 = {'0': 'a', '2': 'c'}
        dummy1_path = Path(self.test_data_path / 'dummy1.json')
        dump_to_json(file=dummy1_path, data=dummy1)

        dummy2 = {'1': 'b', '3': 'd'}
        dummy2_path = Path(self.test_data_path / 'dummy2.json')
        dump_to_json(file=dummy2_path, data=dummy2)

        dummy_unified = get_messages(dummy1_path, dummy2_path)
        expected = {'0': 'a', '1': 'b', '2': 'c', '3': 'd'}

        self.assertDictEqual(expected, dummy_unified)

        dummy1_path.unlink()
        dummy2_path.unlink()

    def test_decode_text(self):
        dummy = {'0': '\u00c5\u0091', '1': '\u00c3\u00a1', '2': ['\u00c5\u0091', {'0': '\u00c3\u00a1'}],
                 '3': {'0': '\u00c5\u0091'}}
        dummy_path = Path(self.test_data_path / 'dummy.json')
        dump_to_json(file=dummy_path, data=dummy)
        read = get_messages(dummy_path, decode=True)
        expected = {'0': 'ő', '1': 'á', '2': ['ő', {'0': 'á'}],
                    '3': {'0': 'ő'}}
        self.assertEqual(expected, read)

        dummy_path.unlink()

    def later_tests(self):
        data = {'participants': [{'name': 'Csőke Boglárka'}, {'name': 'Levente Csőke'}],
                'title': 'Csőke Boglárka',
                'is_still_participant': True,
                'thread_type': 'Regular',
                'thread_path': 'inbox/CsokeBoglarka_5A48Zi9P1w',
                'messages': [...]}
        msg_element = {'sender_name': 'Levente Csőke',
                       'timestamp_ms': 1440948801592,
                       'content': 'ahaa',
                       'type': 'Generic'}

    def test_read_real_data(self):
        bogi_msg = Path('/home/levente/projects/facebook-data-miner/data/messages/inbox/csokeboglarka_5a48zi9p1w')
        data = get_messages(bogi_msg/'message_1.json', bogi_msg/'message_2.json')
        msg = data['messages']