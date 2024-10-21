from pydantic_settings import BaseSettings


class Settings(BaseSettings):
   
    ENABLE_SENTRY: bool = False
    SENTRY_DSN: str = "add sentry dsn url "
    JWT_SECRET: str = "please_please_update_me_please"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 6000
    JWT_REFRESH_EXPIRATION: int = 300000



settings = Settings()