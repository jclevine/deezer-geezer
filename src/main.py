from src.randeezer import randeezer
from src.pydeez import PyDeez
from os import environ

access_token = environ['ACCESS_TOKEN']
pydeez = PyDeez(access_token)


def playlist_filter(name):
    return name.startswith('awesome') or name.startswith('0') or name.startswith('new')


with open('C:\\Users\hodor\\Desktop\\all_music_20180919.txt', 'a', encoding='utf-8') as track_info_file:
    randeezer(pydeez, playlist_filter, new_playlist_prefix='please', track_infos_file=track_info_file)
