from src.simple_track import SimpleTrack
import json


class SimpleTrackDeezer(SimpleTrack):
    def __init__(self, id, isrc, artist_name, album_title, title):
        SimpleTrack.__init__(self, isrc, artist_name, album_title, title)
        self._id = id

    @property
    def id(self):
        return self._id

    def to_dict(self):
        return {
            'id': self.id,
            'isrc': self.isrc,
            'title': self.title,
            'artist': {
                'name': self.artist_name
            },
            'album': {
                'title': self.album_title
            }
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(the_dict):
        return SimpleTrackDeezer(the_dict['id'], the_dict['isrc'], the_dict['artist']['name'],
                                 the_dict['album']['title'], the_dict['title'])
