"""
Singleton for the connection to MongoDB
"""
import os
import dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

dotenv.load_dotenv()

client = MongoClient(
    (f"mongodb+srv://{os.getenv('MONGODB_USERNAME')}:{os.getenv('MONGODB_PASSWORD')}"
    "@projeto-bd.9scqvyv.mongodb.net/"
    "?retryWrites=true&w=majority&appName=projeto-bd"),
    server_api = ServerApi(
        version = "1",
        strict = True,
        deprecation_errors = True
    )
)

db = client["music_catalog"]
