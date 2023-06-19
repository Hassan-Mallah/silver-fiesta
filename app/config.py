from pydantic import BaseSettings


# get values from .env
class Settings(BaseSettings):
    mongo_username: str
    mongo_password: str

    class Config:
        env_file = ".env"
