import telebot
from os import environ
from extra import *
# Nuevo import para poder enviar cosas inline

# Declaración del bot
bot = telebot.TeleBot(environ['TELEGRAM_TOKEN'])
bot.delete_webhook()

# Declaración de los comandos
@bot.message_handler(commands=['start'])
def start_handler(m):
  "Función que maneja los usuarios que inician"
  cid = m.chat.id
  if not is_user(cid):
    uid = m.from_user.id
    uname = m.from_user.first_name
    # Comprobamos el idioma del usuario y en caso de tener Español o Inglés, lo autodetectamos y lo guardamos
    # con ese idioma. En caso de que el mensaje venga sin idioma o el idioma del usuario no lo tengamos en
    # nuestra base de datos de idiomas, le asignamos Inglés.
    try:
      language = m.from_user.language_code[:2] if m.from_user.language_code[:2] in ['en', 'es'] else 'en'
    except:
      language = 'en'
    add_user(cid, language)
    bot.send_message(cid, responses['start'][language].format(uname, uid), parse_mode="Markdown")

@bot.message_handler(commands=['stop'])
def stop_handler(m):
  "Función que maneja los usuarios que paran el bot"
  cid = m.chat.id
  uid = m.from_user.id
  uname = m.from_user.first_name
  if is_user(cid):
    bot.send_message(cid, responses['stop'][lang(cid)].format(uname, uid), parse_mode="Markdown")
    delete_user(cid)

@bot.message_handler(commands=['lang'], func=lambda m: is_user(m.chat.id))
def lang_handler(m):
  "Función para actualizar el idioma del bot"
  cid = m.chat.id
  bot.send_message(cid, responses['lang'][lang(cid)], reply_markup=keyboard if lang(cid) == 'es' else keyboard_2, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data in ['en', 'es'])
def callback_handler(call):
  "Función para manejar el uso de los botones para cambiar el idioma"
  cid = call.message.chat.id
  mid = call.message.message_id
  language = call.data
  update_lang(cid, language)
  bot.edit_message_text(responses['lang_updated'][lang(cid)], cid, mid, reply_markup=keyboard if language == 'es' else keyboard_2, parse_mode="Markdown")

@bot.message_handler(commands=['help'], func=lambda m: is_user(m.chat.id))
def help_handler(m):
  "Función que proporciona ayuda a los usuarios"
  cid = m.chat.id
  bot.send_message(cid, responses['help'][lang(cid)].format(bot.get_me().first_name, bot.get_me().id, bot.get_me().username.replace('_', '\_'), bot.get_me().username), parse_mode="Markdown")

@bot.message_handler(func=lambda m: is_user(m.chat.id))
def pokemon_handler(m):
  "Función que obtiene devuelve información de un Pokémon en caso de existir"
  cid = m.chat.id
  pokemon = m.text.split()[0].lower()
  language = lang(cid)
  bot.send_message(cid, get_pokemon_info(pokemon, language), parse_mode="Markdown")

@bot.inline_handler(lambda query: True)
def inline_handler(q):
  "Función que maneja las peticiones inline devolviendo información sobre cualquier Pokémon"
  cid = q.from_user.id
  try:
    # Obtenemos el nombre del Pokémon
    pokemon = q.query.split()[0].lower()
    uid = q.from_user.id
    # Sacamos la información y el sprite para el thumb (Mirar extra.py)
    pokemon_info, sprite = get_pokemon_info(pokemon, lang(uid))
    # Creamos la respuesta siguiendo el API https://core.telegram.org/bots/api#inlinequeryresultarticle
    aux = types.InlineQueryResultArticle(
              "1",
              pokemon.capitalize(),
              types.InputTextMessageContent(pokemon_info, parse_mode="Markdown"),
              description=responses['basic_info'][lang(uid)],
              thumb_url = sprite)
    # El método pide una lista con las respuestas https://core.telegram.org/bots/api#answerinlinequery
    bot.answer_inline_query(q.id, [aux], cache_time=1)
  except:
    pass

bot.polling(True)
