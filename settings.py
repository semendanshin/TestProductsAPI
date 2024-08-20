from pathlib import Path
from typing import Tuple, Type

from pydantic_settings import BaseSettings, JsonConfigSettingsSource, PydanticBaseSettingsSource, SettingsConfigDict


class DBSettings(BaseSettings):
    name: str
    user: str
    password: str
    host: str
    port: int

    def get_url(self, driver_with_dialect: str = 'postgresql+asyncpg') -> str:
        return f"{driver_with_dialect}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class AppSettings(BaseSettings):
    host: str = '0.0.0.0'
    port: int = 8000


class Settings(BaseSettings):
    db: DBSettings
    app: AppSettings = AppSettings()

    model_config = SettingsConfigDict(
        extra='ignore',
        json_file=Path(__file__).parent / 'settings.json',
        json_file_encoding='utf-8',
    )

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (JsonConfigSettingsSource(settings_cls),)
