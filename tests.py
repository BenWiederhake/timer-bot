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
        for i, (int_value, str_value) in enumerate(test_data):
            with self.subTest(entry_number=i, value=int_value, type="format"):
                actual = logic.format_seconds(int_value)
                self.assertEqual(actual, str_value)
            with self.subTest(entry_number=i, value=str_value, type="parse"):
                actual = logic.parse_seconds(str_value.replace(" ", ""))
                self.assertEqual(actual, int_value)

    def test_parse_special(self):
        test_data = [
            ("0m0s", 0),
            ("1234s", 1234),
            ("90m", 5400),
            ("90min", 5400),
            ("1h30m", 5400),
            ("1h30min", 5400),
            ("0h", 0),
            ("1h", 3600),
            ("1h0s", 3600),
            ("-1s", None),
            ("1", None),
            ("+90", None),
            ("+90s", None),
            ("1h 30m", None),
        ]
        for i, (value, expected) in enumerate(test_data):
            with self.subTest(entry_number=i, value=value):
                actual = logic.parse_seconds(value)
                self.assertEqual(actual, expected)


class TestSequences(unittest.TestCase):
    SEEN_MESSAGES = set()

    @classmethod
    def tearDownClass(_cls):
        expected_keys = set(msg.MESSAGES.keys())
        extraneous_keys = expected_keys.difference(TestSequences.SEEN_MESSAGES)
        assert not extraneous_keys, extraneous_keys

    def check_sequence(self, sequence):
        room = logic.Room()
        for i, (query, expected_response) in enumerate(sequence):
            TestSequences.SEEN_MESSAGES.add(expected_response[0])
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

    def test_uptime(self):
        # Returned text depends on the current time.
        room = logic.Room()
        TestSequences.SEEN_MESSAGES.add("uptime")
        actual_response = logic.handle(room, "uptime", "", "fina", "usna")
        self.assertEqual(3, len(actual_response), actual_response)
        self.assertEqual("uptime", actual_response[0], actual_response)
        self.assertEqual(19, len(actual_response[1]), actual_response)
        self.assertEqual(19, len(actual_response[2]), actual_response)
        template_list = msg.MESSAGES["uptime"]
        self.assertTrue(template_list)
        # Check that all templates all work:
        for template in template_list:
            self.assertTrue(template.format(*actual_response[1:]), (template, actual_response))
        d = room.to_dict()
        room2 = logic.Room.from_dict(d)
        d2 = room2.to_dict()
        self.assertEqual(d, d2)

    def test_unknown_command(self):
        self.check_sequence([
            (('unknown_command', '', 'fina', 'usna'), ('unknown_command', 'fina')),
        ])

    def test_neu(self):
        self.check_sequence([
            (('neu', '', 'fina', 'usna'), ('neu_anonym', 'fina')),
            (('neu', 'foobar', 'fina', 'usna'), ('neu', 'foobar', 'fina')),
            (('neu', '', 'fina', 'usna'), ('existiert_anonym', '0s', 'fina')),
            (('neu', 'foobar', 'fina', 'usna'), ('existiert', 'foobar', '0s', 'fina')),
            (('neu', 'quux', 'fina', 'usna'), ('neu', 'quux', 'fina')),
        ])

    def test_zeige_anonym(self):
        self.check_sequence([
            (('zeige', '', 'fina', 'usna'), ('zeige_missing_anonym', 'fina')),
            (('neu', '', 'fina', 'usna'), ('neu_anonym', 'fina')),
            (('zeige', '', 'fina', 'usna'), ('zeige_anonym', '0s', 'fina')),
            # TODO: Add some time, then output again
        ])

    def test_zeige_specific(self):
        self.check_sequence([
            (('zeige', 'foo', 'fina', 'usna'), ('zeige_missing', 'foo', 'fina')),
            (('neu', 'bar', 'fina', 'usna'), ('neu', 'bar', 'fina')),
            (('zeige', 'foo', 'fina', 'usna'), ('zeige_missing', 'foo', 'fina')),
            (('neu', 'foo', 'fina', 'usna'), ('neu', 'foo', 'fina')),
            (('zeige', 'foo', 'fina', 'usna'), ('zeige', 'foo', '0s', 'fina')),
            # TODO: Add some time, then output again
        ])

    def test_plus_anonym(self):
        self.check_sequence([
            (('plus', '', 'fina', 'usna'), ('modify_noarg', 'fina')),
            (('plus', '1h', 'fina', 'usna'), ('modify_missing_anonym', 'fina')),
            (('neu', '', 'fina', 'usna'), ('neu_anonym', 'fina')),
            (('plus', '1h', 'fina', 'usna'), ('plus_anonym', '1h 0min', '1h 0min', 'fina')),
            (('plus', '1h', 'fina', 'usna'), ('plus_anonym', '1h 0min', '2h 0min', 'fina')),
            (('plus', '3600s', 'fina', 'usna'), ('plus_anonym', '1h 0min', '3h 0min', 'fina')),
            (('plus', '59m60s', 'fina', 'usna'), ('plus_anonym', '1h 0min', '4h 0min', 'fina')),
        ])

    def test_plus_specific(self):
        self.check_sequence([
            (('plus', 'x', 'fina', 'usna'), ('modify_invalid_onearg', 'x', 'fina')),
            (('neu', 'x', 'fina', 'usna'), ('neu', 'x', 'fina')),
            (('plus', 'x 1h', 'fina', 'usna'), ('plus', 'x', '1h 0min', '1h 0min', 'fina')),
            (('plus', 'x 1h', 'fina', 'usna'), ('plus', 'x', '1h 0min', '2h 0min', 'fina')),
            (('plus', 'x 3600s', 'fina', 'usna'), ('plus', 'x', '1h 0min', '3h 0min', 'fina')),
            (('plus', 'x 59m60s', 'fina', 'usna'), ('plus', 'x', '1h 0min', '4h 0min', 'fina')),
        ])

    def test_plus_invalid(self):
        self.check_sequence([
            (('neu', 'x', 'fina', 'usna'), ('neu', 'x', 'fina')),
            (('plus', 'x y', 'fina', 'usna'), ('modify_invalid_twoarg', 'y', 'fina')),
            (('plus', 'x 1h', 'fina', 'usna'), ('plus', 'x', '1h 0min', '1h 0min', 'fina')),
            (('plus', 'x 1h1h', 'fina', 'usna'), ('modify_invalid_twoarg', '1h1h', 'fina')),
        ])

    def test_plus_invalid_anonym(self):
        self.check_sequence([
            (('neu', '', 'fina', 'usna'), ('neu_anonym', 'fina')),
            (('plus', 'y', 'fina', 'usna'), ('modify_invalid_onearg', 'y', 'fina')),
            (('plus', '1h', 'fina', 'usna'), ('plus_anonym', '1h 0min', '1h 0min', 'fina')),
            (('plus', '1h1h', 'fina', 'usna'), ('modify_invalid_onearg', '1h1h', 'fina')),
        ])

    def test_minus_anonym(self):
        self.check_sequence([
            (('minus', '', 'fina', 'usna'), ('modify_noarg', 'fina')),
            (('minus', '1h', 'fina', 'usna'), ('modify_missing_anonym', 'fina')),
            (('neu', '', 'fina', 'usna'), ('neu_anonym', 'fina')),
            (('minus', '1h', 'fina', 'usna'), ('minus_anonym', '1h 0min', '0s', 'fina')),
            (('plus', '10h', 'fina', 'usna'), ('plus_anonym', '10h 0min', '10h 0min', 'fina')),
            (('minus', '1h', 'fina', 'usna'), ('minus_anonym', '1h 0min', '9h 0min', 'fina')),
            (('minus', '3600s', 'fina', 'usna'), ('minus_anonym', '1h 0min', '8h 0min', 'fina')),
            (('minus', '59m60s', 'fina', 'usna'), ('minus_anonym', '1h 0min', '7h 0min', 'fina')),
        ])

    def test_minus_specific(self):
        self.check_sequence([
            (('minus', 'x', 'fina', 'usna'), ('modify_invalid_onearg', 'x', 'fina')),
            (('neu', 'x', 'fina', 'usna'), ('neu', 'x', 'fina')),
            (('minus', 'x 1h', 'fina', 'usna'), ('minus', 'x', '1h 0min', '0s', 'fina')),
            (('plus', 'x 10h', 'fina', 'usna'), ('plus', 'x', '10h 0min', '10h 0min', 'fina')),
            (('minus', 'x 1h', 'fina', 'usna'), ('minus', 'x', '1h 0min', '9h 0min', 'fina')),
            (('minus', 'x 3600s', 'fina', 'usna'), ('minus', 'x', '1h 0min', '8h 0min', 'fina')),
            (('minus', 'x 59m60s', 'fina', 'usna'), ('minus', 'x', '1h 0min', '7h 0min', 'fina')),
        ])

    def test_minus_invalid(self):
        self.check_sequence([
            (('neu', 'x', 'fina', 'usna'), ('neu', 'x', 'fina')),
            (('minus', 'x y', 'fina', 'usna'), ('modify_invalid_twoarg', 'y', 'fina')),
            (('minus', 'x 1h', 'fina', 'usna'), ('minus', 'x', '1h 0min', '0s', 'fina')),
            (('minus', 'x 1h1h', 'fina', 'usna'), ('modify_invalid_twoarg', '1h1h', 'fina')),
        ])

    def test_minus_invalid_anonym(self):
        self.check_sequence([
            (('neu', '', 'fina', 'usna'), ('neu_anonym', 'fina')),
            (('minus', 'y', 'fina', 'usna'), ('modify_invalid_onearg', 'y', 'fina')),
            (('minus', '1h', 'fina', 'usna'), ('minus_anonym', '1h 0min', '0s', 'fina')),
            (('minus', '1h1h', 'fina', 'usna'), ('modify_invalid_onearg', '1h1h', 'fina')),
        ])

    def test_minus_fractional(self):
        self.check_sequence([
            (('neu', '', 'fina', 'usna'), ('neu_anonym', 'fina')),
            (('plus', '37m', 'fina', 'usna'), ('plus_anonym', '37min', '37min', 'fina')),
            (('minus', '18min', 'fina', 'usna'), ('minus_anonym', '18min', '19min', 'fina')),
            (('minus', '22min', 'fina', 'usna'), ('minus_anonym', '22min', '0s', 'fina')),
        ])

    def test_help(self):
        self.check_sequence([
            (('help', '', 'fina', 'usna'), ('help', 'fina')),
        ])


if __name__ == '__main__':
    unittest.main()
