import os
import random
from typing import TYPE_CHECKING, Any, TypedDict, Union
from typing_extensions import NotRequired

import pymongo
from disnake.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from bson import ObjectId

if TYPE_CHECKING:
    from motor.motor_asyncio import AsyncIOMotorCollection

class MotorDbManager(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        self.motor_client = False
        self.client.loop.create_task(self.start())

    async def start(self):  # TODO: use async cog_load() instead
        if not self.motor_client:
            mongo_pass = os.getenv("MONGO_DB_PASS")
            conn_str = f"mongodb+srv://Kur0:{mongo_pass}@kur0bot1.b8p3zby.mongodb.net/?retryWrites=true&w=majority"
            self.motor_client = AsyncIOMotorClient(conn_str, server_api=ServerApi("1"))
            try:
                await self.motor_client.admin.command("ping")
                print("MongoDB connection success!")
            except Exception as e:
                print(f"Tried to ping MongoDB but got this error instead: \n{e}")
        else:
            print("MotorDB already started")

    def get_collection_for_server(self, db_name: str, guild_id: Union[str, int]):
        if not isinstance(self.motor_client, bool):            
            return self.motor_client[str(db_name)][str(guild_id)]
        else:
            raise RuntimeError("Database has not been initialized")

    async def get_latest_doc(self, collec: "AsyncIOMotorCollection"):
        res: list[Any]  = await collec.find().sort("_id", pymongo.DESCENDING).to_list(length=1)  # type: ignore
        return res[0]

    async def get_random(self, coll: "AsyncIOMotorCollection"):
        """Fucky way because sample aggregation is weird for small data"""
        gif_count = await coll.count_documents({})
        chosen_idx = random.randint(1, gif_count)
        limited_list: list[Any] = await coll.find({}).to_list(chosen_idx)  # type: ignore
        return limited_list[-1]

    # def merge_dicts(self, dict1, dict2):
    # merged_dict = dict(dict1.items() | dict2.items())
    # return merged_dict


def setup(client: commands.Bot):
    client.add_cog(MotorDbManager(client))

class StatContents(TypedDict):
    _id: NotRequired[ObjectId]
    user_id: int
    stats: dict[str, Any]    

class ToggleContents(TypedDict):
    _id: NotRequired[ObjectId]
    title: str
    enabled: bool

class DadJokeVictimContents(TypedDict):
    _id: NotRequired[ObjectId]
    user_id: int
    notified: bool