from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    slack_token: str = Field(..., description="Slack Bot User OAuth Token")
    default_hours: int = Field(default=4, description="Default hours to look back")
    batch_size: int = Field(default=100, description="Number of messages to fetch per batch")
    delay_between_requests: float = Field(default=0.5, description="Delay between API requests in seconds")
    delay_between_deletions: float = Field(default=1.0, description="Delay between message deletions")
    
    class Config:
        env_file = ".env"
        env_prefix = "SLACK_CLEANUP_"

try:
    settings = Settings()
except ValidationError as e:
    error_messages = []
    for error in e.errors():
        if error["type"] == "missing":
            field = error["loc"][0]
            error_messages.append(f"Missing required environment variable: SLACK_CLEANUP_{field.upper()}")
    
    if error_messages:
        raise ValueError("\n".join(error_messages))
    raise