from Bot import bot, scraper
import logging 
import os 
from telethon import events, Button
from telethon import errors
from telethon.tl.types import InputMessagesFilterDocument, InputMessagesFilterVideo

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

@bot.on(events.NewMessage(incoming=True, pattern=r'^\/request(.*)'))
def req(request):
  chat = -1001518889982
  try:
    query = request.message.text.split(' ', 1)[1]
  except IndexError:
    await request.reply('Requests are done as `/request Stepmother\'s friends`')
  keybo = []
  async for message in scraper.iter_messages(chat, search=query):
      try:
        text = message.raw_text.split('📓 :', 1)[0]
        msg_id = message.id 
        link = f"https://t.me/c/{str(chat)[4:]}/{str(msg_id)}" 
        keybo.append([Button.url(text =
        f'{text[:30]}...',url= link)])
      except Exception:
        pass
  if not keybo == []:
    await request.reply('Found some results for you.., specifiy if these doesn\'t statisfy', buttons=keybo)
  else:
    req_user = f"[{request.sender.first_name}](tg://user?id={request.sender_id})" 
    text = f"Request: {query}\nRequested by: {req_user}\nRequestor Id: `{request.sender_id}`"
    await bot.send_message(-1001375115372, text, buttons = [
      [
        Button.inline(
          text='Accept',
          callback_data=f'acp_{request.sender_id}',
          )
        ]
      [
        Button.inline(
          text='Request Complete!',
          callback_data=f'recomp_{request.sender_id}',
          )
        ]
      ])
    await request.reply("Request submitted, i will send you a notification if it is accepted or completed!")
  
@bot.on(events.NewMessage(incoming=True,pattern=r'^\/start'))
def start(msg):
  await msg.reply('Im the manga request handler for @mAngaxX11\n\nTo request do `/request <name>`  be specific so we can take the request without asking you other questions!', buttons=[[Button.url(text='Manga18', url='https://t.me/mAngaxX11')]]) 
 
@bot.on(events.NewMessage(incoming=True,func=lambda e: (e.mentioned)))
async reply_to_user(msg):
  try:
    repl = await msg.get_reply_message()
    user_to_message = repl.text.split('`', 1)[1][:-1]
    try:
      await bot.send_message(int(user_to_message), text=msg.message.text)
    except errors.rpcbaseerrors.UnauthorizedError or errors.rpcbaseerrors.ForbiddenError:
      return await msg.reply('Seems like the user blocked me...')
  except IndexError:
    pass

@bot.on(events.CallbackQuery(pattern=b'acp_'))
def accepter(query):
  user_to_notif = query.data.decode('UTF-8').split('_', 1)[1]
  msg_before = query.message.text 
  msg_after = msg_before + '\n\n✔︎ Accepted'
  await query.answer('Trying to send a notif....')
  await bot.send_message(int(user_to_notif), text='Your request was accepted!')
  await query.message.edit(msg_after, buttons=[[Button.inline(text='Request Complete', callback_data=f'recomp_{user_to_notif}')]])
  
@bot.on(events.CallbackQuery(pattern=b'recomp_'))
def accepter(query):
  user_to_notif = query.data.decode('UTF-8').split('_', 1)[1]
  msg_before = query.message.text 
  msg_after = msg_before + '\n\n✔︎✔︎ Completed!'
  await query.answer('Trying to send a notif....')
  await bot.send_message(int(user_to_notif), text='Your request was completed and uploaded in channel, Check!')
  await query.message.edit(msg_after, buttons=[])
  
scraper.start()
bot.start()
bot.run_until_disconnected()
scraper.run_until_disconnected()