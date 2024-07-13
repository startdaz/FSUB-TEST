import datetime
import logging
import subprocess
import sys
from logging.handlers import RotatingFileHandler
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime as dt


def restart_sys():
    subprocess.run([sys.executable] + sys.argv)


class TimeConvert:
    def __init__(self, time_offset: int) -> int:
        self.time_offset = time_offset

    def utc_to_local(self) -> "dt":
        utc_time_now = datetime.datetime.utcnow()
        delta_hours = datetime.timedelta(hours=self.time_offset)
        return utc_time_now + delta_hours

    def local_time(self, *args):
        return self.utc_to_local().timetuple()


class PaddedLevelFormatter(logging.Formatter):
    def format(self, record):
        if record.levelname == "INFO":
            record.levelname = record.levelname.ljust(5)
        if record.levelname == "WARNING":
            record.levelname = "WARN".ljust(5)

        return super().format(record)


class Logger:
    delta_time: TimeConvert = TimeConvert(time_offset=7)

    def __init__(self, log_name: str):
        self.log_time = self.delta_time.local_time
        self.log_name = log_name

        self.log_setup()

    def log_exception_handler(self, record):
        exception_log = any(
            key in record.name for key in {"asyncio", "pymongo"}
        ) and record.levelname.strip() in {"WARN", "ERROR"}
        if exception_log:
            restart_sys()

    def log_setup(self) -> logging.Logger:
        logging.Formatter.converter = self.log_time
        log_level = logging.INFO

        formatter = PaddedLevelFormatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%x | %X",
        )

        file_handler = RotatingFileHandler(
            "logs.txt",
            mode="a",
            maxBytes=32768,
            backupCount=1,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(log_level)

        exception_handler = logging.StreamHandler()
        exception_handler.setLevel(log_level)
        exception_handler.setFormatter(formatter)
        exception_handler.emit = self.log_exception_handler

        logging.basicConfig(level=log_level, handlers=[file_handler, stream_handler])

        self.log = logging.getLogger(self.log_name)

        logging.getLogger("pymongo").setLevel(logging.WARNING)
        logging.getLogger("pyrogram").setLevel(logging.WARNING)

        logging.getLogger().addHandler(exception_handler)

        return self.log


logger: Logger = Logger(log_name="FSUB").log
