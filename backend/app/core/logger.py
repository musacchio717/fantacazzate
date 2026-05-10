# backend/app/core/logger.py
import logging
import os
from datetime import datetime

# Crea la cartella logs se non esiste
os.makedirs("logs", exist_ok=True)

# Configura il logger
logger = logging.getLogger("fantacazzate")
logger.setLevel(logging.INFO)

# Handler per il file — scrive su logs/fantacazzate.log
file_handler = logging.FileHandler(
    f"logs/fantacazzate.log",
    encoding="utf-8"
)
file_handler.setLevel(logging.INFO)

# Handler per la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formato del log
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)