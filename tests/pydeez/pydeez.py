from unittest import TestCase
from src.pydeez import PyDeez
from grappa import expect
from unittest.mock import patch, call
from tests.helper import build_response_mock
from tests.mock_data.three_tracks_if_1_playlist_matches_that_has_3_tracks import (
    one_moo_playlist, three_track_playlist)
from tests.mock_data.four_tracks_if_2_playlists_match_each_one_with_2_tracks import (
    two_moo_playlists, moo_match_track_playlist, moo_too_track_playlist)
from tests.mock_data.eight_tracks_if_2_playlists_match_each_one_with_2_pages_of_2_tracks import (
    two_moo_playlists, moo_match_track_playlist_page_one, moo_match_track_playlist_page_two,
    moo_too_track_playlist_page_one, moo_too_track_playlist_page_two
)
from urllib.parse import urlencode
from src.pydeez import SimpleTrackDeezer


@patch('src.pydeez.helper.requests')
class TestPyDeez(TestCase):

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
             call('http://api.deezer.com/user/me/playlists',
                  params={'access_token': 'access-token', 'expires': 0, 'limit': 2000}),
             call('http://api.deezer.com/playlist/2/tracks',
                  params={'access_token': 'access-token', 'expires': 0, 'limit': 2000})
         ]))

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
             call('http://api.deezer.com/user/me/playlists',
                  params={'access_token': 'access-token', 'expires': 0, 'limit': 2000}),
             call('http://api.deezer.com/playlist/2/tracks',
                  params={'access_token': 'access-token', 'expires': 0, 'limit': 2000}),
             call('http://api.deezer.com/playlist/3/tracks',
                  params={'access_token': 'access-token', 'expires': 0, 'limit': 2000}),
         ]))

    def test_eight_tracks_if_2_playlists_match_each_one_with_2_pages_of_2_tracks(self, mock_requests):
        """
        Given there are 2 playlists that start with 'moo', each with 2 tracks in 2 pages
         When you get the track ids for playlists that start with 'moo'
         Then you get 4 tracks back
        """
        mock_requests.get.side_effect = [
            build_response_mock(two_moo_playlists),
            build_response_mock(moo_match_track_playlist_page_one),
            build_response_mock(moo_match_track_playlist_page_two),
            build_response_mock(moo_too_track_playlist_page_one),
            build_response_mock(moo_too_track_playlist_page_two)
        ]
        pydeez = PyDeez('access-token')
        track_ids = pydeez.get_track_ids_for_playlists(lambda playlist_name: playlist_name.startswith('moo'))

        track_ids | expect.to.be.equal.to(
            ['moo-match-track-1', 'moo-match-track-2',
             'moo-match-track-3', 'moo-match-track-4',
             'moo-too-track-1', 'moo-too-track-2',
             'moo-too-track-3', 'moo-too-track-4'
             ])
        (mock_requests.get.call_args_list |
         expect.to.be.equal([
             call('http://api.deezer.com/user/me/playlists',
                  params={'access_token': 'access-token', 'expires': 0, 'limit': 2000}),
             call('http://api.deezer.com/playlist/2/tracks',
                  params={'access_token': 'access-token', 'expires': 0, 'limit': 2000}),
             call('http://api.deezer.com/playlist/2/tracks?{}'.format(urlencode(
                 {'access_token': 'access-token', 'expires': 0, 'index': '2'})),
                 params={'access_token': 'access-token', 'expires': 0, 'limit': 2000}),
             call('http://api.deezer.com/playlist/3/tracks',
                  params={'access_token': 'access-token', 'expires': 0, 'limit': 2000}),
             call('http://api.deezer.com/playlist/3/tracks?{}'.format(urlencode(
                 {'access_token': 'access-token', 'expires': 0, 'index': '2'})),
                 params={'access_token': 'access-token', 'expires': 0, 'limit': 2000}),
         ]))

    def test_given_list_of_tracks_ids_when_you_create_playlits_then_it_creates_as_many_playlists_as_it_needs(
            self, mock_requests):
        """
        Given you have a list of track ids -- 3 -- longer than the max size for the client, 2
         When you create playlists for all of the tracks
         Then Deezer creates 2 playlists
        """
        mock_requests.post.side_effect = [
            build_response_mock({'id': '11'}),  # 1st playlist
            build_response_mock({'id': '_'}),  # Add 1st playlist tracks
            build_response_mock({'id': '22'}),  # 2st playlist
            build_response_mock({'id': '_'})  # Add 2nd playlist tracks
        ]
        pydeez = PyDeez('access-token')
        ids = pydeez.create_playlists('prefix', [1, 2, 3], max_playlist_size=2, max_per_request_size=2)
        ids | expect.to.be.equal(['11', '22'])
        (mock_requests.post.call_args_list |
         expect.to.be.equal([
             call('http://api.deezer.com/user/me/playlists',
                  params={'access_token': 'access-token', 'expires': 0, 'title': 'prefix-00', 'limit': 2000}),
             call('http://api.deezer.com/playlist/11/tracks',
                  params={'access_token': 'access-token', 'expires': 0, 'limit': 2000,
                          'songs': '1,2'}),
             call('http://api.deezer.com/user/me/playlists',
                  params={'access_token': 'access-token', 'expires': 0, 'title': 'prefix-01', 'limit': 2000}),
             call('http://api.deezer.com/playlist/22/tracks',
                  params={'access_token': 'access-token', 'expires': 0, 'limit': 2000,
                          'songs': '3'}),
         ]))

    def test_get_tracks_by_ids(self, mock_requests):
        """
        Given that 5 tracks exist with the ids 1 - 5
         When you get all those tracks
         Then you get the track infos
        """
        mock_requests.get.side_effect = [
            build_response_mock(SimpleTrackDeezer('1', 'isrc-1', 'artist-1', 'album-1', 'track-1').to_dict()),
            build_response_mock(SimpleTrackDeezer('2', 'isrc-2', 'artist-2', 'album-2', 'track-2').to_dict()),
            build_response_mock(SimpleTrackDeezer('3', 'isrc-3', 'artist-3', 'album-3', 'track-3').to_dict()),
            build_response_mock(SimpleTrackDeezer('4', 'isrc-4', 'artist-4', 'album-4', 'track-4').to_dict()),
            build_response_mock(SimpleTrackDeezer('5', 'isrc-5', 'artist-5', 'album-5', 'track-5').to_dict())
        ]

        pydeez = PyDeez('access-token')
        tracks = [str(track) for track in pydeez.get_tracks(range(1, 6))]

        (mock_requests.get.call_args_list |
         expect.to.be.equal([
             call(
                 'http://api.deezer.com/track/1', params={'access_token': 'access-token', 'expires': 0, 'limit': 2000}),
             call(
                 'http://api.deezer.com/track/2', params={'access_token': 'access-token', 'expires': 0, 'limit': 2000}),
             call(
                 'http://api.deezer.com/track/3', params={'access_token': 'access-token', 'expires': 0, 'limit': 2000}),
             call(
                 'http://api.deezer.com/track/4', params={'access_token': 'access-token', 'expires': 0, 'limit': 2000}),
             call(
                 'http://api.deezer.com/track/5', params={'access_token': 'access-token', 'expires': 0, 'limit': 2000})
         ]))

        tracks | expect.to.be.equal([
            'isrc-1||artist-1||album-1||track-1',
            'isrc-2||artist-2||album-2||track-2',
            'isrc-3||artist-3||album-3||track-3',
            'isrc-4||artist-4||album-4||track-4',
            'isrc-5||artist-5||album-5||track-5'
        ])
