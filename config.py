"""
Centralize place to load all environment variables
"""

import os
import logging
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Load env variables
BASE_DIR = Path(__file__).resolve().parent

DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXP_MINUTES = os.getenv("ACCESS_TOKEN_EXP_MINUTES")
REFRESH_TOKEN_EXP_MINUTES = os.getenv("REFRESH_TOKEN_EXP_MINUTES")

RESET_PASSWORD_EXP_MINUTES = os.getenv("RESET_PASSWORD_EXP_MINUTES")

FROM_EMAIL = os.getenv("FROM_EMAIL")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
DEFAULT_RECIPIENT_EMAIL = os.getenv("DEFAULT_RECIPIENT_EMAIL")


# Logging config
def get_logger(name) -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)
    return logger
