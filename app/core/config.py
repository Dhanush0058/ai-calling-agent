from dotenv import load_dotenv
import os


load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME")
    APP_VERSION = os.getenv("APP_VERSION")
    DEBUG = os.getenv("DEBUG")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
    
    DATABASE_URL = os.getenv("DATABASE_URL")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


settings = Settings()