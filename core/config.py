from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Krishi Sakhi POC"

    class Config:
        env_file = ".env"
        extra = 'ignore'

settings = Settings()