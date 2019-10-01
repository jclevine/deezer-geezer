from src.randeezer import randeezer
from unittest import TestCase
from unittest.mock import Mock, patch
from src.simple_track import SimpleTrack


class TestRandeezer(TestCase):

    @patch('src.randeezer.writelines')
    def test_no_playlists_no_nothing(self, mock_write):
        """
        Given no playlists that start with 'moo'
         When you try to randomize
          and save deezer id, isrc id, artist name, album name, and track title delimited by double-pipes
              into a file named nothing.txt
          and re-upload the playlists to have prefix 'yes'
         Then no file is created with any track ids
          and no playlists are created
        """
        mock_client = Mock()
        mock_client.get_track_ids_for_playlists.return_value = []
        mock_track_infos_file = Mock()

        playlist_name_predicate = 'starts_with_moo'
        randeezer(deezer_client=mock_client, playlist_name_predicate=playlist_name_predicate,
                  new_playlist_prefix='yes', track_infos_file=mock_track_infos_file)
        mock_client.get_track_ids_for_playlists.assert_called_with(playlist_name_predicate)
        mock_write.assert_not_called()
        mock_client.create_playlist.assert_not_called()

    @patch('src.randeezer.uniq_randomize_list', side_effect=lambda x: list(reversed(x)))
    @patch('src.randeezer.writelines')
    def test_playlist_with_tracks_randomizes_saves_info_and_makes_new_list_and_does_not_delete_old_playlists(
            self, mock_write, _):
        """
        Given there is one playlist that start with 'moo'
          and that playlist has 3 tracks
         When you try to randomize (which is a mock that reverses the list order)
          and save deezer id, isrc id, artist name, album name, and track title delimited by double-pipes
              into a file named track_infos.txt
          and re-upload the playlists to have prefix 'yes'
         Then the tracks are reversed/uniqued
          and the 3 tracks reversed are uploaded into a playlist 'yes'
          and the track info is saved properly into a file track_infos.txt
          and old 'moo' playlist is not deleted
        """
        mock_client = Mock()
        mock_client.get_track_ids_for_playlists.return_value = ['1', '2', '3']
        mock_client.get_tracks.return_value = [
            SimpleTrack('3-isrc', '3-artist-name', '3-album-title', '3-title'),
            SimpleTrack('2-isrc', '2-artist-name', '2-album-title', '2-title'),
            SimpleTrack('1-isrc', '1-artist-name', '1-album-title', '1-title')
        ]

        mock_track_info_file = Mock()

        playlist_name_predicate = 'starts_with_moo'
        randeezer(deezer_client=mock_client, playlist_name_predicate=playlist_name_predicate,
                  new_playlist_prefix='yes', track_infos_file=mock_track_info_file,
                  do_delete_old_playlists=False)

        mock_client.get_track_ids_for_playlists.assert_called_with(playlist_name_predicate)
        mock_client.create_playlists.assert_called_with('yes', ['3', '2', '1'])
        mock_client.get_tracks.assert_called_with(['3', '2', '1'], mock_track_info_file)
        mock_write.assert_called_with(mock_track_info_file, [
            '3-isrc||3-artist-name||3-album-title||3-title',
            '2-isrc||2-artist-name||2-album-title||2-title',
            '1-isrc||1-artist-name||1-album-title||1-title'
        ])

        mock_client.delete_playlists.assert_not_called()

    #     # Get all tracks for some set of playlists (favourites is its own url or is it a playlist?)
    #         # Get the playlist ids
    #         # Get the track ids for all those playlists
    #         # Unique randomize
    #         # Put all these ids into a file (incrementally?)
    #     # Read track ids from file with name for new playlists to create
    #         # Create new playlists in chunks and add all tracks
    #     # Delete old ones that you just got tracks from?


