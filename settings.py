from datetime import datetime

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    company: str = 'Тинькофф Банк'
    year: int = Field(default=datetime.now().year)


settings = Settings()
