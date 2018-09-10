from src.pydeez.helper import json_get, get_all_pages_for


class PyDeez:
    BASE_URL = 'http://api.deezer.com'
    MY_PLAYLISTS_URL = '{}{}'.format(BASE_URL, '/user/me/playlists')
    PLAYLIST_TRACKS_URL = '{}/playlist/{{}}/tracks'.format(BASE_URL)

    def __init__(self, access_token):
        self._request_params = {'access_token': access_token, 'expires': 0}

    def get_track_ids_for_playlists(self, title_predicate):
        playlist_ids = self._get_all_playlist_ids(title_predicate)
        return self._get_track_ids_by_playlist_ids(playlist_ids) if playlist_ids else []

    def _get_all_playlist_ids(self, title_predicate):
        all_playlists = json_get(self.MY_PLAYLISTS_URL, params=self._request_params)['data']
        return [playlist['id'] for playlist in all_playlists if title_predicate(playlist['title'])]

    def _get_track_ids_by_playlist_ids(self, playlist_ids):
        all_track_ids = []
        for playlist_id in playlist_ids:
            all_track_ids.extend(self._get_track_ids_by_playlist_id(playlist_id))
        return all_track_ids

    def _get_track_ids_by_playlist_id(self, playlist_id):
        return get_all_pages_for(
            self.PLAYLIST_TRACKS_URL.format(playlist_id), self._request_params, lambda track: track['id'])
