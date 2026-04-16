from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    # Base Config
    ENVIRONMENT: str = "dev"
    WORKSPACE_ROOT: str = os.getcwd()
    
    # API Keys
    BAILIAN_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    
    # LLM Config
    DEFAULT_MODEL_NAME: str = "qwen3-coder-plus"
    MODEL_BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    # Database Config
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "root"
    MYSQL_DEFAULT_DB: str = ""
    MYSQL_CHARSET: str = "utf8mb4"
    
    # MongoDB Config
    MONGODB_URI: str = "mongodb://127.0.0.1:27017"
    MONGODB_DB: str = "chat"

    # Bailian RAG Config
    BAILIAN_WORKSPACE_ID: str = ""
    BAILIAN_CATEGORY_ID: str = ""
    BAILIAN_INDEX_ID: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
