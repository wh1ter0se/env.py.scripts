import logging
import re

LIGHT_BLUE = "\033[94m"
LIGHT_ORANGE = "\033[93m"
LIGHT_RED_ORANGE = "\033[91m"
LIGHT_RED = "\033[95m"
GREY = "\033[90m"
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
                msg = " " * 4 + f"{GREY}{msg}{RESET}"

        # ---------- DEBUG ----------
        elif record.levelno == logging.DEBUG:
            msg = " " * 4 + f"{GREY}{msg}{RESET}"

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


def get_logger() -> logging.Logger:
    # Generate logger
    logger = logging.getLogger("singleton")

    # Configure logger (if not already confiugred)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(CustomFormatter())
        logger.addHandler(stream_handler)

    return logger
