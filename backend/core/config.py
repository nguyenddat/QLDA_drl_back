import os
from typing import *

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Settings(BaseModel):
    """
    Settings for the application.
    """
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SECURITY_ALGORITHM: str = os.getenv("SECURITY_ALGORITHM", "")
    
    DATABASE_URL: str = os.getenv("DB_URL",  "")

    @property
    def STATIC_DIR(self) -> str:
        """ Returns the path to the static directory."""
        return os.path.join(self.BASE_DIR, "static")

settings = Settings()