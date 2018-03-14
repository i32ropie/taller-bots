import telebot
from os import environ
from extra import *

# Declaración del bot
bot = telebot.TeleBot(environ['TELEGRAM_TOKEN'])
bot.delete_webhook()

# Declaración de los comandos
@bot.message_handler(commands=['start'])
def start_handler(m):
  "Función que maneja los usuarios que inician"
  cid = m.chat.id
  uid = m.from_user.id
  uname = m.from_user.first_name
  if not is_user(cid):
    add_user(cid)
    message = "Welcome [{}](tg://user?id={})!\n\nTo see how this bot works, type /help"
    bot.send_message(cid, message.format(uname, uid), parse_mode="Markdown")

@bot.message_handler(commands=['stop'])
def stop_handler(m):
  "Función que maneja los usuarios que paran el bot"
  cid = m.chat.id
  uid = m.from_user.id
  uname = m.from_user.first_name
  if is_user(cid):
    delete_user(cid)
    bot.send_message(cid, "Bye [{}](tg://user?id={})!".format(uname, uid), parse_mode="Markdown")

@bot.message_handler(commands=['help'], func=lambda m: is_user(m.chat.id))
def help_handler(m):
  "Función que proporciona ayuda a los usuarios"
  cid = m.chat.id
  message = "Welcome to [{}](tg://user?id={}).\n\nThe usage of this bot is really simple, just type the name of any Pokémon and if it exists, I will show you some information about it :D"
  bot.send_message(cid, message.format(bot.get_me().first_name, bot.get_me().id), parse_mode="Markdown")

@bot.message_handler(func=lambda m: is_user(m.chat.id))
def pokemon_handler(m):
  "Función que obtiene devuelve información de un Pokémon en caso de existir"
  cid = m.chat.id
  pokemon = m.text.split()[0].lower()
  bot.send_message(cid, get_pokemon_info(pokemon), parse_mode="Markdown")

bot.polling(True)
