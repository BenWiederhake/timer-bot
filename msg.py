#!/usr/bin/env false

import secret

MESSAGES = {
    'neu': [
        'Timer "{0}" mit null Sekunden angelegt, {1}.',
        'Natürlich, {1}. Es gibt jetzt den Timer "{0}", mit initial null Sekunden.',
    ],
    'neu_anonym': [
        'Default-Timer mit null Sekunden angelegt, {0}.',
        'Natürlich, {0}. Es gibt jetzt den Default-Timer, mit initial null Sekunden.',
    ],
    'existiert': [
        'Den Timer "{0}" gibt es bereits, {2}. Da sind noch {1} drauf.',
        'Sorry {2}, das geht nicht. Den Timer "{0}" gibt es bereits, übrigens mit {1} verbleibend.',
    ],
    'existiert_anonym': [
        'Den Default-Timer gibt es bereits, da sind noch {0} drauf, {1}.',
        'Sorry {1}, das geht nicht. Den Default-Timer gibt es bereits, übrigens mit {0} verbleibend.',
    ],
    'zeige_missing': [
        'Der Timer "{0}" existiert nicht. Meintest du vielleicht "/neu {0}", {1}?',
    ],
    'zeige_missing_anonym': [
        'Der Default-Timer existiert nicht. Meintest du vielleicht "/neu", {0}?',
    ],
    'zeige': [
        'Der Timer "{0}" steht bei {1}, {2}.',
        'Im Moment hat der Timer "{0}" {1}, {2}.',
        'Klar, {2}: Es sind {1} auf dem Timer "{0}".',
    ],
    'zeige_anonym': [
        'Der Default-Timer steht bei {0}, {1}.',
        'Im Moment hat der Default-Timer {0}, {1}.',
        'Klar, {1}: Es sind {0} auf dem Default-Timer.',
    ],
    'uptime': [
        'Der Bot war hier das erste Mal {0} aktiv. Jetzt ist es {1}.',
    ],
    'unknown_command': [
        'Häh?',
        'Was?',
        'Bestimmt weiß ich eines Tages, was das bedeuten soll.',
        'Ich habe nicht genügend Erfahrung, um diese Aufgabe auszuführen.',
        'Wenn ich mal groß und stark bin kann ich das auch!',
        '🥺',
    ],
    'debug1': [
        '{0}',
    ],
}
