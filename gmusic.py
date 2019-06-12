from typing import MutableMapping

from gmusicapi import Mobileclient

import config


class DuplicateTrackError(Exception):
    """Raised when the album already has a track defined for a disc"""
    pass


class GMusicTrack:
    title: str
    artist: str
    rating: str

    def __init__(self, title: str, artist: str, rating: str = '') -> None:
        self.title = title
        self.artist = artist
        self.rating = rating

    def __eq__(self, other):
        if not isinstance(other, GMusicTrack):
            return NotImplemented
        return self.title == other.title and self.artist == other.artist

    def __hash__(self):
        return hash((self.title, self.artist))


class GMusicAlbum:
    id: str
    title: str
    album_artist: str
    year: str
    # DiscNumber -> Track Number -> Track
    tracks: MutableMapping[int, MutableMapping[int, GMusicTrack]]

    def __init__(self, id: str, title: str, album_artist: str, year: str = '',
                 tracks: MutableMapping[int, MutableMapping[int, GMusicTrack]] = {}) -> None:
        self.id = id
        self.title = title
        self.album_artist = album_artist
        self.year = year
        self.tracks = {}

    def __track_exists(self, discNum: int, trackNum: int) -> bool:
        return discNum in self.tracks and trackNum in self.tracks[discNum]

    def add_track(self, discNum: int, trackNum: int, track: GMusicTrack) -> None:
        if self.__track_exists(discNum, trackNum):
            raise DuplicateTrackError
        if discNum not in self.tracks:
            self.tracks[discNum] = {}
        self.tracks[discNum][trackNum] = track

    def __eq__(self, other):
        if not isinstance(other, GMusicAlbum):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


def parse_lib(lib: List) -> MutableMapping[str, GMusicAlbum]:
    # TODO do we need to define the type here?
    albums: MutableMapping[str, GMusicAlbum] = {}
    for track in lib:
        albumId = track['albumId']
        if albumId not in albums: 
            albums[albumId] = GMusicAlbum(
                id,
                track['album'],
                track['albumArtist'],
                track['year'] if 'year' in track else '' # TODO better way to handle this?
            )
        album = albums[albumId]
    
        try:
            album.add_track(
                track['discNumber'], 
                track['trackNumber'], GMusicTrack(
                    track['title'],
                    track['artist'],
                    track['rating'] if 'rating' in track else ''
                )
            )
        except DuplicateTrackError as e:
            # TODO just raise it for now for testing, implement a failsafe later
            raise e
    return albums


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
