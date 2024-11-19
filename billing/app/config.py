import os
from dotenv import load_dotenv, find_dotenv # type: ignore


# load environment variables from .env file
load_dotenv(find_dotenv())

config = {
    "MYSQL_DATABASE_HOST": os.getenv("BILLING_DB_NAME"),
    "MYSQL_DATABASE_USER": os.getenv("BILLING_MYSQL_DATABASE_USER"),
    "MYSQL_DATABASE_PASSWORD": os.getenv("BILLING_MYSQL_DATABASE_PASSWORD"),
    "MYSQL_DATABASE_DB": 'billdb',
}