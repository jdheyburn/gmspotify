import config
import spotipy
import spotipy.util as util

_SP_REDIRECT_URL = 'http://localhost'
_SP_SCOPE = 'user-library-modify'


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


