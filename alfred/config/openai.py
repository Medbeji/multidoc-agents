from pydantic import BaseSettings, Field
from typing import Optional

class OpenAIConfig(BaseSettings):
    OPENAI_API_KEY: str = Field(..., env='OPENAI_API_KEY')
    OPENAI_API_BASE: Optional[str] = Field(None, env='OPENAI_API_BASE')
    MODEL: bool = Field(default=False, env='MODEL')

    class Config:
        env_file_encoding = 'utf-8'

    def __init__(self, **values):
        super().__init__(**values)

# When creating an instance, specify the .env file path using an environment variable
openai_config = OpenAIConfig(_env_file='.env')