from random import sample
import requests
import json


ACCESS_TOKEN = ''


def should_use_playlist(title):
    return title.startswith('new') or title.startswith('super')


def get_all_playlist_ids():
    all_playlists = requests.get('http://api.deezer.com/user/me/playlists', params={
        'access_token': ACCESS_TOKEN,
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
    # Make into a unique set
    all_tracks = sample(all_tracks, len(all_tracks))

    with open('all_tracks.txt', 'w') as all_tracks_file:
        all_tracks_file.writelines(['{}\n'.format(str(track)) for track in all_tracks])


def upload_tracks(track_filepath):
    with open(track_filepath, 'r') as all_tracks_file:
        all_tracks = all_tracks_file.read().splitlines()

    playlist_chunks = [all_tracks[i:i + 2000] for i in range(0, len(all_tracks), 2000)]

    for i, playlist in enumerate(playlist_chunks):
        new_playlist_id = create_playlist(i, playlist)

        chunk_size = 10
        subplaylist_chunks = [playlist[i:i + chunk_size] for i in range(0, len(playlist), chunk_size)]
        added_count = 0
        for subplaylist in subplaylist_chunks:

            add_playlist_chunk(new_playlist_id, subplaylist)

            updated_playlist = api_call('https://api.deezer.com/playlist/{}'.format(new_playlist_id))

            if not all_tracks_added(updated_playlist['nb_tracks'], added_count + chunk_size):
                print(','.join(subplaylist))
            added_count = updated_playlist['nb_tracks']
            print('Size: {}'.format(updated_playlist['nb_tracks']))


def all_tracks_added(updated_playlist_count, expected_playlist_count):
    return updated_playlist_count == expected_playlist_count


def add_playlist_chunk(playlist_id, playlist):
    requests.post('http://api.deezer.com/playlist/{}/tracks'.format(playlist_id), params={
        'songs': ','.join(playlist),
        'access_token': ACCESS_TOKEN,
        'expires': 0
    })


def create_playlist(i, playlist):
    print('Playlist {} has {} tracks'.format(i, len(playlist)))
    playlist_title = 'super-fun-{}'.format(i)
    response = requests.post('http://api.deezer.com/user/me/playlists', params={
        'title': playlist_title,
        'access_token': ACCESS_TOKEN,
        'expires': 0
    })

    return json.loads(response.text)['id']


def get_track_ids_for(url):
    tracks = api_call(url)
    if 'next' not in tracks:
        return [track['id'] for track in tracks['data']]
    else:
        return [track['id'] for track in tracks['data']] + get_track_ids_for(tracks['next'])


def api_call(url):
    return json.loads(
        requests.get(url, params={
            'access_token': ACCESS_TOKEN,
            'expires': 0
        }).text)


if __name__ == '__main__':
    get_all_tracks()
    upload_tracks('all_tracks.txt')
