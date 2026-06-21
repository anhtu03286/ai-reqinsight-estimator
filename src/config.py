from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_env: str = "development"
    secret_key: str
    jwt_secret: str
    jwt_access_expire_minutes: int = 15
    jwt_refresh_expire_days: int = 7

    database_url: str
    database_sync_url: str

    redis_url: str = "redis://localhost:6379/0"

    storage_endpoint: str = "http://localhost:9000"
    storage_access_key: str = "minioadmin"
    storage_secret_key: str = "minioadmin"
    storage_bucket: str = "reqinsight-documents"
    storage_use_ssl: bool = False

    llm_provider: str = "claude"
    anthropic_api_key: str = ""
    voyage_api_key: str = ""
    azure_openai_api_key: str = ""
    azure_openai_endpoint: str = ""

    tesseract_cmd: str = "/usr/bin/tesseract"
    debug: bool = False

    # PM integrations
    jira_url: str = ""
    jira_email: str = ""
    jira_api_token: str = ""
    linear_api_key: str = ""
    clickup_api_token: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
