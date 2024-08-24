import re

from storage import Storage
from datetime import datetime, timedelta
from log import Log, LogLevel

class Events:
    id:int
    description:str
    date_time:str

class AgendaDate:
    __fmt_date = "%Y-%m-%d %H:%M:%S"
    __valid_date_formats = ["%d", "%b", "%m", "%Y", "%y"]

    def fmt_time(date):
        return date.strftime(AgendaDate.__fmt_date)

    def parse_date(input_date):
        format_parts = {
                "day": ["%d"],
                "month": ["%b", "%m", "%B"],
                "year": ["%Y", "%y"],
                }
        found_parts = {}
        date_str = ""
        date_fmt = ""
        input_pieces = input_date.split(" ")
        current_piece = 0
        found_hour = False

        for piece in input_pieces:
            if re.match("[0-9]+:[0-9]+", piece):
                (hours, minutes) = piece.split(":")
                date_str += f"{hours}:{minutes} "
                date_fmt += f"%H:%M "
                found_hour = True
                # TODO not found part? can find multiple times?
                continue
            break_piece = False
            for part in format_parts:
                if break_piece:
                    break
                if part in found_parts:
                    continue
                for fmt in format_parts[part]:
                    try:
                        datetime.strptime(piece, fmt)
                        date_str += piece + "-"
                        date_fmt += fmt + "-"
                        break_piece = True
                        found_parts[part] = True
                        break
                    except ValueError as e:
                        pass

        if not found_hour:
            date_str += "23:59"
            date_fmt += "%H:%M"

        now = datetime.now()
        for part in format_parts:
            if part not in found_parts:
                fmt = format_parts[part][0]
                date_str += now.strftime(fmt)
                date_fmt += fmt

        return datetime.strptime(date_str, date_fmt)

class AgendaDB:
    def __init__(self, log=None):
        self.__log = log

    def __pretty_print_event(self, event, show_id=False):
        fmt = f"{event[1]} (At: {event[2]})"
        if show_id:
            fmt = f"{event[1]} (At: {event[2]}) ({event[0]})"
        print(fmt)

    def __events_within_dates(self, start_date, end_date):
        start_str = AgendaDate.fmt_time(start_date)
        end_str = AgendaDate.fmt_time(end_date)
        with Storage(Events, log=self.__log) as storage:
            return storage.filter_between(Events, "date_time", (start_str, end_str))

    def __insert_new_event(self, description, date=None):
        with Storage(Events, log=self.__log) as storage:
            e = Events()
            e.description = description
            if date is not None:
                e.date_time = AgendaDate.fmt_time(date)
            else:
                e.date_time = "daily"
            self.__log.debug(f"Item before storing: {e.description} {e.date_time}")
            storage.insert(e)

    def list_events_7days_ids(self):
        return self.list_events_7days(show_id=True)

    def list_events_7days(self, show_id=False):
        now = datetime.now()
        events = self.__events_within_dates(now, now + timedelta(days=7))
        for event in events:
            self.__pretty_print_event(event, show_id)

    def list_all_events(self):
        with Storage(Events, log=self.__log) as storage:
            events = storage.select_all(Events)
            for event in events:
                self.__pretty_print_event(event, show_id=True)

    def add_new_event(self, description, date_str):
        if date_str == "daily":
            self.__log.info(f"This event occurs daily")
            self.__insert_new_event(description, date=None)
            return
        date = AgendaDate.parse_date(date_str)
        self.__log.info(f"Parsed date: {date}")
        self.__insert_new_event(description, date=date)

    def del_event(self, item_id):
        item = Events()
        item.id = item_id
        with Storage(Events, log=self.__log) as storage:
            storage.delete(item)

    def list_daily_events(self):
        with Storage(Events, log=self.__log) as storage:
            events = storage.filter_key_values(Events, {"date_time": "daily"})
            for event in events:
                self.__pretty_print_event(event)

if __name__ == "__main__":
    agenda = AgendaDB()
    agenda.list_events_7days()
