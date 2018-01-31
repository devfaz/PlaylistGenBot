#!/usr/bin/python
import os
import tempfile
from os import unlink
from telegram.ext import Updater
from telegram.ext import CommandHandler

from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
import logging

logging.basicConfig(ormat='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def error_callback(bot, update, error):
  raise error

updater = Updater(token=os.environ['TOKEN'])

def start(bot, update):
  print(update)
  bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)

def add(bot, update):
  print(update)
  text = update.message.text.replace('/add', '', 1)
  chat_id = update.message.chat_id

  if update.message.chat.title is not None:
    filename = update.message.chat.title + '.m3u'
  else:
    filename = str(chat_id) + '.m3u'

  f = open('/tmp/' + filename, 'a+')
  f.write(text + "\n")
  f.seek(0)
  bot.send_document(chat_id=chat_id, document=f)
  f.close()

add_handler = CommandHandler('add', add)

def reset(bot, update):
  print(update)
  chat_id = update.message.chat_id

  if update.message.chat.title is not None:
    filename = update.message.chat.title + '.m3u'
  else:
    filename = str(chat_id) + '.m3u'

  try: 
    unlink('/tmp/' + filename)
    msg = "Cleared"
  except:
    msg = "Nothing to delete"

  bot.send_message(chat_id=update.message.chat_id, text=msg)

reset_handler = CommandHandler('reset', reset)

def rem(bot, update):
  print(update)
  chat_id = update.message.chat_id
  text = update.message.text.replace('/rem ', '', 1)
  msg = "Removed lines containing " + text

  if update.message.chat.title is not None:
    filename = update.message.chat.title + '.m3u'
  else:
    filename = str(chat_id) + '.m3u'

  try:
    f = open('/tmp/' + filename, 'r')
    data = f.readlines()
    f.close()
  except:
    msg = "Unable to open file"

  try:
    f = open('/tmp/' + filename, 'w')
    for line in data:
      if text not in line:
        f.write(line)
    f.close()
  except:
    msg = "Unable to write file"

  bot.send_message(chat_id=update.message.chat_id, text=msg)
    
rem_handler = CommandHandler('rem', rem)

dispatcher = updater.dispatcher

dispatcher.add_error_handler(error_callback)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(add_handler)
dispatcher.add_handler(reset_handler)
dispatcher.add_handler(rem_handler)

updater.start_polling()

