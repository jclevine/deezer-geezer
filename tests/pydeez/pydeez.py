from unittest import TestCase
from src.pydeez import PyDeez
from grappa import expect


class TestPyDeez(TestCase):

    def test(self):
        """
        Given there are no playlists that start with 'moo'
         When you get the track ids for those playlists
         Then you get an empty list
        """
        pydeez = PyDeez()
        track_ids = pydeez.get_track_ids_for_playlists(lambda playlist_name: playlist_name.startswith('moo'))
        track_ids | expect.to.have.length.of(0)

