#!/usr/bin/env python3
# Run as: ./tests.py

import bot  # check whether the file parses
import logic
import msg  # check keyset
import unittest


class TestFormatSeconds(unittest.TestCase):
    def test_manual(self):
        test_data = [
            (0, "0s"),
            (1, "1s"),
            (59, "59s"),
            (60, "1min"),
            (61, "1min 1s"),
            (90, "1min 30s"),
            (120, "2min"),
            (121, "2min 1s"),
            (300, "5min"),
            (301, "5min 1s"),
            (330, "5min 30s"),
            (599, "9min 59s"),
            (600, "10min"),
            (601, "10min 1s"),
            (3599, "59min 59s"),
            (3600, "1h 0min"),
            (3601, "1h 0min 1s"),
            (3660, "1h 1min"),
            (3661, "1h 1min 1s"),
            (3720, "1h 2min"),
            (10799, "2h 59min 59s"),
            (10800, "3h 0min"),
            (10801, "3h 0min 1s"),
            (86399, "23h 59min 59s"),
            (86400, "1d 0h 0min"),
            (86401, "1d 0h 0min 1s"),
            (86460, "1d 0h 1min"),
            (90000, "1d 1h 0min"),
            (90060, "1d 1h 1min"),
            (90120, "1d 1h 2min"),
            (604800, "7d 0h 0min"),
        ]
        for i, (value, expected) in enumerate(test_data):
            with self.subTest(entry_number=i, value=value):
                actual = logic.format_seconds(value)
                self.assertEqual(actual, expected)


class TestSequences(unittest.TestCase):
    def check_sequence(self, sequence):
        room = logic.Room()
        for i, (query, expected_response) in enumerate(sequence):
            with self.subTest(step=i):
                actual_response = logic.handle(room, *query)
                self.assertEqual(expected_response, actual_response, query)
                self.assertIn(expected_response[0], msg.MESSAGES.keys())
                if expected_response == actual_response and expected_response[0] in msg.MESSAGES.keys():
                    template_list = msg.MESSAGES[expected_response[0]]
                    self.assertTrue(template_list, expected_response[0])
                    # Check that all templates all work:
                    for template in template_list:
                        self.assertTrue(template.format(*expected_response[1:]), (template, expected_response))
        d = room.to_dict()
        room2 = logic.Room.from_dict(d)
        d2 = room2.to_dict()
        self.assertEqual(d, d2)

    def test_empty(self):
        self.check_sequence([])

    def test_invalid(self):
        self.check_sequence([
            (('asdf', '', 'fina', 'usna'), ('unknown_command', 'fina')),
        ])

    def test_unknown_command(self):
        self.check_sequence([
            (('unknown_command', '', 'fina', 'usna'), ('unknown_command', 'fina')),
        ])

    def test_neu(self):
        self.check_sequence([
            (('neu', '', 'fina', 'usna'), ('neu_anonym', 'fina')),
            (('neu', 'foobar', 'fina', 'usna'), ('neu', 'foobar', 'fina')),
            (('neu', '', 'fina', 'usna'), ('existiert_anonym', 0, 'fina')),
            (('neu', 'foobar', 'fina', 'usna'), ('existiert', 'foobar', 0, 'fina')),
            (('neu', 'quux', 'fina', 'usna'), ('neu', 'quux', 'fina')),
        ])


if __name__ == '__main__':
    unittest.main()
