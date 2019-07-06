import argparse
import logging
import pprint
import re
from typing import List, MutableMapping, Set, AbstractSet

import jsonpickle
import munch

import config
import gmusic
import spotify
import utils

logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.setLevel(logging.DEBUG)


def get_gm_track_artists(gm_track: gmusic.GMusicTrack) -> List[str]:
    artists = []
    if '&' in gm_track.artist:
        artists = [artist.strip() for artist in gm_track.artist.split('&')]
    else:
        artists.append(gm_track.artist)
    _, ft_artists = utils.strip_ft_artist_from_title(gm_track.title)
    if ft_artists:
        artists.append(ft_artists)
    return sorted(artists)


def get_sp_track_artists(sp_track: spotify.SpAlbumTrack) -> List[str]:
    return sorted([artist.name for artist in sp_track.artists])


# def _get_all_artists_from_tracks(gm_track: gmusic.GMusicTrack,
#         s_track: munch.Munch) -> Mapping[str, List[str]]:
#     s_artists = [artist.name for artist in s_track.artists]

#     if len(s_artists) == 0:
#         raise AssertionError() # TODO this error correct?

#     gm_artists = [gm_track.artist]
#     if len(s_artists) > 1:
#         # Two artists expected, crawl through the track metadata to extract additional artists
#         _, add_artists = utils.strip_ft_artist_from_title(gm_track.title)
#         if not add_artists:
#             if '&' not in gm_track.artist:
#                 raise AssertionError(f'Could not find additional artists for GTrack "{gm_track.__dict__}"')
#             gm_artists = gm_track.artist.split('&')
#         else:
#             gm_artists.append(add_artists)

#     gm_artists.sort()
#     s_artists.sort()

#     return {
#         'gm_artists': gm_artists,
#         's_artists': s_artists
#     }


def titles_match(gm_title: str, sp_title: str) -> bool:
    stripped_gm_title, _ = utils.strip_ft_artist_from_title(gm_title)
    stripped_sp_title, _ = utils.strip_ft_artist_from_title(sp_title)
    stripped_gm_title = utils.strip_str(stripped_gm_title)
    stripped_sp_title = utils.strip_str(stripped_sp_title)
    logger.debug(
        f'Comparing gm_title "{stripped_gm_title}" to "{stripped_sp_title}"')
    return stripped_gm_title == stripped_sp_title


def artists_match(gm_artists: List[str], sp_artists: List[str]) -> bool:
    stripped_gm_artists = [utils.strip_str(artist) for artist in gm_artists]
    stripped_sp_artists = [utils.strip_str(artist) for artist in sp_artists]
    logger.debug(
        f'Comparing gm_artists "{stripped_gm_artists}" to "{stripped_sp_artists}"')
    return stripped_gm_artists == stripped_sp_artists


def _tracks_match(gm_track: gmusic.GMusicTrack,
                  sp_track: spotify.SpAlbumTrack):
    sp_artists = get_sp_track_artists(sp_track)
    gm_artists = get_gm_track_artists(gm_track)
    logger.info(
        f'Comparing GM_Track {gm_track.title} - {gm_track.artist} to SP_track {sp_track.title} - {sp_artists}')
    if not titles_match(gm_track.title, sp_track.title):
        logger.warning(
            f'Titles do not match - "{gm_track.title}" - "{sp_track.title}"')
        return False
    logger.info(f'Titles do match - "{gm_track.title}" - "{sp_track.title}"')
    if not artists_match(sp_artists, gm_artists):
        logger.warning(
            f'Artists do not match - "{sp_artists}" - "{gm_artists}"')
        return False
    logger.info(f'Artists do match - "{sp_artists}" - "{gm_artists}"')
    return True


def _option1(gm_track: gmusic.GMusicTrack,
             sp_tracks: List[spotify.SpAlbumTrack],
             gm_disc_num: int,
             gm_track_num: int) -> spotify.SpAlbumTrack:
    # TODO implement
    #   1. Look up sp_track by disc and track num and determine if they match
    #       - if not then perform a lookup by other means
    #       - how common is it that tracks are different across music services?
    # Get the sp_track for disc and track num
    corresponding_sp_track = [sp_track for sp_track in sp_tracks
                              if sp_track.disc_number == gm_disc_num and
                              sp_track.track_number == gm_track_num]
    if len(corresponding_sp_track) != 1:
        # TODO handle when no track found
        # TODO handle multiple tracks found
        # sp_track = do_stuff_to_get_sp_track()
        raise ValueError('Multiple tracks found')
    else:
        sp_track = corresponding_sp_track[0]
    if not _tracks_match(gm_track, sp_track):
        raise ValueError('Track at position was not what was expected')
    return sp_track


def _option2(gm_track: gmusic.GMusicTrack,
             sp_tracks: List[spotify.SpAlbumTrack]):
    # TODO implement
    #   2. Loop through all the sp_tracks and do a lookup on several factors
    #       - track_num/disc_num/title/artists/etc

    return False


def _match_tracks(
        gm_tracks: MutableMapping[int, MutableMapping[int, gmusic.GMusicTrack]],
        sp_tracks: List[spotify.SpAlbumTrack]):
    sp_tracks_added = []
    # TODO fix these ugly for loops
    for disc_num, disc_tracks in gm_tracks.items():
        for track_num, gm_track in disc_tracks.items():
            # Two ways to tackle this:
            #   1. Look up sp_track by disc and track num and determine if they match
            #       - if not then perform a lookup by other means
            #       - how common is it that tracks are different across music services?
            #   2. Loop through all the sp_tracks and do a lookup on several factors
            #       - track_num/disc_num/title/artists/etc
            # TODO implement both and time them
            sp_track = _option1(gm_track, sp_tracks, disc_num, track_num)
            # sp_track = _option2(gm_track, sp_tracks)
            gm_track.set_spotify_id(sp_track.id)
            if sp_track.id in sp_tracks_added:
                raise ValueError('sp_track already exists in list added')
            sp_tracks_added.append(sp_track.id)
    no_matches = []
    for disc_num, disc_tracks in gm_tracks.items():
        for track_num, gm_track in disc_tracks.items():
            if not gm_track.spotify_id:
                no_matches.append(gm_track)
    if no_matches:
        logger.error('Some tracks could not be matched in spotify:')
        pprint.pprint(jsonpickle.encode(no_matches))
    else:
        logger.info('All tracks were matched successfully')


def _bonus_disc_added(gm_discs: AbstractSet[int], sp_discs: Set[int]) -> bool:
    logger.debug(
        f'gm_discs: {gm_discs} - sp_discs: {sp_discs}')
    if len(gm_discs) == len(sp_discs):
        logger.info('Count of discs is the same, no bonus disc')
        return False
    diff_discs = max(sp_discs) - max(gm_discs)
    if diff_discs != 1:
        raise ValueError(f'Did not expect diff_discs to != 1: Was {diff_discs}')
    logger.info('Difference between highest disc is 1 - consider this a bonus disc')
    return True


def _process_album(gm_album: gmusic.GMusicAlbum,
                   sp_album: spotify.SpAlbum):
    # Usually if the user has the entire album added, we won't perform a
    # per track lookup. However during early stages I want more real test
    # cases for the matching logic
    # TODO reorder if statement when we are no longer performing track matching on everything
    if gm_album.total_tracks() != sp_album.total_tracks:
        # Sometimes Spotify will have a bonus CD whch GM does not
        logger.info(
            'Album partially added to library - checking if bonus CD is on Spotify')
        if _bonus_disc_added(gm_album.discs_added(), sp_album.disc_count):
            logger.info(
                'Bonus disc found on Spotify - marking complete album added')
            gm_album.set_whole_album_added(True)
        else:
            logger.info('No bonus disc found - assuming that user only has some tracks added')
    else:
        logger.info('Complete album added')
        gm_album.set_whole_album_added(True)


    # TODO handle empty results
    # TODO handle # tracks > return limit
    _match_tracks(gm_album.tracks, sp_album.tracks)


# TODO tidy up this function
def query_gm_album_in_spotify(sp_api: spotify.SpApi,
                              gm_album: gmusic.GMusicAlbum):
    q_text = f'{gm_album.title} - {gm_album.album_artist} - {gm_album.year}'
    logger.info(f'Processing {q_text}')
    q = spotify.SpQueryBuilder(
        album=gm_album.title,
        album_artist=gm_album.album_artist,
        year=gm_album.year
    ).build()
    sp_album_query_resp = sp_api.execute_query(q)
    if not sp_album_query_resp.albums.total:
        logger.warning(
            f'No results found querying by year for: {q_text}')
        q_text = f'{gm_album.title} - {gm_album.album_artist}'
        logger.warning(f'Now querying by {q_text}')
        q = spotify.SpQueryBuilder(
            album=gm_album.title,
            album_artist=gm_album.album_artist
        ).build()
        sp_album_query_resp = sp_api.execute_query(q=q)
    if not sp_album_query_resp.albums.total:
        logger.warning(f'No results found querying by: {q_text}. \
            Now querying by album title: {gm_album.title}')
        sp_album_query_resp = sp_api.query_album_by_title(title=gm_album.title)
    if sp_album_query_resp.albums.total > 1:
        raise ValueError(
            f'Could not accurately look up: {gm_album.title} - \
                {gm_album.album_artist}')
        # TODO handle this
    if not sp_album_query_resp.albums.total:
        raise ValueError(
            f'No results found after querying for artist or album title: {gm_album.title} - {gm_album.album_artist}')
    logger.info('Found exactly one match')
    return sp_album_query_resp.albums.items[0]


def main():
    # Auth with spotify and gmusic
    gm_api = gmusic.get_gm_api()

    sp_api = spotify.SpApi(config.get_sp_client_id(),
                           config.get_sp_client_secret())
    # Get all songs
    gm_lib = gm_api.get_all_songs()
    gmusic.gen_report(gm_lib)
    # Match with Spotify
    added_lib = gmusic.filter_added_tracks(gm_lib)

    gm_albums = gmusic.parse_lib(added_lib)
    for gm_album in gm_albums.values():
        sp_album = query_gm_album_in_spotify(sp_api, gm_album)
        gm_album.set_spotify_id(sp_album.id)
        sp_album_detail = sp_api.get_album_by_id(sp_album.id)
        _process_album(gm_album, sp_album_detail)

    # Generate report on what could be matched and what couldn't

    # Ask user what they would like added


if __name__ == '__main__':
    main()
