from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    KAFKA_INSTANCE: str

    class Config:
        env_file = './.env'


settings = Settings()
