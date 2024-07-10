from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    pizz_bot_token: SecretStr
    alex_tg_token: SecretStr
    openai_token: SecretStr
    my_phone: SecretStr
    vk_password: SecretStr

    class Config:
        env_file = 'memory/config.env'
        env_file_encoding = 'utf-8'


config = Settings()
