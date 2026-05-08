from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "CloudNAS"
    api_prefix: str = "/api/v1"
    secret_key: str = "cloudnas-secret"
    local_storage_path: str = "/tmp/cloudnas_storage"

    class Config:
        env_file = ".env"

settings = Settings()
