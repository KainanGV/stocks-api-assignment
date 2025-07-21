import logging
import sys

logger = logging.getLogger("stocks-api")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
