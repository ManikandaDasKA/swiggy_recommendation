from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL:str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    CONNECTION_STRING: str

    class Config:
        env_file = ".env"

settings = Settings() 