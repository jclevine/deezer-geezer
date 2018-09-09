class SimpleTrack:

    def __init__(self, isrc, artist_name, album_title, title):
        self._isrc = isrc
        self._artist_name = artist_name
        self._album_title = album_title
        self._title = title

    @property
    def isrc(self):
        return self._isrc

    @property
    def artist_name(self):
        return self._artist_name

    @property
    def album_title(self):
        return self._album_title

    @property
    def title(self):
        return self._title

    def __eq__(self, other):
        if isinstance(other, SimpleTrack):
            return self.isrc == other.isrc
        raise NotImplementedError()

    @property
    def __dict__(self):
        return {
            'isrc': self.isrc, 'artist_name': self.artist_name, 'album_title': self.album_title, 'title': self.title
        }

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self):
        return '{}||{}||{}||{}'.format(self.isrc, self.artist_name, self.album_title, self.title)

    def __str__(self):
        return self.__repr__()
