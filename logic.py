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

    def modify_by(self, sign, argument, sender_firstname, sender_username):
        if not argument:
            return ('modify_noarg', sender_firstname)

        parts = argument.split(" ", 1)
        if len(parts) > 1:
            assert len(parts) == 2
            timer_name = parts[0]
            old_value = self.timers.get(timer_name, None)
            if old_value is None:
                return ('modify_missing', timer_name, sender_firstname)
            modify_part = parts[1]
            modify_amount = parse_seconds(modify_part)
            if modify_amount is None:
                return ('modify_invalid_twoarg', modify_part, sender_firstname)
        else:
            assert len(parts) == 1
            timer_name = ""
            old_value = self.timers.get(timer_name, None)
            # Check old_value for `None` later.
            modify_part = parts[0]
            modify_amount = parse_seconds(modify_part)
            if modify_amount is None:
                return ('modify_invalid_onearg', modify_part, sender_firstname)
            if old_value is None:
                return ('modify_missing_anonym', sender_firstname)

        new_value = max(0, old_value + sign * modify_amount)
        self.timers[timer_name] = new_value

        modify_amount_str = format_seconds(modify_amount)  # Well-formed, in contrast to the input
        new_value_str = format_seconds(new_value)
        if sign > 0:
            if timer_name:
                return ('plus', timer_name, modify_amount_str, new_value_str, sender_firstname)
            else:
                return ('plus_anonym', modify_amount_str, new_value_str, sender_firstname)
        else:
            if timer_name:
                return ('minus', timer_name, modify_amount_str, new_value_str, sender_firstname)
            else:
                return ('minus_anonym', modify_amount_str, new_value_str, sender_firstname)

    def command_list(self, argument, sender_firstname, sender_username):
        entries = list(self.timers.items())
        if not entries:
            return ('list', '(keine Timer)', sender_firstname)

        entries.sort()
        default_name = 'Default-Timer'
        parts = [f"{name if name else default_name}: {format_seconds(secs)}" for name, secs in entries]
        return ("list", "\n".join(parts), sender_firstname)


def compute_uptime(room, argument, sender_firstname, sender_username) -> None:
    return ('uptime', room.init_datetime.strftime(DATETIME_FORMAT), datetime.datetime.now().strftime(DATETIME_FORMAT))


def handle(room, command, argument, sender_firstname, sender_username):
    if command == 'uptime':
        return compute_uptime(room, argument, sender_firstname, sender_username)
    elif command == 'neu':
        return room.command_neu(argument, sender_firstname, sender_username)
    elif command == 'zeige':
        return room.command_zeige(argument, sender_firstname, sender_username)
    elif command == 'list':
        return room.command_list(argument, sender_firstname, sender_username)
    elif command == 'plus':
        return room.modify_by(1, argument, sender_firstname, sender_username)
    elif command == 'minus':
        return room.modify_by(-1, argument, sender_firstname, sender_username)
    elif command == 'help':
        return ('help', sender_firstname)
    elif command == 'plus_viertel':
        amount = "15min"
        padded = f"{argument} {amount}" if argument else amount
        return room.modify_by(1, padded, sender_firstname, sender_username)
    elif command == 'plus_stunde':
        amount = "1h"
        padded = f"{argument} {amount}" if argument else amount
        return room.modify_by(1, padded, sender_firstname, sender_username)
    elif command == 'plus_tag':
        amount = "1d"
        padded = f"{argument} {amount}" if argument else amount
        return room.modify_by(1, padded, sender_firstname, sender_username)
    else:
        return ('unknown_command', sender_firstname)
