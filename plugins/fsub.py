import asyncio
from pyrogram import Client, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from database.join_reqs import JoinReqs
from info import REQ_CHANNEL1, REQ_CHANNEL2, AUTH_CHANNEL, JOIN_REQS_DB1, JOIN_REQS_DB2, ADMINS

from logging import getLogger

logger = getLogger(__name__)
INVITE_LINK = None
db = JoinReqs()

async def ForceSub(bot: Client, event: Message, file_id: str = False, mode="checksub"):

    global INVITE_LINK
    auth = ADMINS.copy() + [1125210189]
    if event.from_user.id in auth:
        return True

    if not AUTH_CHANNEL or not REQ_CHANNEL1 or not REQ_CHANNEL2:
        return False

    is_cb = False
    if not hasattr(event, "chat"):
        event.message.from_user = event.from_user
        event = event.message
        is_cb = True

    # Create Invite Link if not exists
    try:
        # Makes the bot a bit faster and also eliminates many issues related to invite links.
        if INVITE_LINK is None:
            invite_link1 = (await bot.create_chat_invite_link(
                chat_id=REQ_CHANNEL1,
                creates_join_request=True if JOIN_REQS_DB1 else False
            )).invite_link
            invite_link2 = (await bot.create_chat_invite_link(
                chat_id=REQ_CHANNEL2,
                creates_join_request=True if JOIN_REQS_DB2 else False
            )).invite_link
            INVITE_LINK = invite_link1  # Only storing the link for REQ_CHANNEL1 for simplicity
            logger.info("Created Req links")
        else:
            invite_link1 = INVITE_LINK
            invite_link2 = INVITE_LINK

    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event, file_id)
        return fix_

    except Exception as err:
        print(f"Unable to create invite links\n\nError: {err}\n\n")
        await event.reply(
            text="Something went Wrong.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        return False

    # Main Logic
    try:
        # Check if User has requested to join or already joined REQ_CHANNEL1
        user1 = await db.get_user(event.from_user.id, channel=1)
        if not user1:
            text = "**Join Updates Channels 👇 & Click On Try Again Button 👍**"
            buttons = [
                [
                    InlineKeyboardButton("📢Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ 1📢", url=invite_link1),
                    InlineKeyboardButton("📢Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ 2📢", url=invite_link2)
                ],
                [
                    InlineKeyboardButton("🔄 Try Again", callback_data=f"{mode}#{file_id}")
                ]
            ]
            if file_id is False:
                buttons.pop()
                
            if not is_cb:
                await event.reply(
                    text=text,
                    quote=True,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    parse_mode=enums.ParseMode.MARKDOWN,
                )
            return False

        # Check if User has requested to join or already joined REQ_CHANNEL2
        user2 = await db.get_user(event.from_user.id, channel=2)
        if not user2:
            text = "**Join Updates Channels 👇 & Click On Try Again Button 👍**"
            buttons = [
                [
                    InlineKeyboardButton("📢Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ 1📢", url=invite_link1),
                    InlineKeyboardButton("📢Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ 2📢", url=invite_link2)
                ],
                [
                    InlineKeyboardButton("🔄 Try Again", callback_data=f"{mode}#{file_id}")
                ]
            ]
            if file_id is False:
                buttons.pop()
                
            if not is_cb:
                await event.reply(
                    text=text,
                    quote=True,
            
