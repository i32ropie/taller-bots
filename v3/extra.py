import json
import requests
from telebot import *

# Cargamos el archivo de respuestas
with open('responses.json') as f: responses = json.load(f)

# Cargamos los usuarios
with open('usuarios.json') as f: usuarios = json.load(f)

# Funciones de ayuda
# CAMBIADAS EN ESTA VERSIÓN YA QUE AHORA ALMACENAMOS MÁS INFORMACIÓN
def save_users():
  "Guarda los usuarios en nuestro fichero de usuarios"
  with open('usuarios.json', 'w') as f: json.dump(usuarios, f, indent=2)

def is_user(cid):
  "Comprueba si un ID es usuario de nuestro bot (ACTUALIZADA)"
  return usuarios.get(str(cid)) and usuarios[str(cid)]['active']

def add_user(cid, language):
  "Añade un usuario (ACTUALIZADA)"
  usuarios[str(cid)] = {'lang':language, 'active':True}
  save_users()

def delete_user(cid):
  "Borra un usuario (ACTUALIZADA)"
  usuarios[str(cid)]['active'] = False
  save_users()

def lang(cid):
  "Devuelve el idioma del usuario o 'en' en caso de no serlo (Para que funcione inline a todo el mundo)"
  return usuarios[str(cid)]['lang'] if is_user(cid) else 'en'

def update_lang(cid, lang):
  "Actualiza el idioma de un usuario"
  usuarios[str(cid)]['lang'] = lang
  save_users()

# Generamos el teclado a usar a la hora de actualizar el idioma
keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton('Español', callback_data='es'),
             types.InlineKeyboardButton('Inglés', callback_data='en'))

keyboard_2 = types.InlineKeyboardMarkup()
keyboard_2.add(types.InlineKeyboardButton('Spanish', callback_data='es'),
             types.InlineKeyboardButton('English', callback_data='en'))


# Funciones para obtener información de los pokemon
url = "https://pokeapi.co/api/v2/{}"

def get_pokemon_info(pokemon, language):
  "Obtiene información básica de un Pokémon en un idioma determinado"
  r = requests.get(url.format('pokemon/{}'.format(pokemon)))
  # Comprobamos si la petición tuvo éxito
  if r.status_code != 200:
    return responses['error'][language]
  # Sabiendo que ha sido una petición buena, empezamos a sacar información del pokemon
  # Primero obtendremos el json del resultado a la petición
  r_json = r.json()
  # Crearemos un diccionario donde almacenar la información del pokemon de forma cómoda
  # Para esto cogeremos una petición cualquiera y la analizaremos con http://jsonviewer.stack.hu/
  poke_info = dict()
  # Obtenemos el nombre y lo ponemos capitalizamos
  poke_info['name'] = r_json['name'].capitalize()
  # El peso (Viene en gramos)
  poke_info['weight'] = r_json['weight']/10
  # La altura (Viene en centímetros)
  poke_info['height'] = r_json['height']/10
  # EN LA VERSIÓN 3 TENEMOS VARIOS IDIOMAS, POR LO QUE CAMBIA COMO OBTENEMOS LOS TIPOS Y HABILIDADES
  # REALMENTE SEGUIMOS USANDO LIST COMPREHENSION PERO UN POCO MÁS COMPLICADO
  # Los tipos
  poke_info['types'] = [y['name'] for x in [requests.get(x['type']['url']).json()['names'] for x in r_json['types']] for y in x if y['language']['name'] == language]
  # Habilidades
  poke_info['abilities'] = [y['name'] for x in [requests.get(x['ability']['url']).json()['names'] for x in r_json['abilities']] for y in x if y['language']['name'] == language]
  # Sprite del pokemon (Viene una lista y cogeremos solo la parte de alante por defecto)
  poke_info['sprite'] = r_json['sprites']['front_default']
  # Generamos el mensaje a enviar utilizando la información del pokemon
  # OJO, lo que hay entre los corchetes de antes del sprite es un caracter vacío
  # que utilizaremos para enviar la imagen desde la URL
  message = responses['poke_info'][language].format(sprite = poke_info['sprite'],
                                                    name = poke_info['name'],
                                                    types = "\n\t· ".join(poke_info['types']),
                                                    abilities = "\n\t· ".join(poke_info['abilities']),
                                                    height = poke_info['height'],
                                                    weight = poke_info['weight'])
  return message, poke_info['sprite']
