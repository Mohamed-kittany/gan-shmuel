# app/config.py
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    MYSQL_DATABASE_HOST = os.getenv("MYSQL_DATABASE_HOST", "localhost")
    MYSQL_DATABASE_USER = os.getenv("MYSQL_DATABASE_USER", "root")
    MYSQL_DATABASE_PASSWORD = os.getenv("MYSQL_DATABASE_PASSWORD", "root")
    MYSQL_DATABASE_DB = os.getenv("MYSQL_DATABASE_DB", "billdb")
    