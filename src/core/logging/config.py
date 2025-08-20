import logging
import logging.config
import os
import sys
from typing import Dict, Any


def setup_logging() -> None:
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    environment = os.getenv("ENVIRONMENT", "development")
    is_docker = os.getenv("DOCKER_ENV", "false").lower() == "true"

    if is_docker:
        handlers = ["console"]
        handlers_config = {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "detailed" if environment == "development" else "default",
                "stream": sys.stdout
            }
        }
    else:
        handlers = ["console", "file", "error_file"]
        handlers_config = {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "detailed" if environment == "development" else "default",
                "stream": sys.stdout
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "detailed",
                "filename": "logs/task-manager.log",
                "maxBytes": 10485760,
                "backupCount": 5,
                "encoding": "utf-8"
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": "logs/task-manager-errors.log",
                "maxBytes": 10485760,
                "backupCount": 5,
                "encoding": "utf-8"
            }
        }

    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "json": {
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(name)s %(levelname)s %(funcName)s %(lineno)d %(message)s"
            }
        },
        "handlers": handlers_config,
        "loggers": {
            "": {
                "level": log_level,
                "handlers": handlers,
                "propagate": False
            },
            "src.task": {
                "level": log_level,
                "handlers": handlers,
                "propagate": False
            },
            "src.core": {
                "level": log_level,
                "handlers": handlers,
                "propagate": False
            },
            "sqlalchemy.engine": {
                "level": "INFO" if os.getenv("SQL_ECHO", "false").lower() == "true" else "WARNING",
                "handlers": handlers,
                "propagate": False
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": handlers,
                "propagate": False
            },
            "fastapi": {
                "level": "INFO",
                "handlers": handlers,
                "propagate": False
            }
        }
    }

    if not is_docker:
        os.makedirs("logs", exist_ok=True)

    logging.config.dictConfig(logging_config)

    logger = logging.getLogger(__name__)
    logger.info(f"Логгирование настроено. Уровень: {log_level}, Среда: {environment}, Docker: {is_docker}")
