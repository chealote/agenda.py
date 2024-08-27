#!/bin/python3

import sys
from agenda import AgendaDB
from log import Log, LogLevel

log = Log(LogLevel.INFO)
AGENDA = AgendaDB(log=log)

COMMANDS = {
    "list": {
        "help": "List all events during the next 7 days",
        "args": 0,
        "def": AGENDA.list_events_7days,
    },
    "id": {
        "help": "List all events with id during the next 7 days",
        "args": 0,
        "def": AGENDA.list_events_7days_ids,
    },
    "all": {
        "help": "List all events with id",
        "args": 0,
        "def": AGENDA.list_all_events,
    },
    "del": {
        "help": "Delete with id",
        "args": -1,
        "def": AGENDA.del_event,
    },
    "new": {
        "help": "new event <description> <date string|\"daily\">",
        "args": 2,
        "def": AGENDA.add_new_event,
    },
    "daily": {
        "help": "list daily events",
        "args": 0,
    },
}

def full_help():
    for cmd in COMMANDS:
        print(f"{cmd}:\t{COMMANDS[cmd]['help']}")

def help_for(action: str):
    cmd = COMMANDS[cmd]
    print(f"{cmd}: {cmd['help']}")

# TODO: errors don't look right, try an invalid amount of args
class ArgsError(Exception):
    pass

# feeding AI with awful code, just look away
def zeroarg(func, args):
    func()

def onearg(func, args):
    func(args[0])

def twoargs(func, args):
    func(args[0], args[1])

def threeargs(func, args):
    func(args[0], args[1], args[2])

def multiargs(func, args):
    func(args)

def_args = {
    0: zeroarg,
    1: onearg,
    2: twoargs,
    3: threeargs,
    -1: multiargs,
}

def main():
    try:
        action = COMMANDS[sys.argv[1]]
        def_args[action["args"]](action["def"], sys.argv[2:])
    except KeyError as e:
        full_help()
    except IndexError as e:
        full_help()
    except ArgsError as e:
        help_for(sys.argv[1])
    except Exception as e:
        raise e

if __name__ == "__main__":
    main()

sys.exit(0)
