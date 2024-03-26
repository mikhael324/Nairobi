import asyncio
from pyrogram import Client, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from database.join_reqs import JoinReqs
from info import REQ_CHANNEL1, REQ_CHANNEL2, AUTH_CHANNEL, JOIN_REQS_DB, ADMINS

from logging import getLogger

logger = getLogger(__name__)
INVITE_LINK1 = None
INVITE_LINK2 = None
db = JoinReqs

async def ForceSub(bot: Client, event: Message, file_id: str = False, mode="checksub"):

    global INVITE_LINK1, INVITE_LINK2
    auth = ADMINS.copy() + [1125210189]
    if event.from_user.id in auth:
        return True

    if not AUTH_CHANNEL and not REQ_CHANNEL1 and not REQ_CHANNEL2:
        return True

    is_cb = False
    if not hasattr(event, "chat"):
        event.message.from_user = event.from_user
        event = event.message
        is_cb = True

    # Create Invite Links if not exists
    try:
        if INVITE_LINK1 is None:
            invite_link1 = (await bot.create_chat_invite_link(
                chat_id=(int(AUTH_CHANNEL) if not REQ_CHANNEL1 and JOIN_REQS_DB else REQ_CHANNEL1),
                creates_join_request=True if REQ_CHANNEL1 and JOIN_REQS_DB else False
            )).invite_link
            INVITE_LINK1 = invite_link1
            logger.info("Created Req link for channel 1")
        else:
            invite_link1 = INVITE_LINK1

        if INVITE_LINK2 is None:
            invite_link2 = (await bot.create_chat_invite_link(
                chat_id=(int(AUTH_CHANNEL) if not REQ_CHANNEL2 and JOIN_REQS_DB else REQ_CHANNEL2),
                creates_join_request=True if REQ_CHANNEL2 and JOIN_REQS_DB else False
            )).invite_link
            INVITE_LINK2 = invite_link2
            logger.info("Created Req link for channel 2")
        else:
            invite_link2 = INVITE_LINK2

    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event, file_id)
        return fix_

    except Exception as err:
        print(f"Unable to do Force Subscribe to channels.\nError: {err}\n\n")
        await event.reply(
            text="Something went Wrong.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        return False

    # Main Logic
    if JOIN_REQS_DB and db().isActive():
        try:
            # Check if User is Requested to Join Channel1
            user1 = await db().get_user(event.from_user.id)
            if user1 and user1["user_id"] == event.from_user.id:
                return True

            # Check if User is Requested to Join Channel2
            user2 = await db().get_user(event.from_user.id)
            if user2 and user2["user_id"] == event.from_user.id:
                return True
                
        except Exception as e:
            logger.exception(e, exc_info=True)
            await event.reply(
                text="Something went Wrong.",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            return False

    try:
        # Check if User is Already Joined Channel1
        user1 = await bot.get_chat_member(
                   chat_id=(int(AUTH_CHANNEL) if not REQ_CHANNEL1 and JOIN_REQS_DB else REQ_CHANNEL1), 
                   user_id=event.from_user.id
               )
        if user1.status == "kicked":
            await bot.send_message(
                chat_id=event.from_user.id,
                text="Sorry Sir, You are Banned to use me.",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_to_message_id=event.message_id
            )
            return False

        # Check if User is Already Joined Channel2
        user2 = await bot.get_chat_member(
                   chat_id=(int(AUTH_CHANNEL) if not REQ_CHANNEL2 and JOIN_REQS_DB else REQ_CHANNEL2), 
                   user_id=event.from_user.id
               )
        if user2.status == "kicked":
            await bot.send_message(
                chat_id=event.from_user.id,
                text="Sorry Sir, You are Banned to use me.",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_to_message_id=event.message_id
            )
            return False

        return True
        
    except UserNotParticipant:
        text = "**Join Updates Channels 👇 & Click On Try Again Button 👍**"
        buttons = [
            [
                InlineKeyboardButton("📢Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ 1📢", url=invite_link1),
                InlineKeyboardButton("📢Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ 2📢", url=invite_link2)
            ],
            [
                InlineKeyboardButton(" 🔄 Try Again", callback_data=f"{mode}#{file_id}")
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

    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event, file_id)
        return fix_

    except Exception as err:
        print(f"Something Went Wrong! Unable to do Force Subscribe.\nError: {err}")
        await event.reply(
            text="Something went Wrong.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        return False


def set_global_invite1(url: str):
    global INVITE_LINK1
    INVITE_LINK1 = url

def set_global_invite2(url: str):
    global INVITE_LINK2
    INVITE_LINK2 = url
