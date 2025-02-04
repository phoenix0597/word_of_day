import sys
from os.path import join
from loguru import logger

from core.config import settings


def setup_logging():
    logger.remove()

    # настройки логирования в консоль
    logger.add(
        sys.stdout,
        format="{time: YYYY-MM-DD HH:mm:ss} | {level} | {module}: {message}",
        level="INFO",
        colorize=True,
    )

    # настройки логирования в файл
    logger.add(
        join(settings.BASE_DIR, "logs", "app.log"),
        format="{time: YYYY-MM-DD HH:mm:ss} | {level} | {module}: {message}",
        level="INFO",
        colorize=True,
        rotation="500 MB",
        compression="zip",
    )
