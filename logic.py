#!/bin/false
# Not for execution

import datetime

DATETIME_FORMAT = '%Y-%m-%d %T'


class Room:
    def __init__(self):
        self.init_datetime = datetime.datetime.now()

    def to_dict(self):
        return dict(
            init_datetime=self.init_datetime.timestamp(),
        )

    def from_dict(d):
        r = Room()
        r.init_datetime = datetime.datetime.fromtimestamp(d['init_datetime'])
        return r

    def __repr__(self):
        return str(self.to_dict())


def compute_uptime(room, argument, sender_firstname, sender_username) -> None:
    return ('uptime', room.init_datetime.strftime(DATETIME_FORMAT), datetime.datetime.now().strftime(DATETIME_FORMAT))


def handle(room, command, argument, sender_firstname, sender_username):
    if command == 'uptime':
        return compute_uptime(room, argument, sender_firstname, sender_username)
    else:
        return ('unknown_command', sender_firstname)
