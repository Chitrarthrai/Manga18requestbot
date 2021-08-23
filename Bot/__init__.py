import os
from telethon import TelegramClient 
from telethon.sessions import StringSession

API_ID = int(os.enviorn.get('API_ID'))
API_HASH = os.enviorn.get('API_HASH')
BOT_TOKEN = os.enviorn.get('BOT_TOKEN')
STRING_SESSION = os.enviorn.get('STRING_SESSION')

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

scraper = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)