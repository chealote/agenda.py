#!/bin/python3

import sys
from agenda import AgendaDB
from log import Log, LogLevel

log = Log(LogLevel.INFO)
AGENDA = AgendaDB(log=log)

# TODO: make valid_nargs more dynamic, I want to compare the same number, greater or less as well
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

# TODO: errors don't look right, try an invalid amount of args
class ArgsError(Exception):
    pass

# TODO no longer needed! just keeping around for now
#def parse_args():
#    if len(sys.argv) == 1:
#        return ("list", None)
#    cmd = sys.argv[1]
#    nargs = sys.argv[2:]
#    if cmd in COMMANDS:
#        valid_nargs = COMMANDS[cmd]["valid_nargs"]
#        if len(nargs) != valid_nargs and valid_nargs != -1:
#            raise ArgsError(COMMANDS[cmd]["help"])
#        return (cmd, nargs)
#    return ("help", None)

#def run_cmd(cmd, args_array=None):
#    if cmd == "list":
#        AGENDA.list_events_7days()
#    elif cmd == "id":
#        AGENDA.list_events_7days(show_id=True)
#    elif cmd == "all":
#        AGENDA.list_all_events()
#    elif cmd == "del":
#        for event_id in args_array:
#            AGENDA.del_event(event_id)
#    elif cmd == "new":
#        desc = args_array[0]
#        date_str = args_array[1]
#        AGENDA.add_new_event(desc, date_str)
#    elif cmd == "daily":
#        print("daily")
#        AGENDA.list_daily_events()
#    elif cmd == "help":
#        print("help?")

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
        print("help message")
    except IndexError as e:
        print("again the help message")
    except ArgsError as e:
        print("ERROR:", e)
    except Exception as e:
        raise e

if __name__ == "__main__":
    main()

sys.exit(0)
