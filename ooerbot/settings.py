from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ably_key: str = Field(repr=False)

    admin_user_ids: set[int] = set()

    api_key: str = Field(repr=False)
    api_url: HttpUrl = HttpUrl("http://localhost:8000")

    discord_bot_token: str = Field(repr=False)

    log_level: str = "INFO"
