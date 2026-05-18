from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "contextual-chatbot"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    OPENAI_API_KEY: str = "sk-placeholder"
    GROQ_API_KEY: str = "gsk_placeholder"

    DATABASE_URL: str = "postgresql://chatbot:chatbot123@localhost:5432/chatbot_db"
    REDIS_URL: str = "redis://localhost:6379/0"

    VECTOR_DB_TYPE: str = "chromadb"
    CHROMA_PERSIST_DIR: str = "./data/chroma"

    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "llama-3.1-8b-instant"
    SENTIMENT_MODEL: str = "distilbert-base-uncased-finetuned-sst-2-english"
    MAX_CONTEXT_LENGTH: int = 4000

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8501"]

    SECRET_KEY: str = "my-super-secret-key-change-this-123456"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ENABLE_METRICS: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()