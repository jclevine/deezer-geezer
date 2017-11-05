from random import shuffle
import requests
import json


def should_use_playlist(title):
    return (title.startswith('fun') or title.startswith('new')
            or title.startswith('Batman') or title.startswith('Lost')
            or title.startswith('Give'))


def get_all_playlist_ids():
    all_playlists = requests.get('http://api.deezer.com/user/me/playlists', params={
        'access_token': '',
        'expires': 0
    })

    playlist_ids = []

    all_playlists = json.loads(all_playlists.text)['data']
    for playlist in all_playlists:
        title = playlist['title']
        if should_use_playlist(title):
            playlist_ids.append(playlist['id'])
    return playlist_ids


def get_all_tracks():
    all_tracks = []
    for playlist_id in get_all_playlist_ids():
        tracks = get_track_ids_for('http://api.deezer.com/playlist/{}/tracks'.format(playlist_id))
        all_tracks.extend(tracks)
        print('{} has {} tracks'.format(playlist_id, len(tracks)))
    print('total tracks: {}'.format(len(all_tracks)))


def get_track_ids_for(url):
    tracks = api_call(url)
    if 'next' not in tracks:
        return [track['id'] for track in tracks['data']]
    else:
        return [track['id'] for track in tracks['data']] + get_track_ids_for(tracks['next'])


def api_call(url):
    return json.loads(
        requests.get(url, params={
            'access_token': '',
            'expires': 0
        }).text)


if __name__ == '__main__':
    get_all_tracks()
