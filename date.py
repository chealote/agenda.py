import re
import sys

from datetime import datetime

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
            found_hour = True
            (hours, minutes) = piece.split(":")
            date_str += f"{hours}:{minutes}"
            date_fmt += f"%H:%M"
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

if __name__ == "__main__":
    print(parse_date(" ".join(sys.argv[1:])))
