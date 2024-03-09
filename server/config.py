from decouple import config


class Settings:
    mongo_uri = config("MONGO_URI")
    db_name = "llm-chat-db"
    files_dir = config("FILES_STORAGE_DIR")


CONFIG = Settings()
