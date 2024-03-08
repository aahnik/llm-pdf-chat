from decouple import config


class Settings:
    mongo_uri = config("MONGO_URI")
    db_name = "llm-chat-db"


CONFIG = Settings()
