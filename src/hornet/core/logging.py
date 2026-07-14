import logging
import logging.handlers
import os

from hornet.constants import LOG_BACKUP_COUNT, LOG_MAX_BYTES

def setup_logging(level: str, log_file: str) -> None:
    parent = os.path.dirname(log_file)

    if parent:
        os.makedirs(parent, exist_ok=True)

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    root = logging.getLogger()
    root.setLevel(level)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    root.addHandler(console)
    rotating = logging.handlers.RotatingFileHandler(log_file, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
    rotating.setFormatter(formatter)
    root.addHandler(rotating)
