import os

import pymongo
from disnake.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi


class MotorDbManager(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.motor_client = False
        self.client.loop.create_task(self.start())

    async def start(self):
        if not self.motor_client:
            mongo_pass = os.getenv("MONGO_DB_PASS")
            conn_str = f"mongodb+srv://Kur0:{mongo_pass}@kur0bot1.b8p3zby.mongodb.net/?retryWrites=true&w=majority"
            self.motor_client = AsyncIOMotorClient(conn_str, server_api=ServerApi("1"))
            try:
                await self.motor_client.admin.command("ping")
                print("MongoDB connection success!")
            except Exception as e:
                print(e)
        else:
            print("MotorDB already started")

    async def get_collection_for_server(self, db_name, guild_id):
        return self.motor_client[str(db_name)][str(guild_id)]

    async def get_latest_doc(self, collec):
        res = await collec.find().sort("_id", pymongo.DESCENDING).to_list(length=1)
        return res[0]


def setup(client):
    client.add_cog(MotorDbManager(client))
