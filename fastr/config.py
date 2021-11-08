from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the FastAPI app. Override with environment variables or .env file.

    Override example:
    `export FASTR_SECRET_KEY=secret`
    """
    database_path: str = "./fastr.sqlite"
    secret_key: str = "<override_in_production>"

    class Config:
        env_prefix = "fastr_"
        env_file = ".env"
