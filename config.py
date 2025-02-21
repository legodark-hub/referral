from dotenv import load_dotenv
import os

load_dotenv()

MODE = os.getenv("MODE")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
JWT_SECRET_KEY = os.getenv("JWT_SECRET")
