import os
from telethon import TelegramClient 
from telethon.sessions import StringSession

API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
STRING_SESSION = os.environ.get('STRING_SESSION')

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

scraper = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)