from typing import Dict
import asyncio
from datetime import datetime

class UserSession:
    user_locks: Dict[str, asyncio.Lock]  # A dictionary to store locks for individual users
    user_tokens: Dict[str, str]          # Simulated storage of tokens per user
    token_expiration: Dict[str, datetime]  # Simulated storage of token expiry times per user

    def __init__(self):
        self.user_locks = {}
        self.user_tokens = {}
        self.token_expiration = {}
