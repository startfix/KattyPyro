import logging
from logging import *
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler


"""
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "logs.txt", maxBytes=5000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)"""

basicConfig(
# Konfigurasi handler konsol
    level=INFO,
    format="%(filename)s:%(lineno)s %(levelname)s: %(message)s",
    datefmt="%m-%d %H:%M",
    handlers=[RichHandler()],
)
console = StreamHandler()
console.setLevel(logging.ERROR)
console.setFormatter(Formatter("%(filename)s:%(lineno)s %(levelname)s: %(message)s"))
logging.getLogger("").addHandler(console)

# Set level untuk beberapa logger tertentu
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)

# Fungsi untuk mendapatkan logger
def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
