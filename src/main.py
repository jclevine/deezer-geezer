from src.randeezer import randeezer
from src.pydeez import PyDeez
from os import environ


access_token = environ['ACCESS_TOKEN']
pydeez = PyDeez(access_token)
track_ids = pydeez.get_track_ids_for_playlists(lambda x: x.startswith('awesome'))
print(track_ids)
# randeezer()
