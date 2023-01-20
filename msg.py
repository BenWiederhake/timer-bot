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
    'modify_noarg': [
        'Sorry {0}, leider musst du das eintippen, mit Argument wie viel es sein soll. /help erklärt, wie.',
        'Das musst du leider in Langform eintippen, {0}. Probier mal /help.',
        'Dazu muss ich erst wissen wieviel, {0}. /halp sagt dir, wie es geht.',
        'Das geht leider nicht ohne Argument, {0}. Schau dir mal /help an.',
    ],
    'modify_missing_anonym': [
        'Sorry {0}, aber da der Default-Timer nicht existiert geht das schlecht. Mach mal /neu, dann geht das.',
        'Sorry {0}, aber es gibt keinen Default-Timer, also kann ich ihn nicht verändern. Mit /neu kannst du ihn anlegen, mit /help erkläre ich nochmal das Zeit-Format.',
    ],
    'modify_missing': [
        'Sorry {0}, aber den Timer {1} gibt es noch nicht. Mach mal /neu {1} vielleicht, oder schau dir /help an?',
    ],
    'plus_anonym': [
        'Natürlich {2}, Default-Timer um {0} erhöht. Er steht jetzt auf {1}.',
        'Default-Timer um {0} erhöht, und steht jetzt auf {1}.',
        'Default-Timer plus {0} ergibt {1}, {2}.',
        'Mit den neuen {0} sind jetzt {1} im Default-Timer, {2}.',
        'Plus {0} ergibt {1} im Default-Timer, {2}.',
        '{2} hat {0} draufgepackt, jetzt sind {1} im Default-Timer.',
        'Mit den {0} von {2} sind jetzt {1} im Default-Timer.',
    ],
    'plus': [
        'Natürlich {3}, Timer {0} um {1} erhöht. Er steht jetzt auf {2}.',
        'Timer {0} um {1} erhöht, und steht jetzt auf {2}.',
        'Timer {0} plus {1} ergibt {2}, {3}.',
        'Mit den neuen {1} sind jetzt {2} im Timer {0}, {3}.',
        'Plus {1} ergibt {2} im Timer {0}, {3}.',
        '{3} hat {1} draufgepackt, jetzt sind {2} im Timer {0}.',
        'Mit den {1} von {3} sind jetzt {2} im Timer {0}.',
    ],
    'minus_anonym': [
        'Natürlich {2}, {0} vom Default-Timer abgezogen. Er steht jetzt auf {1}.',
        'Default-Timer um {0} verringert, und steht jetzt auf {1}.',
        'Default-Timer minus {0} ergibt {1}, {2}.',
        'Um {0} weniger ergibt {1} im Default-Timer, {2}.',
        'Minus {0} ergibt {1} im Default-Timer, {2}.',
        '{2} hat {0} abgezogen, jetzt sind {1} im Default-Timer.',
        'Ohne die {0} von {2} sind jetzt {1} im Default-Timer.',
    ],
    'minus': [
        'Natürlich {3}, {1} vom Timer {0} abgezogen. Er steht jetzt auf {2}.',
        'Timer {0} um {1} verringert, und steht jetzt auf {2}.',
        'Timer {0} minus {1} ergibt {2}, {3}.',
        'Um {1} weniger ergibt {2} im Timer {0}, {3}.',
        'Minus {1} ergibt {2} im Timer {0}, {3}.',
        '{3} hat {1} abgezogen, jetzt sind {2} im Timer {0}.',
        'Ohne die {1} von {3} sind jetzt {2} im Timer {0}.',
    ],
    'modify_invalid_onearg': [
        'Sorry {1}, aber "{0}" verstehe ich nicht. Schau dir vielleicht nochmal /help an?',
        'Leider kann ich die Zeit "{0}" nicht verstehen. Schau dir nochmal /help an, oder falls das ein Timer-Name war gib die Zeit noch zusätzlich an.',
    ],
    'modify_invalid_twoarg': [
        'Sorry {1}, ich weiß welchen Timer du meinst, aber "{0}" verstehe ich nicht. Schau dir vielleicht nochmal /help an?',
        'Leider kann ich die Zeit "{0}" nicht verstehen. Vielleicht hilft die Erklärung in /help?',
    ],
    'uptime': [
        'Der Bot war hier das erste Mal {0} aktiv. Jetzt ist es {1}.',
    ],
    'list': [
        'Natürlich, {0}. Die Timer stehen bei:\n{1}',
        'Hey {0}, die Timer stehen im Moment bei:\n{1}',
    ],
    'unknown_command': [
        'Häh?',
        'Was?',
        'Bestimmt weiß ich eines Tages, was das bedeuten soll.',
        'Ich habe nicht genügend Erfahrung, um diese Aufgabe auszuführen.',
        'Wenn ich mal groß und stark bin kann ich das auch!',
        '🥺',
    ],
    'help': [
        'Gerne doch, {0}! Zeit-formate gibst du an als "1d" für einen Tag (day), "2h" für zwei Stunden, "3m" oder "3min" für drei Minuten. Und das kann man zusammengeschrieben. Also würde "1d2h3m" bedeuted: Ein Tag, zwei Stunden, und drei Minuten.',
    ],
}
