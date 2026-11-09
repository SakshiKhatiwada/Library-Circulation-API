from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus

class Settings(BaseSettings):
    db_url: str = "sqlite:///./library.db"
    use_test_db: bool = False

    model_config = SettingsConfigDict(
        env_file=".env" if Path(".env").exists() else ".env.example",
        env_parse_json=True,
    )
    
    # @property
    # def db_url(self) -> str:
    #     if self.use_test_db:
    #         return (
    #             f"sqlite:///./{self.db_name}.db"
    #         )
    #     else:
    #         password = quote_plus(self.db_password)
    #         return (
    #             f"postgresql+psycopg://{self.db_user}:{password}@127.0.0.1:5432/{self.db_name}"
    #         )
            


settings = Settings()

# db_url = (
#     settings.TEST_DB_URL
#     if settings.USE_TEST_DB
#     else settings.DB_URL
# )