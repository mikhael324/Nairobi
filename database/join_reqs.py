import motor.motor_asyncio
from pyrogram import Client
from info import JOIN_REQS_DB1, JOIN_REQS_DB2, REQ_CHANNEL1, REQ_CHANNEL2

# Define JoinReqs class based on d.code
class JoinReqs:

    def __init__(self):
        if JOIN_REQS_DB1:
            self.client1 = motor.motor_asyncio.AsyncIOMotorClient(JOIN_REQS_DB1)
            self.db1 = self.client1["JoinReqs1"]
            self.col1 = self.db1[str(REQ_CHANNEL1)]
        else:
            self.client1 = None
            self.db1 = None
            self.col1 = None

        if JOIN_REQS_DB2:
            self.client2 = motor.motor_asyncio.AsyncIOMotorClient(JOIN_REQS_DB2)
            self.db2 = self.client2["JoinReqs2"]
            self.col2 = self.db2[str(REQ_CHANNEL2)]
        else:
            self.client2 = None
            self.db2 = None
            self.col2 = None

    def isActive(self):
        return self.client1 is not None and self.client2 is not None

    async def add_user(self, user_id, first_name, username, date, channel=None):
    try:
        existing_user = await self.get_user(user_id, channel)
        if existing_user:
            print(f"User with ID {user_id} already exists in the database.")
        else:
            if channel == 1 and self.col1:
                await self.col1.insert_one({"_id": int(user_id), "user_id": int(user_id), "first_name": first_name, "username": username, "date": date})
            elif channel == 2 and self.col2:
                await self.col2.insert_one({"_id": int(user_id), "user_id": int(user_id), "first_name": first_name, "username": username, "date": date})
    except Exception as e:
        print(f"Error adding user: {e}")


    async def get_user(self, user_id, channel=None):
        if channel == 1 and self.col1:
            return await self.col1.find_one({"user_id": int(user_id)})
        elif channel == 2 and self.col2:
            return await self.col2.find_one({"user_id": int(user_id)})
        else:
            return None

    async def delete_user(self, user_id, channel):
        if channel == 1 and self.col1:
            await self.col1.delete_one({"user_id": int(user_id)})
        elif channel == 2 and self.col2:
            await self.col2.delete_one({"user_id": int(user_id)})

    async def delete_all_users(self, channel=None):
        if channel == 1 and self.col1:
            await self.col1.delete_many({})
        elif channel == 2 and self.col2:
            await self.col2.delete_many({})

    async def get_all_users_count(self, channel=None):
        count = 0
        if channel == 1 and self.col1:
            count += await self.col1.count_documents({})
        elif channel == 2 and self.col2:
            count += await self.col2.count_documents({})
        return count

# Initialize JoinReqs object
join_reqs = JoinReqs()

# Define Pyrogram client based on d.code
async def handle_join_request(client, message):
    if message.chat.id == REQ_CHANNEL1 or message.chat.id == REQ_CHANNEL2:
        user_id = message.from_user.id
        channel = 1 if message.chat.id == REQ_CHANNEL1 else 2
        await join_reqs.add_user(user_id, message.from_user.first_name, message.from_user.username, message.date, channel)
        await message.reply_text("Your join request has been received.")


        
