from src.pydeez.helper import json_get, get_all_pages_for, json_post
from src.common import flatten, chunk_list


class PyDeez:
    BASE_URL = 'http://api.deezer.com'
    MY_PLAYLISTS_URL = '{}{}'.format(BASE_URL, '/user/me/playlists')
    PLAYLIST_TRACKS_URL = '{}/playlist/{{}}/tracks'.format(BASE_URL)
    MAX_PLAYLIST_SIZE = 2000

    def __init__(self, access_token):
        self._request_params = {'access_token': access_token, 'expires': 0, 'limit': self.MAX_PLAYLIST_SIZE}

    def get_track_ids_for_playlists(self, title_predicate):
        playlist_ids = self._get_all_playlist_ids(title_predicate)
        return self._get_track_ids_by_playlist_ids(playlist_ids) if playlist_ids else []

    def create_playlist(self, title):
        request_params = self._request_params.copy()
        request_params['title'] = title
        return json_post(self.MY_PLAYLISTS_URL, params=request_params)['id']

    def create_playlists(self, playlist_name_prefix, track_ids, max_playlist_size=2000, max_per_request_size=100):
        new_playlist_ids = []
        chunked_track_ids = chunk_list(track_ids, max_playlist_size)
        for i, playlist_tracks in enumerate(chunked_track_ids):
            playlist_name = self._build_playlist_name(playlist_name_prefix, i)
            new_playlist_id = self.create_playlist(playlist_name)
            request_chunks = chunk_list(playlist_tracks, max_per_request_size)
            for request_chunk in request_chunks:
                # TODO: jlevine - Handle error if add_tracks_to_playlist returns False rather than True
                self.add_tracks_to_playlist(new_playlist_id, request_chunk)
            new_playlist_ids.append(new_playlist_id)
        return new_playlist_ids

    def add_tracks_to_playlist(self, playlist_id, track_ids):
        request_params = self._request_params.copy()
        request_params['songs'] = ','.join([str(id) for id in track_ids])
        return json_post(self.PLAYLIST_TRACKS_URL.format(playlist_id), params=request_params)

    @staticmethod
    def _build_playlist_name(prefix, number):
        return '{0}-{1:0>2}'.format(prefix, number)

    def _get_all_playlist_ids(self, title_predicate):
        all_playlists = json_get(self.MY_PLAYLISTS_URL, params=self._request_params)['data']
        return [playlist['id'] for playlist in all_playlists if title_predicate(playlist['title'])]

    def _get_track_ids_by_playlist_ids(self, playlist_ids):
        return flatten([self._get_track_ids_by_playlist_id(playlist_id) for playlist_id in playlist_ids])

    def _get_track_ids_by_playlist_id(self, playlist_id):
        return get_all_pages_for(
            self.PLAYLIST_TRACKS_URL.format(playlist_id), self._request_params, lambda track: track['id'])
