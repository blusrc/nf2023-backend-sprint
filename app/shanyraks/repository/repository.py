from datetime import datetime
from bson.objectid import ObjectId
from pymongo.database import Database


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
            "created_at": datetime.utcnow(),
            "media": []
        }
        # print(payload)
        res = self.database["shanyraks"].insert_one(payload)
        return str(res.inserted_id)

    def get_shanyrak_by_id(self, shanyrak_id: str) -> dict | None:
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
        # print(shanyrak)
        return shanyrak

    def update_shanyrak_by_id(self, id: str, payload: dict) -> int:
        update_data = {k: v for k, v in payload.dict().items() if v is not None}
        res = self.database["shanyraks"].update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        return res.modified_count

    def push_shanyrak_media_by_id(self, id: str, payload: dict) -> int:
        # print(payload)
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

    def post_comment(self, user_id, shanyrak_id, content: str) -> str:
        payload = {
            "content": content,
            "author_id": user_id,
            "shanyrak_id": shanyrak_id,
            "created_at": datetime.utcnow(),
        }
        self.database["comments"].insert_one(payload)
        return content

    def get_comments_shanyrak_by_id(self, shanyrak_id: str):
        query = {"shanyrak_id": shanyrak_id}
        projection = {"_id": 0}

        comments = self.database["comments"].find(query, projection)
        comments_list = [comment for comment in comments]

        return {"comments": comments_list}

    def get_comment_by_id(self, id: str):
        comment = self.database["comments"].find_one({"_id": ObjectId(id)})
        return comment.dict()

    def update_comment_by_id(self, comment_id: str, new_content: str):
        res = self.database["comments"].update_one(
            {"_id": ObjectId(comment_id)},
            {"$set": {"content": new_content}}
        )
        return res.acknowledged

    def delete_comment_by_id(self, comment_id) :
        self.database["comments"].delete_one({
            "_id": ObjectId(comment_id)
        })
