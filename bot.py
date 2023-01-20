#!/usr/bin/env python3

from atomicwrites import atomic_write
import json
import logging
import os
import secret  # See secret_template.py
import secrets
import sys

# Written for telegram.__version__ >= 20.0
from telegram import Chat, ChatMember, ChatMemberUpdated, Update
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    Updater,
)

import logic
import msg


logger = logging.getLogger(__name__)

PERMANENCE_FILENAME = 'timerbot_data.json'

ROOMS = dict()


def load_rooms():
    global ROOMS
    if os.path.exists(PERMANENCE_FILENAME):
        with open(PERMANENCE_FILENAME, 'r') as fp:
            rooms = json.load(fp)
        for chat_id, room_dict in rooms.items():
            ROOMS[int(chat_id)] = logic.Room.from_dict(room_dict)
        logger.info(f'Loaded {len(ROOMS)} rooms.')
    else:
        logger.info(f'Permanence file {PERMANENCE_FILENAME} does not exist; starting with all rooms denied.')


def save_rooms():
    rooms = {k: v.to_dict() for k, v in ROOMS.items()}
    with atomic_write(PERMANENCE_FILENAME, overwrite=True) as fp:
        json.dump(rooms, fp, indent=1)
    logger.info(f'Wrote {len(rooms)} to {PERMANENCE_FILENAME}.')


def message(msg_id):
    return secrets.choice(msg.MESSAGES[msg_id])


async def cmd_admin(update: Update, _context: CallbackContext) -> None:
    if update.effective_user.id != secret.OWNER_ID:
        return

    await update.effective_message.reply_text(
        'The admin can do:'
        '\n/admin → show admin commands'
        '\n/show_state → show *all* internal state'
        '\n/resetall → reset all rooms'
        '\n/resethere → reset current room'
        '\n/permit → permit the current room, if not already'
        '\n/deny → stop and deny the current room'
        '\n/denyall → stop and deny all rooms'
    )


async def cmd_show_state(update: Update, _context: CallbackContext) -> None:
    if update.effective_user.id != secret.OWNER_ID:
        return

    await update.effective_message.reply_text(str(ROOMS))


async def cmd_resetall(update: Update, _context: CallbackContext) -> None:
    global ROOMS

    if update.effective_user.id != secret.OWNER_ID:
        return

    for key in ROOMS.keys():
        ROOMS[key] = logic.Room()
    save_rooms()
    await update.effective_message.reply_text(f'Alle Räume zurückgesetzt. ({len(ROOMS.keys())} erlaubte Räume blieben erhalten.)')


async def cmd_resethere(update: Update, _context: CallbackContext) -> None:
    global ROOMS

    if update.effective_user.id != secret.OWNER_ID:
        return

    if update.effective_chat.id in ROOMS.keys():
        ROOMS[update.effective_chat.id] = logic.Room()
        save_rooms()
        await update.effective_message.reply_text('Diesen Raum zurückgesetzt.')
    else:
        await update.effective_message.reply_text('Dieser Raum war noch nicht erlaubt. Meintest du /permit?')


async def cmd_permit(update: Update, _context: CallbackContext) -> None:
    global ROOMS

    if update.effective_user.id != secret.OWNER_ID:
        return

    if update.effective_chat.id in ROOMS.keys():
        await update.effective_message.reply_text('Dieser Raum ist bereits erlaubt. Vielleicht meintest du /reset oder /start?')
    else:
        ROOMS[update.effective_chat.id] = logic.Room()
        save_rooms()
        await update.effective_message.reply_text('Bot für diesen Raum aktiviert. Probier doch mal /start! :)')


async def cmd_deny(update: Update, _context: CallbackContext) -> None:
    global ROOMS

    if update.effective_user.id != secret.OWNER_ID:
        return

    if update.effective_chat.id in ROOMS.keys():
        del ROOMS[update.effective_chat.id]
        save_rooms()
        await update.effective_message.reply_text('Raum gelöscht.')
    else:
        await update.effective_message.reply_text('Raum ist bereits gelöscht(?)')


async def cmd_denyall(update: Update, _context: CallbackContext) -> None:
    global ROOMS

    if update.effective_user.id != secret.OWNER_ID:
        return

    count = len(ROOMS)
    ROOMS = dict()
    save_rooms()
    await update.effective_message.reply_text(f'Alle {count} Räume gelöscht.')


async def cmd_start(update: Update, _context: CallbackContext) -> None:
    await update.effective_message.reply_text(
        f'Hi {update.effective_user.first_name}!'
        f'\n/neu [TIMERNAME] – Legt einen neuen Timer an. Wenn TIMERNAME weggelassen wird, dann legt es den Default-Timer an.'
        f'\n/plus [TIMERNAME] ZEIT – Fügt ZEIT dem Default-Timer oder dem TIMERNAME hinzu.'
        f'\n/minus [TIMERNAME] ZEIT – Nimmt ZEIT vom Default-Timer runter, oder vom TIMERNAME.'
        f'\n/help – Erklärt wie die Zeit-Angaben funktionieren.'
        f'\n/zeige TIMERNAME – Zeigt wieviel Zeit auf dem TIMERNAME noch verbleibt.'
        f'\n/list – Listet alle Timer auf.'
        f'\nhttps://github.com/BenWiederhake/timer-bot'
        # For botfather:
        # plus_viertel - Default-Timer +15 Minuten
        # plus_stunde - Default-Timer +60 Minuten
        # plus_tag - Default-Timer +24 Stunden
        # list - Alle Timer auflisten
    )


def cmd_for(command):
    async def cmd_handler(update: Update, _context: CallbackContext):
        if update.message is None or update.message.text is None:
            return  # Don't consider Updates that don't stem from a text message.
        text = update.message.text.split(' ', 1)
        argument = text[1] if len(text) == 2 else ''

        room = ROOMS.get(update.effective_chat.id)
        if room is None:
            return  # No interactions permitted
        maybe_response = logic.handle(room, command, argument, update.effective_user.first_name, update.effective_user.username)
        save_rooms()
        if maybe_response is None:
            return  # Don't respond at all
        await update.effective_message.reply_text(
            message(maybe_response[0]).format(*maybe_response[1:])
        )
    return cmd_handler


def run():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.info("Alive")

    load_rooms()

    application = Application.builder().token(secret.TOKEN).build()

    application.add_handler(CommandHandler("admin", cmd_admin))
    application.add_handler(CommandHandler("show_state", cmd_show_state))
    application.add_handler(CommandHandler("dump_state", cmd_show_state))
    application.add_handler(CommandHandler("resetall", cmd_resetall))
    application.add_handler(CommandHandler("resethere", cmd_resethere))
    application.add_handler(CommandHandler("permit", cmd_permit))
    application.add_handler(CommandHandler("deny", cmd_deny))
    application.add_handler(CommandHandler("denyall", cmd_denyall))
    application.add_handler(CommandHandler("start", cmd_start))

    application.add_handler(CommandHandler("help", cmd_for('help')))
    application.add_handler(CommandHandler("neu", cmd_for('neu')))
    application.add_handler(CommandHandler("plus", cmd_for('plus')))
    application.add_handler(CommandHandler("minus", cmd_for('minus')))
    application.add_handler(CommandHandler("zeige", cmd_for('zeige')))
    application.add_handler(CommandHandler("list", cmd_for('list')))
    application.add_handler(CommandHandler("plus_viertel", cmd_for('plus_viertel')))
    application.add_handler(CommandHandler("plus_stunde", cmd_for('plus_stunde')))
    application.add_handler(CommandHandler("plus_tag", cmd_for('plus_tag')))
    application.add_handler(CommandHandler("uptime", cmd_for('uptime')))
    application.add_handler(CommandHandler("unknown_command", cmd_for('unknown_command')))  # By popular opinion

    logger.info("Begin idle loop")
    application.run_polling()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        run()
    elif len(sys.argv) == 2 and sys.argv[1] == '--dry-run':
        print(f'Dry-running from file {PERMANENCE_FILENAME}')
        load_rooms()
        print(f'Loaded: {ROOMS}')
    else:
        print(f'USAGE: {sys.argv[0]} [--dry-run]')
        exit(1)
