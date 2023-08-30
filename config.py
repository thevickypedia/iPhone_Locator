import logging
import smtplib
import socket
from typing import Union

import gmailconnector as gc
from pydantic import EmailStr
from pydantic_settings import BaseSettings

LOGGER = logging.getLogger(__name__)
HANDLER = logging.StreamHandler()
FORMATTER = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - [%(processName)s:%(module)s:%(lineno)d] - %(funcName)s - %(message)s'
)
HANDLER.setFormatter(fmt=FORMATTER)
LOGGER.addHandler(hdlr=HANDLER)
LOGGER.setLevel(level=logging.DEBUG)


def is_port_open(host: str = "example.com", port: int = 80) -> bool:
    """Function to detect if a particular port is open.

    Args:
        host: Hostname to connect to.
        port: Port number to connect on.

    Returns:
        bool:
        Returns a True flag is port is open.
    """
    try:
        sock = socket.create_connection((host, port), timeout=2)
        sock.close()
        return True
    except (ConnectionRefusedError, TimeoutError):
        return False


class EnvConfig(BaseSettings):
    """Wrapper for env variables."""

    apple_id: EmailStr
    password: str
    gmail_user: Union[str, None] = None
    gmail_pass: Union[str, None] = None
    recipient: Union[EmailStr, None] = None
    device: Union[str, None] = None
    location: Union[str, None] = None


env = EnvConfig()

validated = gc.validate_email(
    email_address=env.gmail_user.__str__(), smtp_check=is_port_open(port=smtplib.SMTP_PORT)
)
assert validated.ok, validated.json()
