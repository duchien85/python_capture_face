import logging
import sys

# Tạo logger chung
logger = logging.getLogger("face_app")
logger.setLevel(logging.DEBUG)

# Handler in ra console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# Format log
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)

# Gắn handler
if not logger.handlers:
    logger.addHandler(console_handler)
