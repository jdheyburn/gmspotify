from typing import List, Set

import jsonpickle
import munch
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import config

_SP_REDIRECT_URL = 'http://localhost:8888/callback/'
_SP_SCOPE = 'user-library-modify'


class SpArtist():
    id: str
    name: str

    def __init__(self, obj: munch.Munch) -> None:
        self.id = obj.id
        self.name = obj.name

    def __eq__(self, other):
        if type(other) != type(self):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __str__(self):
        return jsonpickle.encode(self)


class SpAlbumTrack():
    artists: List[SpArtist]
    disc_number: int
    id: str
    title: str
    track_number: int

    def __init__(self, obj: munch.Munch) -> None:
        self.artists = [SpArtist(artist) for artist in obj.artists]
        self.disc_number = obj.disc_number
        self.id = obj.id
        self.title = obj.name
        self.track_number = obj.track_number

    def __eq__(self, other):
        if type(other) != type(self):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __str__(self):
        return jsonpickle.encode(self)


class SpAlbum():
    id: str
    title: str
    artists: List[SpArtist]
    tracks: List[SpAlbumTrack]
    label: str
    album_type: str
    release_date: str  # TODO convert to date obj?
    total_tracks: int
    disc_count: Set[int]

    def __init__(self, obj: dict) -> None:
        munched_obj = munch.munchify(obj)
        self.id = munched_obj.id
        self.title = munched_obj.name
        self.artists = [SpArtist(artist) for artist in munched_obj.artists]
        self.tracks = [SpAlbumTrack(track)
                       for track in munched_obj.tracks['items']]
        self.label = munched_obj.label
        self.album_type = munched_obj.album_type
        self.release_date = munched_obj.release_date
        self.total_tracks = munched_obj.total_tracks
        self.disc_count = set([track.disc_number for track in self.tracks])

    def __eq__(self, other):
        if type(other) != type(self):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __str__(self):
        return jsonpickle.encode(self)


class SpQueryAlbum():
    album_type: str
    artists: List[SpArtist]
    id: str
    title: str
    release_date: str
    total_tracks: int

    def __init__(self, obj: munch.Munch) -> None:
        self.album_type = obj.album_type
        self.artists = [SpArtist(artist) for artist in obj.artists]
        self.id = obj.id
        self.title = obj.name
        self.release_date = obj.release_date
        self.total_tracks = obj.total_tracks

    def __eq__(self, other):
        if type(other) != type(self):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __str__(self):
        return jsonpickle.encode(self)


class SpQueryAlbumsResp():
    total: int
    items: List[SpQueryAlbum]

    def __init__(self, obj: munch.Munch) -> None:
        self.total = obj['total']
        self.items = [SpQueryAlbum(munch.munchify(album))
                      for album in obj['items']]

    def __eq__(self, other):
        if type(other) != type(self):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __str__(self):
        return jsonpickle.encode(self)


class SpQueryRespWrapper():
    albums: SpQueryAlbumsResp

    def __init__(self, obj: dict) -> None:
        self.albums = SpQueryAlbumsResp(obj['albums'])

    def __eq__(self, other):
        if type(other) != type(self):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __str__(self):
        return jsonpickle.encode(self)
        


class SpQueryBuilder():
    album: str
    artist: str
    year: str

    def __init__(self, album: str = '',
                 album_artist: str = '', year: str = ''):
        self.album = album
        self.artist = album_artist
        self.year = year

    def build(self) -> str:
        built_query = ''
        for key, val in vars(self).items():
            if val:
                built_query += f'{key}:{val} '
        return built_query.strip()

    def __str__(self):
        return jsonpickle.encode(self)


class SpApi():
    client: spotipy.Spotify

    def __init__(self, id: str, secret: str) -> None:
        ccm = SpotifyClientCredentials(
            client_id=id,
            client_secret=secret
        )
        self.client = spotipy.Spotify(client_credentials_manager=ccm)

    def get_album_by_id(self, id: str) -> SpAlbum:
        return SpAlbum(self.client.album(id))

    def query_album_by_title(self, title: str) -> SpQueryRespWrapper:
        q = SpQueryBuilder(album=title).build()
        return self.execute_query(q)

    def query_album_by_title_and_artist(self,
                                        title: str,
                                        artist: str) -> SpQueryRespWrapper:
        q = SpQueryBuilder(album=title, album_artist=artist).build()
        return self.execute_query(q)

    def execute_query(self, q: str) -> SpQueryRespWrapper:
        return SpQueryRespWrapper(self.client.search(q=q, type='album'))


def get_sp_api():
    username = config.get_username()
    token = util.prompt_for_user_token(
        username,
        _SP_SCOPE,
        client_id=config.get_sp_client_id(),
        client_secret=config.get_sp_client_secret(),
        redirect_uri=_SP_REDIRECT_URL
    )
    return spotipy.Spotify(auth=token)
