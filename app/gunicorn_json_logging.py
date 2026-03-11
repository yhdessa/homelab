import logging
from pythonjsonlogger import jsonlogger

access_logger = logging.getLogger("gunicorn.access")
access_logger.setLevel(logging.INFO)

json_formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(message)s %(pathname)s %(funcName)s %(lineno)d",
    json_ensure_ascii=False,
    datefmt="%Y-%m-%dT%H:%M:%S%z"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(json_formatter)
access_logger.addHandler(console_handler)

error_logger = logging.getLogger("gunicorn.error")
error_logger.setLevel(logging.ERROR)
error_logger.addHandler(console_handler)

logging.getLogger("werkzeug").setLevel(logging.WARNING)
