#!/bin/false
# Not for execution

import datetime
import re

DATETIME_FORMAT = '%Y-%m-%d %T'
SECONDS_PARSE_RE = re.compile('^(?:([0-9]+)d)?(?:([0-9]+)h)?(?:([0-9]+)m(?:in)?)?(?:([0-9]+)s)?$')


def format_seconds(value):
    secs_bare = value % 60
    value //= 60
    secs_needed = value == 0 or secs_bare > 0

    mins_needed = value > 0
    mins_bare = value % 60
    value //= 60

    hours_needed = value > 0
    hours_bare = value % 24
    value //= 24

    days_needed = value > 0
    days_bare = value

    parts = []

    if days_needed:
        parts.append(f"{days_bare}d")
    if hours_needed:
        parts.append(f"{hours_bare}h")
    if mins_needed:
        parts.append(f"{mins_bare}min")
    if secs_needed:
        parts.append(f"{secs_bare}s")

    return " ".join(parts)


def parse_seconds(argument):
    if not argument:
        return None  # Technically valid, but refuse it anyway.
    match = SECONDS_PARSE_RE.match(argument)
    if not match:
        return None
    g_d, g_h, g_m, g_s = match.groups()
    d = int(g_d) if g_d else 0
    h = int(g_h) if g_h else 0
    m = int(g_m) if g_m else 0
    s = int(g_s) if g_s else 0
    return ((d * 24 + h) * 60 + m) * 60 + s


class Room:
    def __init__(self):
        self.init_datetime = datetime.datetime.now()
        self.timers = dict()  # name to total seconds

    def to_dict(self):
        return dict(
            init_datetime=self.init_datetime.timestamp(),
            timers=self.timers,
        )

    def from_dict(d):
        r = Room()
        r.init_datetime = datetime.datetime.fromtimestamp(d['init_datetime'])
        r.timers = d['timers']
        return r

    def __repr__(self):
        return str(self.to_dict())

    def command_neu(self, argument, sender_firstname, sender_username):
        if argument in self.timers:
            value = self.timers[argument]
            if argument:
                return ('existiert', argument, format_seconds(value), sender_firstname)
            else:
                return ('existiert_anonym', format_seconds(value), sender_firstname)

        self.timers[argument] = 0
        if argument:
            return ('neu', argument, sender_firstname)
        else:
            return ('neu_anonym', sender_firstname)

    def command_zeige(self, argument, sender_firstname, sender_username):
        value = self.timers.get(argument, None)
        if value is None:
            if argument:
                return ('zeige_missing', argument, sender_firstname)
            else:
                return ('zeige_missing_anonym', sender_firstname)

        if argument:
            return ('zeige', argument, format_seconds(value), sender_firstname)
        else:
            return ('zeige_anonym', format_seconds(value), sender_firstname)


def compute_uptime(room, argument, sender_firstname, sender_username) -> None:
    return ('uptime', room.init_datetime.strftime(DATETIME_FORMAT), datetime.datetime.now().strftime(DATETIME_FORMAT))


def handle(room, command, argument, sender_firstname, sender_username):
    if command == 'uptime':
        return compute_uptime(room, argument, sender_firstname, sender_username)
    elif command == 'neu':
        return room.command_neu(argument, sender_firstname, sender_username)
    elif command == 'zeige':
        return room.command_zeige(argument, sender_firstname, sender_username)
    else:
        return ('unknown_command', sender_firstname)
