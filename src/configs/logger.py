import logging
import logging.config
import sys

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s.%(msecs)03d] %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "logconsole": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["logconsole"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["logconsole"],
            "level": "DEBUG",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["logconsole"],
            "level": "INFO",
            "propagate": False,
        },
        "apscheduler": {
            "handlers": ["logconsole"],
            "level": "INFO",
            "propagate": False,
        },
        "sqlalchemy": {
            "handlers": ["logconsole"],
            "level": "WARN",
            "propagate": False,
        },
    },
    "root": {"handlers": ["logconsole"], "level": "INFO"},
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger()
