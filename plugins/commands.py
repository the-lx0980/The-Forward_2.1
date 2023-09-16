import os
from config import Config
from pyrogram import Client, filters
import asyncio
import sys

START_MSG="Hi {},\nThis is a simple bot to forward all messages from one channel to other" 
HELP_MSG="Available commands:-\n\n/index - To index a channel\n/forward - To start forwarding\n/total - Count total messages in DB\n/status - Check Current status\n/help - Help data\n/stop - To stop all running processes. \n\nUse /index to index messages from a channel to database.\n\nAfter indexing you can start forwarding by using /forward.\n\n<b>Note:</b>\nYou will require the following data to index a channel:-\n\n<b>Channel Invite Link</b>:- If channel is a Private channel User needs to join channel to acces the messages. Please note that do not leave channel until forwarding completes.\n\n<b>Channel ID</b>:- If channel is a private channel you may need to enter Channel ID. Get it from @ChannelidHEXbot.\n\n<b>SKIP_NO</b>:-From where you want to start Forwarding files.Give 0 if from starting"

@Client.on_message(filters.private & filters.command('start'))
async def start(client, message):
    await client.send_message(
        chat_id=message.chat.id,
        text=START_MSG.format(message.from_user.mention)
    )

@Client.on_message(filters.command("stop"))
async def stop_button(bot, message):
    if message.from_user.id not in Config.OWNER_ID:
        return
    msg = await bot.send_message(
        text="Stoping all processes...",
        chat_id=message.chat.id
    )
    await asyncio.sleep(1)
    await msg.edit("All Processes Stopped and Restarted")
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_message(filters.private & filters.command('help'))
async def help(client, message):
    await client.send_message(
        chat_id=message.chat.id,
        text=HELP_MSG
    )
