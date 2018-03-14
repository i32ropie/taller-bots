import json
import requests

# Cargamos los usuarios
with open('usuarios.json') as f: usuarios = json.load(f)

# Funciones de ayuda
def save_users():
  "Guarda los usuarios en nuestro fichero de usuarios"
  with open('usuarios.json', 'w') as f: json.dump(usuarios, f, indent=2)

def is_user(cid):
  "Comprueba si un ID es usuario de nuestro bot"
  return usuarios.get(str(cid))

def add_user(cid):
  "Añade un usuario"
  usuarios[str(cid)] = True
  save_users()

def delete_user(cid):
  "Borra un usuario"
  usuarios[str(cid)] = False
  save_users()

# Funciones para obtener información de los pokemon
url = "https://pokeapi.co/api/v2/{}"

def get_pokemon_info(pokemon):
  "Obtiene información básica de un Pokémon"
  r = requests.get(url.format('pokemon/{}'.format(pokemon)))
  # Comprobamos si la petición tuvo éxito
  if r.status_code != 200:
    return "Error. Pokémon not found"
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
  # Los tipos (Viene una lista con los tipos en minúscula)
  # Aquí estamos usando list comprehension http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Comprehensions.html
  poke_info['types'] = [x['type']['name'].capitalize() for x in r_json['types']]
  # Habilidades (Viene como los tipos)
  poke_info['abilities'] = [x['ability']['name'].capitalize() for x in r_json['abilities']]
  # Sprite del pokemon (Viene una lista y cogeremos solo la parte de alante por defecto)
  poke_info['sprite'] = r_json['sprites']['front_default']
  # Generamos el mensaje a enviar utilizando la información del pokemon
  # OJO, lo que hay entre los corchetes de antes del sprite es un caracter vacío
  # que utilizaremos para enviar la imagen desde la URL
  message = "[⁣]({sprite})Pokémon: *{name}*\nHeight: *{height}* m\nWeight: *{weight}* kg\nTypes:\n*\t· {types}*\nAbilities:\n*\t· {abilities}*".format(
            sprite = poke_info['sprite'], name = poke_info['name'], types = "\n\t· ".join(poke_info['types']),
            abilities = "\n\t· ".join(poke_info['abilities']), height = poke_info['height'], weight = poke_info['weight'])
  return message, poke_info['sprite']
