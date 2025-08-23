from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL : str
    ## add the variable and variable type in .env file
    ## Note: var name should match that in .env file
    setting = SettingsConfigDict(
        env_file= "backend/.env",
        extra= "ignore"
    )

setting = Settings()