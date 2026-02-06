import os
from dotenv import load_dotenv

# .env file se variables load karne ke liye
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_super_secret_key_12345')
    MYSQL_HOST = os.getenv('DB_HOST')
    MYSQL_PORT = int(os.getenv('DB_PORT', 26713))
    MYSQL_USER = os.getenv('DB_USER')
    MYSQL_PASSWORD = os.getenv('DB_PASSWORD')
    MYSQL_DB = os.getenv('DB_NAME')