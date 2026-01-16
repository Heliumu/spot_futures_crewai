# config/settings.py
"""
应用配置
"""
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # API配置
    DATA_SERVICE_URL: str = "http://localhost:8000"
    MAX_RETRIES: int = 3
    REQUEST_TIMEOUT: int = 30
    
    # Agent配置
    AGENT_TIMEOUT: int = 300  # 5分钟
    MAX_ITERATIONS: int = 15
    
    # 缓存配置
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # 1小时
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"

settings = Settings()
