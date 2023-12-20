from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    INV_LINK: str
    NOTIFICATION_LINK: str
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_ROOT_USERNAME: str
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str

    class Config:
        env_file = './.env'


settings = Settings()
