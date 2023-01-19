#!/usr/bin/env python3
# Run as: ./tests.py

import bot  # check whether the file parses
import logic
import msg  # check keyset
import unittest


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


if __name__ == '__main__':
    unittest.main()
