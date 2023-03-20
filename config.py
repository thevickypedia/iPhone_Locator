import logging
import os

import dotenv

dotenv.load_dotenv(dotenv_path=".env")

LOGGER = logging.getLogger(__name__)
HANDLER = logging.StreamHandler()
FORMATTER = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - [%(processName)s:%(module)s:%(lineno)d] - %(funcName)s - %(message)s'
)
HANDLER.setFormatter(fmt=FORMATTER)
LOGGER.addHandler(hdlr=HANDLER)
LOGGER.setLevel(level=logging.DEBUG)


class EnvConfig(dict):
    """Wrapper for env variables."""

    apple_id: str = os.environ.get("APPLE_ID") or os.environ.get("apple_id")
    password: str = os.environ.get("PASSWORD") or os.environ.get("password")
    gmail_user: str = os.environ.get("GMAIL_USER") or os.environ.get("gmail_user")
    gmail_pass: str = os.environ.get("GMAIL_PASS") or os.environ.get("gmail_pass")
    recipient: str = os.environ.get("RECIPIENT") or os.environ.get("recipient")
    device: str = os.environ.get("DEVICE") or os.environ.get("device")
    location: str = os.environ.get("LOCATION") or os.environ.get("location") or "EARTH"


env = EnvConfig()

if not all((env.apple_id, env.password)):
    raise ValueError("apple_id and password are mandatory args")
