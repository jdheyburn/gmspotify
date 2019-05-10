from gmusicapi import Mobileclient
import config

def filter_thumbs_down_tracks(lib):
    return [track for track in lib if 'rating' in track and track['rating'] == '1']


def filter_thumbs_up_tracks(lib):
    return [track for track in lib if 'rating' in track and track['rating'] == '5']


def get_gm_api():
    api = Mobileclient()
    if not api.oauth_login(config.get_gpm_device_id()):
        res = api.perform_oauth()
        if not api.oauth_login(config.get_gpm_device_id()):
            raise ValueError("Could not authenticate")
    return api


def filter_uploaded_tracks(lib):
    return [track for track in lib if 'trackType' not in track]


def filter_added_tracks(lib):
    return [track for track in lib if 'trackType' in track]


def gen_report(lib):
    tu_tracks = filter_thumbs_up_tracks(lib)
    td_tracks = filter_thumbs_down_tracks(lib)
    uploaded_tracks = filter_uploaded_tracks(lib)
    added_tracks = filter_added_tracks(lib)
    print('Total : {}'.format(len(lib)))
    print('Thumbs up: {}'.format(len(tu_tracks)))
    print('Thumbs down: {}'.format(len(td_tracks)))
    print('Uploaded: {}'.format(len(uploaded_tracks)))
    print('Added: {}'.format(len(added_tracks)))

