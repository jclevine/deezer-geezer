from unittest import TestCase, skip
from unittest.mock import patch
from album_info_finder import get_album_infos, strip_parenthetical_nonsense, extract_album_info


class TestAlbumInfoFinder(TestCase):

    def test_get_one_album_info(self):
        albums = get_album_infos(['./A Tribe Called Quest/Midnight Marauders'])
        self.assertEqual(1207252, albums[0]['album_id'])

    # @skip('Implement when you got something working, maybe')
    # def test_get_no_album_info(self):
    #     pass
    #
    # @skip('Implement when you got something working, maybe')
    # def test_get_empty_album_info(self):
    #     pass
    #
    def test_get_two_album_infos(self):
        albums = get_album_infos(['./A Tribe Called Quest/Midnight Marauders', './Apoptygma Berzerk/7'])

        self.assertEqual(1207252, albums[0]['album_id'])
        self.assertEqual(3393801, albums[1]['album_id'])
    #
    # @patch('album_info_finder.logging')
    # def test_log_no_album_found(self, logging):
    #     albums = get_album_infos(['./Bobby Knight/Does Not Exist'])
    #     self.assertEqual(0, len(albums))
    #     logging.warning.assert_called_with('Album Not Found: Bobby Knight | Does Not Exist')

    def test_ignore_parenthetical_nonsense(self):
        parenthetical_nonsense = 'This Is A Good Album (Remastered To The Max!)'
        self.assertEqual('This Is A Good Album', strip_parenthetical_nonsense(parenthetical_nonsense))

    def test_get_failing_album(self):
        albums = get_album_infos(['./Depeche Mode/Songs of Faith and Devotion'])
        self.assertEqual(1, len(albums))

# Bauhaus | The Sky's Gone Out
    def test_get_another_failing_album(self):
        albums = get_album_infos(["./Bauhaus/The Sky's Gone Out"])
        self.assertEqual(1, len(albums))

# DJ Shadow | Endtroducing...._
    def test_yet_another_failing_album(self):
        albums = get_album_infos(["./DJ Shadow/Endtroducing..."])
        self.assertEqual(1, len(albums))

    def test_split_normal_album(self):
        album_title = './An Artist/An Album'
        parts = extract_album_info(album_title)
        self.assertEqual(('An Artist', 'An Album'), parts)

    def test_split_apostrophe_album(self):
        album_title = './An Artist/An Album\'s Fun'
        parts = extract_album_info(album_title)
        self.assertEqual(('An Artist', "An Album\\'s Fun"), parts)
