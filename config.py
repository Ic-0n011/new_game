import sys
import os

# config.py
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
BROWN = (139, 69, 19)

MONITOR_POS = (250, 50)
MONITOR_SIZE = (300, 200)
TABLE_POS = (0, 250)
TABLE_SIZE = (800, 350)

ENDING_SMASHED_MONITOR = 1
ENDING_BUTTON_THREE_TIMES = 2
ENDING_BUTTON_AND_LEVER = 3

def resource_path(relative_path):
    """Возвращает абсолютный путь к ресурсу.
    Работает для разработки и для собранного приложения с помощью PyInstaller."""
    try:
        # При упаковке PyInstaller создает временную папку, путь к которой хранится в sys._MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
