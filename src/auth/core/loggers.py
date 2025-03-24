"""Логгер конфиг модуль"""

from __future__ import annotations
import json
from pathlib import Path
import logging
import logging.config
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from auth.settings import Settings


def setup_logging(settings: Settings):
    config_file: Path = settings.paths.PATH_TO_BASE_FOLDER / "log_config.json"
    with open(config_file) as file:
        config = json.load(file)
    logging.config.dictConfig(config)
