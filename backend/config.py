from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


class Settings(BaseSettings):
    app_name: str = "Business Card Website"
    debug: bool = False

    database_path: Path = DATA_DIR / "business_card.db"

    admin_username: str
    admin_password_hash: str

    secret_key: str

    access_token_expire_minutes: int = 60

    cookie_secure: bool = False
    cookie_same_site: str = "lax"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()