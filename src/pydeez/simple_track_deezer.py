from src.simple_track import SimpleTrack


class SimpleTrackDeezer(SimpleTrack):
    def __init__(self, id, isrc, artist_name, album_title, title):
        super(SimpleTrack, self).__init__(isrc, artist_name, album_title, title)
        self._id = id

    @property
    def id(self):
        return self._id

