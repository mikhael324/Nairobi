from logging import getLogger
from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest, Message
from database.join_reqs import JoinReqs
from info import ADMINS, REQ_CHANNEL1, REQ_CHANNEL2

db = JoinReqs()
logger = getLogger(__name__)

@Client.on_chat_join_request(filters.chat(REQ_CHANNEL1 if REQ_CHANNEL1 else "self"))
async def join_reqs1(client, join_req: ChatJoinRequest):
    if db.isActive():
        user_id = join_req.from_user.id
        first_name = join_req.from_user.first_name
        username = join_req.from_user.username
        date = join_req.date

        await db.add_user(
            user_id=user_id,
            first_name=first_name,
            username=username,
            date=date
        )

@Client.on_chat_join_request(filters.chat(REQ_CHANNEL2 if REQ_CHANNEL2 else "self"))
async def join_reqs2(client, join_req: ChatJoinRequest):
    if db.isActive():
        user_id = join_req.from_user.id
        first_name = join_req.from_user.first_name
        username = join_req.from_user.username
        date = join_req.date

        await db.add_user(
            user_id=user_id,
            first_name=first_name,
            username=username,
            date=date
        )

@Client.on_message(filters.command("totalrequests1") & filters.private & filters.user((ADMINS.copy() + [1125210189])))
async def total_requests1(client, message):
    if db.isActive():
        total = await db.get_all_users_count(channel=1)
        await message.reply_text(
            text=f"Total Requests for Channel 1: {total}",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )

@Client.on_message(filters.command("purgerequests1") & filters.private & filters.user(ADMINS))
async def purge_requests1(client, message):
    if db.isActive():
        await db.delete_all_users(channel=1)
        await message.reply_text(
            text="Purged All Requests for Channel 1.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )

@Client.on_message(filters.command("totalrequests2") & filters.private & filters.user((ADMINS.copy() + [1125210189])))
async def total_requests2(client, message):
    if db.isActive():
        total = await db.get_all_users_count(channel=2)
        await message.reply_text(
            text=f"Total Requests for Channel 2: {total}",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )

@Client.on_message(filters.command("purgerequests2") & filters.private & filters.user(ADMINS))
async def purge_requests2(client, message):
    if db.isActive():
        await db.delete_all_users(channel=2)
        await message.reply_text(
            text="Purged All Requests for Channel 2.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
)
        
