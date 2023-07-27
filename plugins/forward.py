from config import Config
from pyrogram import Client, filters, enums
from database import Data, save_data, get_search_results
import asyncio
from pyrogram.errors import FloodWait
import random
from pyrogram.errors.exceptions.bad_request_400 import FileReferenceEmpty, FileReferenceExpired, MediaEmpty
import pytz
from datetime import datetime

IST = pytz.timezone('Asia/Kolkata')
MessageCount = 0
BOT_STATUS = "0"
status = set(int(x) for x in BOT_STATUS.split())
OWNER = int(Config.OWNER_ID)

@Client.on_message(filters.command("status"))
async def count(bot, m):
    if 1 in status:
        await m.reply_text("Currently Bot is forwarding messages.")
    if 1 not in status and 2 not in status:
        await m.reply_text("Bot is Idle now, You can start a task.")

@Client.on_message(filters.command('total'))
async def total(bot, message):
    msg = await message.reply("Counting total messages in DB...", quote=True)
    try:
        total = await Data.count_documents()
        await msg.edit(f'Total Messages: {total}')
    except Exception as e:
        await msg.edit(f'Error: {e}')

@Client.on_message(filters.command('cleardb'))
async def clrdb(bot, message):
    msg = await message.reply("Clearing files from DB...", quote=True)
    try:
        await Data.collection.drop()
        await msg.edit(f'Cleared DB')
    except Exception as e:
        await msg.edit(f'Error: {e}')

@Client.on_message(filters.command("forward"))
async def forward(bot, message):
    if 1 in status:
        await message.reply_text("A task is already running.")
        return

    m = await bot.send_message(chat_id=OWNER, text="Started Forwarding")

    while await Data.count_documents() != 0:
        data = await get_search_results()
        for msg in data:
            channel = msg.channel
            file_id = msg.id
            message_id = msg.message_id
            method = "bot"
            caption = msg.caption
            file_type = msg.file_type
            chat_id = Config.TO_CHANNEL

            try:
                if file_type in (enums.MessageMediaTyp.DOCUMENT,
                                 enums.MessageMediaTyp.VIDEO, 
                                 enums.MessageMediaTyp.AUDIO, 
                                 enums.MessageMediaTyp.PHOTO):
                    await bot.send_cached_media(
                        chat_id=chat_id,
                        file_id=file_id,
                        caption=caption
                    )
                else:
                    await bot.copy_message(
                        chat_id=chat_id,
                        from_chat_id=channel,
                        parse_mode=enums.ParseMode.MARKDOWN,
                        caption=caption,
                        message_id=message_id
                    )
                await asyncio.sleep(1)

                try:
                    status.add(1)
                except:
                    pass

            except FloodWait as e:
                await asyncio.sleep(e.x)
                if file_type in (enums.MessageMediaTyp.DOCUMENT, 
                                 enums.MessageMediaTyp.VIDEO, 
                                 enums.MessageMediaTyp.AUDIO, 
                                 enums.MessageMediaTyp.PHOTO):
                    await bot.send_cached_media(
                        chat_id=chat_id,
                        file_id=file_id,
                        caption=caption
                    )
                else:
                    await bot.copy_message(
                        chat_id=chat_id,
                        from_chat_id=channel,
                        parse_mode=enums.ParseMode.MARKDOWN,
                        caption=caption,
                        message_id=message_id
                    )
                await asyncio.sleep(1)

            except Exception as e:
                print(e)
                pass

            await Data.collection.delete_one({
                'channel': channel,
                'message_id': message_id,
                'file_type': file_type,
                'use': "forward"
            })

            MessageCount += 1

            try:
                datetime_ist = datetime.now(IST)
                ISTIME = datetime_ist.strftime("%I:%M:%S %p - %d %B %Y")
                await m.edit(text=f"Total Forwarded: <code>{MessageCount}</code>\nForwarded Using: Bot\nSleeping for {1} Seconds\nLast Forwarded at {ISTIME}")
            except Exception as e:
                print(e)
                await bot.send_message(chat_id=OWNER, text=f"LOG-Error: {e}")
                pass

    print("Finished")

    try:
        await m.edit(text=f'Successfully Forwarded {MessageCount} messages')
    except Exception as e:
        await bot.send_message(OWNER, e)
        print(e)
        pass

    try:
        status.remove(1)
    except:
        pass

    MessageCount = 0
