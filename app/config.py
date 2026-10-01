from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Meeting Intelligence & Action Tracker"
    debug: bool = True

    MONGO_URL: str
    DATABASE_NAME:str = "metting_intelligence"

    GROQ_API_KEY:str

    GROQ_STT_MODEL:str = "whisper-large-v3-turbo"
    GROQ_LLM_MODEL:str = "openai/gpt-oss-120b"
    UPLOAD_DIR:str = "uploads"
    MAX_FILE_SIZE_MB:int = 100

    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8", case_sensitive=True, extra="ignore")

settings = Settings()
