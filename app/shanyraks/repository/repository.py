from datetime import datetime

from bson.objectid import ObjectId
from pymongo.database import Database

# from ..utils.security import hash_password


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id, user: dict) -> str:
        payload = {
            "user_id": user_id,
            "type": user["type"],
            "price": user["price"],
            "address": user["address"],
            "area": user["area"],
            "room_count": user["room_count"],
            "description": user["description"],
            # "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
            "media": []
        }
        print(payload)
        res = self.database["shanyraks"].insert_one(payload)
        return str(res.inserted_id)

    def get_shanyrak_by_id(self, shanyrak_id: str) -> dict | None:
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(shanyrak_id),
            }
        )
        print(shanyrak)
        return shanyrak

    # def get_user_by_email(self, email: str) -> dict | None:
    #     user = self.database["users"].find_one(
    #         {
    #             "email": email,
    #         }
    #     )
    #     return user

    def update_shanyrak_by_id(self, id: str, payload: dict) -> int:
        update_data = {k: v for k, v in payload.dict().items() if v is not None}
        res = self.database["shanyraks"].update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        return res.modified_count

    def push_shanyrak_media_by_id(self, id: str, payload: dict) -> int:
        # update_data = {k: v for k, v in payload.items() if v is not None}
        print(payload)
        res = self.database["shanyraks"].update_one(
            {"_id": ObjectId(id)},
            {"$push": payload}
        )
        return res.acknowledged

    def delete_shanyrak_by_id(self, id: str):
        self.database["shanyraks"].delete_one(
            {
                "_id": ObjectId(id)
            }
        )

    def delete_shanyrak_media_by_id(self, id: str, payload: dict):
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(id)})

        result = list(set(shanyrak["media"]) - set(payload["media"]))

        res = self.database["shanyraks"].update_one(
            {"_id": ObjectId(id)},
            {"$set": {"media": result}}
        )
        
        return res.acknowledged
