import re
import pytz
import logging
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait
from config import Config
from bot import Bot
from asyncio.exceptions import TimeoutError
from database import save_data

logger = logging.getLogger(__name__)

end_msg_id = ""
skip_no = ""
caption = ""
channel_id_ = ""
IST = pytz.timezone('Asia/Kolkata')
OWNER = int(Config.OWNER_ID)

@Client.on_message(filters.private & filters.command(["index"]))
async def run(bot, message):
    if message.from_user.id != OWNER:
        await message.reply_text("Who the hell are you!!")
        return
    while True:
        try:
            chat = await bot.ask(text = "To Index a channel you may send me the channel username without @", chat_id = message.from_user.id, filters=filters.text, timeout=30)
            channel=chat.text
        except TimeoutError:
            await bot.send_message(message.from_user.id, "Error!!\n\nRequest timed out.\nRestart by using /index")
            return

        source = chat.text.strip()
        chat = await bot.get_chat(source)
        chat_id = chat.username
        if not chat_id:
            await chat.reply_text("invalid username, chek username and send Again without @")
            continue
        

    
    channel_id_=chat_id

    while True:
        try:
            SKIP = await bot.ask(
                text="Send me from where you want to start forwarding\nSend 0 for from the beginning.",
                chat_id=message.from_user.id,
                filters=filters.text,
                timeout=30
            )
            logger.info(SKIP.text)
        except TimeoutError:
            return await bot.send_message(message.from_user.id, "Error!!\n\nRequest timed out.\nRestart by using /index")

        try:
            skip_no = int(SKIP.text)
            break
        except ValueError:
            await SKIP.reply_text("That's an invalid ID. It should be an integer.")
            continue

    while True:
        try:
            LIMIT = await bot.ask(
                text="Send me from Upto what extent(LIMIT) do you want to Index\nSend 0 for all messages.",
                chat_id=message.from_user.id,
                filters=filters.text,
                timeout=30
            )
            logger.info(LIMIT.text)
        except TimeoutError:
            return await bot.send_message(message.from_user.id, "Error!!\n\nRequest timed out.\nRestart by using /index")

        try:
            limit_no = int(LIMIT.text)
            break
        except ValueError:
            await LIMIT.reply_text("That's an invalid ID. It should be an integer.")
            continue

    while True:
        try:
            end_id = await bot.ask(
                text="Send me forward ending msg id",
                chat_id=message.from_user.id,
                filters=filters.text,
                timeout=30
            )
            logger.info(end_id.text)
        except TimeoutError:
            return await bot.send_message(message.from_user.id, "Error!!\n\nRequest timed out.\nRestart by using /index")

        try:
            end_msg_id = int(end_id.text)
            break
        except ValueError:
            await end_id.reply_text("That's an invalid ID. It should be an integer.")
            continue

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("All Messages", callback_data="all")
            ],
            [
                InlineKeyboardButton("Document", callback_data="docs"),
                InlineKeyboardButton("Photos", callback_data="photos")
            ],
            [
                InlineKeyboardButton("Videos", callback_data="videos"),
                InlineKeyboardButton("Audios", callback_data="audio")
            ]
        ]
    )

    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"Ok,\nNow choose what type of messages you want to forward.",
        reply_markup=buttons
    )

@Client.on_callback_query()
async def cb_handler(bot: Client, query: CallbackQuery):
    filter = ""
    if query.data == "docs":
        filter = MessageMediaType.DOCUMENT
    elif query.data == "all":
        filter = "empty"
    elif query.data == "photos":
        filter = MessageMediaType.PHOTO
    elif query.data == "videos":
        filter = MessageMediaType.VIDEO
    elif query.data == "audio":
        filter = MessageMediaType.AUDIO
    caption = None
    await query.message.delete()

    while True:
        try:
            get_caption = await bot.ask(
                text="Do you need a custom caption?\n\nIf yes, send me the caption.\n\nIf No, send '0'",
                chat_id=query.from_user.id,
                filters=filters.text,
                timeout=30
            )
        except TimeoutError:
            await bot.send_message(query.from_user.id, "Error!!\n\nRequest timed out.\nRestart by using /index")
            return

        input_caption = get_caption.text
        if input_caption == "0":
            caption = None
        else:
            caption = input_caption
        break

    m = await bot.send_message(
        text="Indexing Started",
        chat_id=query.from_user.id
    )

    msg_count = 0
    mcount = 0
    FROM=str(channel_id_)
    lst_msg_id=end_msg_id
    chat=FROM
    CURRENT=int(skip_no)
    try:
        async for msg in bot.iter_messages(chat, lst_msg_id, CURRENT):
            if msg.empty:
                continue
            msg_caption = ""
            if caption is not None:
                msg_caption = caption
            elif msg.caption:
                msg_caption = msg.caption

            if filter in [MessageMediaType.DOCUMENT, MessageMediaType.VIDEO, MessageMediaType.AUDIO, MessageMediaType.PHOTO]:
                media = getattr(msg, msg.media.value, None)
                if media is not None:
                    file_type = msg.media.value
                    id = media.file_id
            elif filter == "empty":
                for media_type in [MessageMediaType.DOCUMENT, MessageMediaType.VIDEO, MessageMediaType.AUDIO, MessageMediaType.PHOTO]:
                    media = getattr(msg, msg.media.value, None)
                    if media is not None:
                        file_type = msg.media.value
                        id = media.file_id
                        break
                else:
                    id = f"{FROM}_{msg.id}"
                    file_type = "others"

            message_id = msg.id

            try:
                await save_data(id, channel, message_id, msg_caption, file_type)
            except Exception as e:
                logger.exception(e)
                await bot.send_message(OWNER, f"LOG-Error-{e}")
                pass

            msg_count += 1
            mcount += 1
            new_skip_no = str(skip_no + msg_count)
            logger.info(f"Total Indexed: {msg_count} - Current SKIP_NO: {new_skip_no}")

            if mcount == 100:
                try:
                    datetime_ist = datetime.now(IST)
                    ISTIME = datetime_ist.strftime("%I:%M:%S %p - %d %B %Y")
                    await m.edit(text=f"Total Indexed: <code>{msg_count}</code>\nCurrent skip_no: <code>{new_skip_no}</code>\nLast edited at {ISTIME}")
                    mcount -= 100
                except FloodWait as e:
                    logger.info(f"Floodwait {e.value}")  
                    pass
                except Exception as e:
                    await bot.send_message(chat_id=OWNER, text=f"LOG-Error: {e}")
                    logger.exception(e)
                    pass

        await m.edit(f"Succesfully Indexed <code>{msg_count}</code> messages.")

    except Exception as e:
        logger.exception(e)
        await m.edit(text=f"Error: {e}")
        pass
