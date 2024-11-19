import os
from dotenv import load_dotenv, find_dotenv # type: ignore


# load environment variables from .env file
load_dotenv(find_dotenv())

config = {
    "MYSQL_DATABASE_HOST": os.getenv("WEIGHT_DB_NAME"),
    "MYSQL_DATABASE_USER": os.getenv("WEIGHT_MYSQL_DATABASE_USER"),
    "MYSQL_DATABASE_PASSWORD": os.getenv("WEIGHT_MYSQL_DATABASE_PASSWORD"),
    "MYSQL_DATABASE_DB": os.getenv("WEIGHT_MYSQL_DATABASE_DB"),
}