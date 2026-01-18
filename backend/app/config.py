from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    groq_api_key: str
    tavily_api_key: str
    model_name: str = "Llama3-8b-8192"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
