from random import shuffle
import requests
import json


def create_playlists():
    with open('all_tracks.txt', 'r') as all_tracks_file:
        all_tracks = all_tracks_file.read().splitlines()

    shuffle(all_tracks)
    playlist_chunks = [all_tracks[i:i + 1000] for i in range(0, len(all_tracks), 1000)]

    for i, playlist in enumerate(playlist_chunks):
        playlist_title = 'fun-{}'.format(i)
        response = requests.post('http://api.deezer.com/user/me/playlists', params={
            'title': playlist_title,
            'access_token': '',
            'expires': 0
        })

        new_playlist_id = json.loads(response.text)['id']

        subplaylist_chunks = [playlist[i:i + 15] for i in range(0, len(playlist), 15)]
        for subplaylist in subplaylist_chunks:
            requests.post('http://api.deezer.com/playlist/{}/tracks'.format(new_playlist_id), params={
                'songs': ','.join(subplaylist),
                'access_token': '',
                'expires': 0
            })

if __name__ == '__main__':
    create_playlists()
