# timer-bot

Yet another timer bot for Telegram, because all the others suck.

The existing bots are all defunct or incomplete. So I wrote my own.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [TODOs](#todos)
- [NOTDOs](#notdos)
- [Contribute](#contribute)

## Install

```console
$ # Install Python3 somehow
$ pip3 install --user -r requirements.txt
```

That should be it.

## Usage

- Copy `secret_template.py` to `secret.py`
- Create your bot
    * This means you have to talk to the `@BotFather`: https://web.telegram.org/z/#93372553
    * Do `/newbot`, edit it as much as you like (i.e. description, photo)
    * For the commands, see `bot.py`, function `cmd_start`.
    * Invite him into the group chat(s) you like
    * Afterwards, set the bot to "Allow groups: No"
    * Copy the API token
- Fill in your own username and the API token in `secret.py`
- Run `bot.py`. I like to run it as `./bot.py 2>&1 | tee bot_$(date +%s).log`, because that works inside screen and I still have arbitrary scrollback.
- Write `/permit` into the chat to allow that room. Use `/admin` to view all the commands you have.
- You can Ctrl-C the bot at any time and restart it later. The state is made permanent in `timerbot_data.json`

## TODOs

Not much, maybe add more message variants?

## NOTDOs

Here are some things this project will definitely (probably) not support:
* Complex D&D-style roll syntax
* Any advanced parsing
* Any further control of the room

## Contribute

Feel free to dive in! [Open an issue](https://github.com/BenWiederhake/timer-bot/issues/new) or submit PRs.
