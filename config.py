from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MARKERS_DB_URL"))
aws_region = os.getenv("REGION")
access_key = os.getenv('ACCESS_KEY')
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASS")
secret_access_key = os.getenv('SECRET_ACCESS_KEY')

prerana_db = client["prerana"]
prusers_collection = prerana_db["users"]
