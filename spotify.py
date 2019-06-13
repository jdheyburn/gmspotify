import config
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from munch import munchify, Munch
from typing import List

_SP_REDIRECT_URL = 'http://localhost:8888/callback/'
_SP_SCOPE = 'user-library-modify'

class InvalidTypeError(Exception):
    pass

# TODO Complete these classes for Spotify response 
# class SpArtistItem():
#     id: str
#     name: str
#     def __init__(self, obj: Munch):
#         self.id = obj.id
#         self.name = obj.name

# class SpAlbumItem():
#     id: str
#     album_type: str
#     artists: List[SpArtistItem]
#     name: str
#     release_date: str
#     release_day_precision: str
#     total_tracks: int
#     def __init(self, obj: Munch):
#         if obj.type != 'album':
#             raise InvalidTypeError
#         self.id = obj.id
#         self.album_type = obj.album_type


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


class SpAlbumApiResp():
    


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


def get_sp_ccm():
    ccm = SpotifyClientCredentials(
        client_id=config.get_sp_client_id(),
        client_secret=config.get_sp_client_secret()
        )
    return spotipy.Spotify(client_credentials_manager=ccm)


def get_album_by_id(sp_api, id):
    return sp_api.album(id)


def query_album_by_artist(sp_api, album_title, album_artist) -> SpAlbumsQueryApiResp:
    query = 'album:{} artist:{}'.format(album_title, album_artist)
    return SpAlbumsQueryApiResp(sp_api.search(q=query, type='album'))


def query_albums_by_title(sp_api, album_title) -> SpAlbumsQueryApiResp:
    query = 'album:{}'.format(album_title)
    return SpAlbumsQueryApiResp(sp_api.search(q=query, type='album'))

def query_albums_by_title_year(sp_api, album_title, year) -> SpAlbumsQueryApiResp:
    query = 'album:{} year:{}'.format(album_title, year)
    return SpAlbumsQueryApiResp(sp_api.search(q=query, type='album'))



