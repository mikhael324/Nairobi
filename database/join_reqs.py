import motor.motor_asyncio
from info import REQ_CHANNEL1, REQ_CHANNEL2

class JoinReqs:

    def __init__(self):
        from info import JOIN_REQS_DB
        if JOIN_REQS_DB:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(JOIN_REQS_DB)
            self.db = self.client["JoinReqs"]
            self.col1 = self.db[str(REQ_CHANNEL1)] if REQ_CHANNEL1 else None
            self.col2 = self.db[str(REQ_CHANNEL2)] if REQ_CHANNEL2 else None
        else:
            self.client = None
            self.db = None
            self.col1 = None
            self.col2 = None

    def isActive(self):
        return self.client is not None

    async def add_user(self, user_id, first_name, username, date, channel):
        try:
            if channel == 1 and self.col1:
                await self.col1.insert_one({"_id": int(user_id), "user_id": int(user_id), "first_name": first_name, "username": username, "date": date})
            elif channel == 2 and self.col2:
                await self.col2.insert_one({"_id": int(user_id), "user_id": int(user_id), "first_name": first_name, "username": username, "date": date})
        except Exception as e:
            print(f"Error adding user: {e}")

    async def get_user(self, user_id, channel):
        if channel == 1 and self.col1:
            user = await self.col1.find_one({"user_id": int(user_id)})
            return user
        elif channel == 2 and self.col2:
            user = await self.col2.find_one({"user_id": int(user_id)})
            return user

    async def get_all_users(self, channel):
        users = []
        if channel == 1 and self.col1:
            users.extend(await self.col1.find().to_list(None))
        elif channel == 2 and self.col2:
            users.extend(await self.col2.find().to_list(None))
        return users

    async def delete_user(self, user_id, channel):
        if channel == 1 and self.col1:
            await self.col1.delete_one({"user_id": int(user_id)})
        elif channel == 2 and self.col2:
            await self.col2.delete_one({"user_id": int(user_id)})

    async def delete_all_users(self, channel):
        if channel == 1 and self.col1:
            await self.col1.delete_many({})
        elif channel == 2 and self.col2:
            await self.col2.delete_many({})

    async def get_all_users_count(self, channel):
        count = 0
        if channel == 1 and self.col1:
            count += await self.col1.count_documents({})
        elif channel == 2 and self.col2:
            count += await self.col2.count_documents({})
        return count
        
