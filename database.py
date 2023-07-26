from config import Config
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
import asyncio
import random
import pytz
from datetime import datetime
from database import get_search_results

IST = pytz.timezone('Asia/Kolkata')
MessageCount = 0
BOT_STATUS = "0"
status = set(int(x) for x in BOT_STATUS.split())
OWNER = int(Config.OWNER_ID)

@Client.on_message(filters.command("forward"))
async def forward(bot, message):
    if 1 in status:
        await message.reply_text("A task is already running.")
        return

    m = await bot.send_message(chat_id=OWNER, text="Started Forwarding")

    batch_size = 10  # Change this value according to your requirement
    while await get_search_results().count() != 0:
        data = await get_search_results().to_list(length=batch_size)
        if not data:
            break

        for msg in data:
            channel = msg['channel']
            file_id = msg['_id']
            message_id = msg['message_id']
            method = "bot"
            caption = msg['caption']
            file_type = msg['file_type']
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

            collection.delete_one({
                'channel': channel,
                'message_id': message_id,
                'file_type': file_type,
                'method': "bot",
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

