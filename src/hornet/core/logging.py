import logging
import logging.handlers
import os

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
    rotating = logging.handlers.RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    rotating.setFormatter(formatter)
    root.addHandler(rotating)
