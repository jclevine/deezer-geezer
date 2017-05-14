import requests
import json


def retrieve_tracks():
    with open('album-info.json') as albums_file:
        albums = json.loads(albums_file.read())


    all_tracks = []
    for album in albums:
        response = requests.get('https://api.deezer.com/album/{}'.format(album['album_id']))
        formatted_response = json.loads(response.text)
        track_ids = [track['id'] for track in formatted_response['tracks']['data']]
        all_tracks.extend(track_ids)

    with open('all_tracks.txt', 'w') as all_tracks_file:
        all_tracks_file.writelines(['{}\n'.format(str(track)) for track in all_tracks])


if __name__ == '__main__':
    retrieve_tracks()
