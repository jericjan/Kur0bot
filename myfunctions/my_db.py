# goofy ahh synchronous mongodb function, will be replacing with motor.py

from typing import Any
from pymongo import MongoClient
import os

def get_db(db_name: str):

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    PASS = os.getenv("MONGO_DB_PASS")
    CONNECTION_STRING = f"mongodb+srv://Kur0:{PASS}@kur0bot1.b8p3zby.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client: MongoClient[Any] = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[db_name]
