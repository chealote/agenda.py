from datetime import datetime
from enum import IntEnum

class LogLevel(IntEnum):
    DEBUG = 1
    INFO = 2
    ERROR = 3

class Log:
    __date_fmt = "%d-%m-%yT%H:%M:%S"

    def __init__(self, level=LogLevel.INFO):
        self.level = level

    def __prefix_log(level):
        if level == LogLevel.DEBUG:
            return "DEBUG"
        elif level == LogLevel.INFO:
            return "INFO"
        elif level == LogLevel.ERROR:
            return "ERROR"

    def __date_str():
        return datetime.now().strftime(Log.__date_fmt)

    # level: debug 1 -> 1 2 3
    # class: info 2 -> 2 3
    def __log(self, level, msg):
        if self.level <= level:
            print(f"[{Log.__date_str()} {Log.__prefix_log(level)}]: {msg}")

    def info(self, msg):
        self.__log(LogLevel.INFO, msg)

    def debug(self, msg):
        self.__log(LogLevel.DEBUG, msg)

    def error(self, msg):
        self.__log(LogLevel.ERROR, msg)

if __name__ == "__main__":
    log = Log(LogLevel.INFO)
    log.info("hello")
    log.error("oh no")
    log.debug("this is debug 1")
    log = Log(LogLevel.DEBUG)
    log.debug("this is debug 2")
