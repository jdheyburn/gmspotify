from typing import List

import munch
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import config

_SP_REDIRECT_URL = 'http://localhost:8888/callback/'
_SP_SCOPE = 'user-library-modify'

class SpAlbumApiResp():
    def __init__(self, obj: dict):
        self.__dict__.update(munch.munchify(obj))
    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        return self.__dict__ == other.__dict__

# Wrapper around items since munch is still a dict
class SpAlbumsQueryApiResp():
    album_items: List
    total: int

    def __init__(self, obj: dict):
        if 'albums' not in obj:
            raise AttributeError()
        munched_obj = munch.munchify(obj)
        self.total = munched_obj.albums.total
        self.album_items = munch.munchify(munched_obj.albums['items'])


class SpQueryBuilder():
    album: str
    artist: str
    year: str

    def __init__(self, album: str='', album_artist: str='', year: str=''):
        self.album = album
        self.artist = album_artist
        self.year = year

    def build(self) -> str:
        built_query = ''
        for key, val in vars(self).items():
            if val:
                built_query += f'{key}:{val} '
        return built_query.strip()


class SpApi():
    client: spotipy.Spotify

    def __init__(self, id: str, secret: str) -> None:
        ccm = SpotifyClientCredentials(
            client_id=id,
            client_secret=secret
        )
        self.client = spotipy.Spotify(client_credentials_manager=ccm)

    def get_album_by_id(self, id: str) -> SpAlbumApiResp:
        return SpAlbumApiResp(self.client.album(id))

    def execute_query(self, q: str) -> SpAlbumsQueryApiResp:
        return SpAlbumsQueryApiResp(self.client.search(q=q, type='album'))


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
