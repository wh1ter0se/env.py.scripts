import logging
from typing import ClassVar, Dict, Optional


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_template = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS: ClassVar[Dict[int, str]] = {
        logging.DEBUG: grey + format_template + reset,
        logging.INFO: grey + format_template + reset,
        logging.WARNING: yellow + format_template + reset,
        logging.ERROR: red + format_template + reset,
        logging.CRITICAL: bold_red + format_template + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


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
