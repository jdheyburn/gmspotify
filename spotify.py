import config
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

_SP_REDIRECT_URL = 'http://localhost:8888/callback/'
_SP_SCOPE = 'user-library-modify'

# TODO Complete these classes for Spotify response 
class SpArtistItem():
    id: str
    name: str
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']

class SpAlbumItem():
    album_type: str
    artists



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


def query_album_by_artist(sp_api, album_title, album_artist):
    query = 'album:{} artist:{}'.format(album_title, album_artist)
    return sp_api.search(q=query, type='album')


def query_albums_by_title(sp_api, album_title):
    query = 'album:{}'.format(album_title)
    return sp_api.search(q=query, type='album')

def query_albums_by_title_year(sp_api, album_title, year):
    query = 'album:{} year:{}'.format(album_title, year)
    return sp_api.search(q=query, type='album')



