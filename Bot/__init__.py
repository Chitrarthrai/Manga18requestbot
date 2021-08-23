import os
from telethon.sync import TelegramClient 
from telethon.sessions import StringSession

API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
string = os.environ.get('STRING')
if string:
  print('Session loaded..')

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

scraper = TelegramClient(StringSession(string), API_ID, API_HASH)