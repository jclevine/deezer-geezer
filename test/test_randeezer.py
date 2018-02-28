from randeezer import randeezer
from unittest import TestCase
from unittest.mock import Mock
from src.pydeez import PyDeez


class TestMain(TestCase):

    def test_something(self):
        """
        Given no playlists that start with 'moo'
         When you try to randomize
          and save deezer id, isrc id, artist name, album name, and track title delimited by double-pipes
              into a file named nothing.txt
          and re-upload the playlists to have prefix 'yes'
         Then no file is created with any track ids
          and no playlists are created
        """

        def starts_with_moo(x): x.starts_with('moo')
        mock_client = Mock()
        mock_client.get_playlists.return_value = 'Moo!'

        randeezer(deezer_client=mock_client, playlist_name_predicate=starts_with_moo,
                  new_playlist_prefix='yes',
                  track_infos_filepath='nothing.txt')

        mock_client.get_playlists.assert_called_with(starts_with_moo)
        # Get all tracks for some set of playlists (favourites is its own url or is it a playlist?)
            # Get the playlist ids
            # Get the track ids for all those playlists
            # Unique randomize
            # Put all these ids into a file (incrementally?)
        # Read track ids from file with name for new playlists to create
            # Create new playlists in chunks and add all tracks
        # Delete old ones that you just got tracks from?


