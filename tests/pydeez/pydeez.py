from unittest import TestCase
from src.pydeez import PyDeez
from grappa import expect
from unittest.mock import patch, call
from tests.helper import build_response_mock
from tests.mock_data.three_tracks_if_1_playlist_matches_that_has_3_tracks import (
    one_moo_playlist, three_track_playlist)
from tests.mock_data.four_tracks_if_2_playlists_match_each_one_with_2_tracks import (
    two_moo_playlists, moo_match_track_playlist, moo_too_track_playlist)


class TestPyDeez(TestCase):

    @patch('src.pydeez.helper.requests')
    def test_no_tracks_if_no_playlists_match(self, mock_requests):
        """
        Given there are no playlists that start with 'moo'
         When you get the track ids for those playlists
         Then you get an empty list
        """
        mock_requests.get.return_value = build_response_mock({'data': []})
        pydeez = PyDeez('access-token')
        track_ids = pydeez.get_track_ids_for_playlists(lambda playlist_name: playlist_name.startswith('moo'))
        track_ids | expect.to.have.length.of(0)

    @patch('src.pydeez.helper.requests')
    def test_three_tracks_if_1_playlist_matches_that_has_3_tracks(self, mock_requests):
        """
        Given there is 1 playlist that start with 'moo' that has 3 tracks
         When you get the track ids for that playlist
         Then you get 3 tracks back
        """
        mock_requests.get.side_effect = [
            build_response_mock(one_moo_playlist), build_response_mock(three_track_playlist)
        ]
        pydeez = PyDeez('access-token')
        track_ids = pydeez.get_track_ids_for_playlists(lambda playlist_name: playlist_name.startswith('moo'))

        track_ids | expect.to.be.equal.to(['track-1', 'track-2', 'track-3'])
        (mock_requests.get.call_args_list |
            expect.to.be.equal([
                call('http://api.deezer.com/user/me/playlists', params={'access_token': 'access-token', 'expires': 0}),
                call('http://api.deezer.com/playlist/2/tracks', params={'access_token': 'access-token', 'expires': 0})
            ]))

    @patch('src.pydeez.helper.requests')
    def test_four_tracks_if_2_playlists_match_each_one_with_2_tracks(self, mock_requests):
        """
        Given there are 2 playlists that start with 'moo', each with 2 tracks
         When you get the track ids for playlists that start with 'moo'
         Then you get 4 tracks back
        """
        mock_requests.get.side_effect = [
            build_response_mock(two_moo_playlists),
            build_response_mock(moo_match_track_playlist),
            build_response_mock(moo_too_track_playlist)
        ]
        pydeez = PyDeez('access-token')
        track_ids = pydeez.get_track_ids_for_playlists(lambda playlist_name: playlist_name.startswith('moo'))

        track_ids | expect.to.be.equal.to(
            ['moo-match-track-1', 'moo-match-track-2', 'moo-too-track-1', 'moo-too-track-2'])
        (mock_requests.get.call_args_list |
            expect.to.be.equal([
                call('http://api.deezer.com/user/me/playlists', params={'access_token': 'access-token', 'expires': 0}),
                call('http://api.deezer.com/playlist/2/tracks', params={'access_token': 'access-token', 'expires': 0}),
                call('http://api.deezer.com/playlist/3/tracks', params={'access_token': 'access-token', 'expires': 0})
            ]))

