from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvEnum(str, Enum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class Config(BaseSettings):
    env: EnvEnum

    sentry_enabled: bool
    sentry_dsn: str
    sentry_environment: str

    telegram_bot_token: str
    telegram_group_id: str

    webhook_secret: str

    def env_is_prod(self) -> bool:
        return self.env == EnvEnum.PRODUCTION

    def env_is_dev(self) -> bool:
        return self.env == EnvEnum.DEVELOPMENT

    def env_is_local(self) -> bool:
        return self.env == EnvEnum.LOCAL

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
