import logging
import re
from typing import Optional

LIGHT_BLUE = "\033[94m"
LIGHT_ORANGE = "\033[93m"
LIGHT_RED_ORANGE = "\033[91m"
LIGHT_RED = "\033[95m"
RESET = "\033[0m"


class CustomFormatter(logging.Formatter):
    bracket_start = re.compile(r"^\[([^]]+)\]")

    def format(self, record: logging.LogRecord) -> str:
        msg = record.getMessage()
        if msg is None:
            return ""

        # ---------- INFO ----------
        if record.levelno == logging.INFO:
            m = self.bracket_start.match(msg)
            if m:
                inner = m.group(1)  # text inside brackets
                colored = f"[{LIGHT_BLUE}{inner}{RESET}]"  # color ONLY inside
                msg = colored + msg[m.end() :]  # keep rest unchanged
            else:
                msg = " " * 4 + msg

        # ---------- DEBUG ----------
        elif record.levelno == logging.DEBUG:
            msg = " " * 4 + msg

        # ---------- WARNING ----------
        elif record.levelno == logging.WARNING:
            msg = f"  {LIGHT_ORANGE}!{RESET} " + msg

        # ---------- ERROR ----------
        elif record.levelno == logging.ERROR:
            msg = f" {LIGHT_RED_ORANGE}!!{RESET} " + msg

        # ---------- CRITICAL ----------
        elif record.levelno == logging.CRITICAL:
            msg = f"{LIGHT_RED}!!!{RESET} " + msg

        return msg


def get_logger(
    name: Optional[str] = None,
    level: str = "info",
) -> logging.Logger:
    # Convert level string to literal
    upper_level = level.strip().upper()
    if upper_level not in logging._nameToLevel.keys():
        raise ValueError(f"Invalid log level: {level}")
    literal_level = logging._nameToLevel[upper_level]

    # Generate logger
    logger = logging.getLogger(name)
    logger.setLevel(literal_level)

    # Attach stream (console) handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(literal_level)
    stream_handler.setFormatter(CustomFormatter())
    logger.addHandler(stream_handler)

    return logger
