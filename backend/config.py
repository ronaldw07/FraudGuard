# Author: Ronald Wen
# config.py - Centralized application configuration and secret loading

import os

from dotenv import load_dotenv

load_dotenv()

ALGORITHM = 'HS256'

JWT_SECRET = os.getenv('JWT_SECRET')
if not JWT_SECRET:
    raise RuntimeError(
        'JWT_SECRET environment variable is required. '
        'Set it to a strong, random value before starting the app.'
    )
