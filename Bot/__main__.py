from Bot import bot, scraper
import logging 
import os 
from telethon import events, Button
from telethon import errors
from telethon.tl.types import InputMessagesFilterDocument, InputMessagesFilterVideo

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

@bot.on(events.NewMessage(incoming=True, pattern=r'^\/request(.*)'))
async def req(request):
  chat = -1518889982
  try:
    query = request.message.text.split(' ', 1)[1]
  except IndexError:
    await request.reply('Requests are done as `/request Stepmother\'s friends`')
  keybo = []
  async for message in scraper.iter_messages(chat, search=query):
      try:
        text = message.raw_text.split('📓 :', 1)[1]
        text = text.split('\n', 1)[0]
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
    await bot.send_message(-1001375115372, text, buttons = [[
        Button.inline(
          text='Accept',
          data=f'acp_{request.sender_id}',
          )
        ],
      [
        Button.inline(
          text='Request Complete!',
          data=f'recomp_{request.sender_id}',
          )
        ]
      ])
    await request.reply("Request submitted, i will send you a notification if it is accepted or completed!")
  
@bot.on(events.NewMessage(incoming=True,pattern=r'^\/start'))
async def start(msg):
  await msg.reply('Im the manga request handler for @mAngaxX11\n\nTo request do `/request <name>`  be specific so we can take the request without asking you other questions!, and if asked questions just send the answer to the bot, and i will forward it to the admins...', buttons=[[Button.url(text='Manga18', url='https://t.me/mAngaxX11')]]) 
 
@bot.on(events.NewMessage(incoming=True,func=lambda e: (e.mentioned)))
async def reply_to_user(msg):
  repl = await msg.get_reply_message()
  try:
    user_to_message = repl.text.split('`', 1)[1]
    user_to_message = user_to_message.split('`')[0]
    user_to_message = int(user_to_message)
  except IndexError:
    user_to_message = repl.forward.from_id
  try:
    text = msg.message.text + ''
    await bot.send_message(user_to_message, msg.message.text)
  except errors.rpcerrorlist.UserIsBlockedError:
    return await msg.reply('Seems like the user blocked me...')

@bot.on(events.NewMessage(incoming=True,func=lambda e: (e.is_private)))
async def reply_to_user(msg):
  if not msg.message.text.startswith('/'):
    await msg.forward_to(-1001375115372)


@bot.on(events.CallbackQuery(pattern=b'acp_'))
async def accepter(query):
  user_to_notif = query.data.decode('UTF-8').split('_', 1)[1]
  msg_before = await query.get_message()
  msg_after = msg_before.text + '\n\n✔︎ Accepted'
  try:
    await bot.send_message(int(user_to_notif), 'Your request was accepted!')
    await query.answer('Sent notif...')
  except errors.rpcerrorlist.UserIsBlockedError:
    await query.answer('User blocked bot....')
  await query.edit(msg_after, buttons=[[Button.inline(text='Request Complete', data=f'recomp_{user_to_notif}')]])
  
@bot.on(events.CallbackQuery(pattern=b'recomp_'))
async def accepter(query):
  user_to_notif = query.data.decode('UTF-8').split('_', 1)[1]
  msg_before = await query.get_message()
  msg_after = msg_before.text + '\n\n✔︎✔︎ Completed!'
  try:
    await bot.send_message(int(user_to_notif), 'Your request was completed and uploaded in channel, Check!')
    await query.answer('Sent Notif...')
  except errors.rpcerrorlist.UserIsBlockedError:
    await query.answer('User blocked bot..')
  await query.edit(msg_after)

@bot.on(events.InlineQuery)
async def inline_search(inline):
  chat = -1001518889982
  if inline.text == '':
    await inline.answer([], switch_pm='Search in @mAngaxX11..', switch_pm_param='start')
  query = inline.text
  keybo = []
  async for message in scraper.iter_messages(chat, search=query):
      if len(keybo) > 30:
        await inline.answer([], switch_pm='Try to be a little specific...', switch_pm_param='start')
        return
      msg_id = message.id 
      link = f"https://t.me/c/{str(chat)[4:]}/{str(msg_id)}" 
      try:
        title = message.raw_text.split('📓 :', 1)[1]
        title = title.split('\n', 1)[0]
        description = message.raw_text.replace('\n', '|')
        keybo.append(
          inline.builder.article(
            title=f'{title}',
            description=f'{description}......',
            text=f'{message.text}',
            link_preview=False,
            )
          )
      except AttributeError:
        pass
      except IndexError:
        pass
  if keybo == []:
    return await inline.answer([], switch_pm='Could not find the thing you searched....', switch_pm_param='start')
  await inline.answer(keybo)
  
scraper.start()
bot.start()
bot.run_until_disconnected()
scraper.run_until_disconnected()
