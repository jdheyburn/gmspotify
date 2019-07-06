import logging
from typing import List, MutableMapping, AbstractSet

from gmusicapi import Mobileclient
import jsonpickle

import config


class DuplicateTrackError(Exception):
    """Raised when the album already has a track defined for a disc"""
    pass


class GMusicTrack:
    title: str
    artist: str
    rating: str
    spotify_id: str

    def __init__(self, title: str, artist: str, rating: str = '') -> None:
        self.title = title
        self.artist = artist
        self.rating = rating

    def set_spotify_id(self, spotify_id: str) -> None:
        self.spotify_id = spotify_id

    def __eq__(self, other):
        if not isinstance(other, GMusicTrack):
            return NotImplemented
        return self.title == other.title and self.artist == other.artist

    def __hash__(self):
        return hash((self.title, self.artist))

    def __str__(self):
        return jsonpickle.encode(self)


class GMusicAlbum:
    id: str
    title: str
    album_artist: str
    year: str
    # disc_number -> Track Number -> Track
    tracks: MutableMapping[int, MutableMapping[int, GMusicTrack]]
    spotify_id: str
    whole_album_added: bool

    def __init__(self, id: str, title: str, album_artist: str, year: str = '',
                 tracks: MutableMapping[
                     int, MutableMapping[int, GMusicTrack]] = {}) -> None:
        self.id = id
        self.title = title
        self.album_artist = album_artist
        self.year = year
        self.tracks = dict(tracks)
        self.spotify_id = ''
        self.whole_album_added = False

    def set_spotify_id(self, spotify_id: str) -> None:
        self.spotify_id = spotify_id

    def set_whole_album_added(self, whole_album_added: bool) -> None:
        self.whole_album_added = whole_album_added

    def __track_exists(self, disc_num: int, track_num: int) -> bool:
        return disc_num in self.tracks and track_num in self.tracks[disc_num]

    def add_track(self, disc_num: int,
                  track_num: int, track: GMusicTrack) -> None:
        if self.__track_exists(disc_num, track_num):
            raise DuplicateTrackError
        if disc_num not in self.tracks:
            self.tracks[disc_num] = {}
        self.tracks[disc_num][track_num] = track

    def total_tracks(self) -> int:
        return sum(len(disc_tracks) for disc_tracks in self.tracks.values())

    def discs_added(self) -> AbstractSet[int]:
        return self.tracks.keys()


    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return jsonpickle.encode(self)


def parse_lib(lib: List) -> MutableMapping[str, GMusicAlbum]:
    # TODO do we need to define the type here?
    albums: MutableMapping[str, GMusicAlbum] = {}
    for track in lib:
        album_id = track['albumId']
        if album_id not in albums:
            albums[album_id] = GMusicAlbum(
                album_id,
                track['album'],
                track['albumArtist'],
                # TODO better way to handle this?
                track['year'] if 'year' in track else ''
            )
        album = albums[album_id]

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
            # TODO just raise it for now for testing implement a failsafe later
            raise e
    return albums


def filter_thumbs_down_tracks(lib):
    return [track for track in lib
            if 'rating' in track and track['rating'] == '1']


def filter_thumbs_up_tracks(lib):
    return [track for track in lib
            if 'rating' in track and track['rating'] == '5']


def get_gm_api():
    api = Mobileclient()
    if not api.oauth_login(config.get_gpm_device_id()):
        api.perform_oauth()
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
    logging.info('Total : {}'.format(len(lib)))
    logging.info('Thumbs up: {}'.format(len(tu_tracks)))
    logging.info('Thumbs down: {}'.format(len(td_tracks)))
    logging.info('Uploaded: {}'.format(len(uploaded_tracks)))
    logging.info('Added: {}'.format(len(added_tracks)))
