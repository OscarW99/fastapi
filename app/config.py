from pydantic import BaseSettings

# BaseSettings will read first from your computer environemnt variables and then from the values given in this class. If the variables given dont exits it will throw an error. If the variables given are of the wrong type it will throw an error.
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    # Note all these are lower case. pydantic is case insensitive so this doesn't mater.

    class Config:
        env_file = ".env"


settings = Settings()

