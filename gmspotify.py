import gmusic
import config
import spotify
import argparse
import pprint
import re
import utils
from typing import List, MutableMapping, Mapping
import munch


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


def get_s_track_artists(s_track: munch.Munch) -> List[str]:
    return sorted([artist.name for artist in s_track.artists])


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


def titles_match(gm_title: str, s_title: str) -> bool:
    stripped_gm_title, _ = utils.strip_ft_artist_from_title(gm_title)
    stripped_s_title, _ = utils.strip_ft_artist_from_title(s_title)
    return stripped_gm_title == stripped_s_title

# TODO implement this - but need to create classes first
# def match_tracks(gm_track: gmusic.GMusicTrack, s_track: spotify.STrack):
#     pass


def _match_tracks(gm_tracks, s_tracks):
    s_tracks_added = []
    for gm_track in gm_tracks:
        for s_track in s_tracks:
            s_track_id = s_track['id']
            if s_track_id in s_tracks_added:
                continue
            gm_artists = [utils.strip_str(gm_track['artist'])]

            if len(s_track['artists']) > 1:
                print('s_track {} has more than one artist! {}'.format(
                    gm_track['title'], [x['name'] for x in s_track['artists']]))
                gm_title, ft_artists = utils.strip_ft_artist_from_title(
                    gm_track['title'])
                if not ft_artists:
                    print('ft_artist was empty unexpectedly')
                else:
                    gm_title = utils.strip_str(gm_track['title'])

            s_title = utils.strip_str(s_track['name'])
            s_artist = utils.strip_str(s_track['artists'][0]['name'])
            if gm_title == s_title:
                if gm_artist == s_artist:
                    print('Found match for {} - {}'.format(gm_title, gm_artist))
                gm_track['spotifyId'] = s_track_id
                s_tracks_added.append(s_track_id)
    no_matches = [x for x in gm_tracks if 'spotifyId' not in x]
    if no_matches:
        print('Some tracks could not be matched in spotify:')
        pprint.pprint(no_matches)
    else:
        print('All tracks were matched successfully')


def _process_album(sp_api, album, spotify_album):
    album['spotifyId'] = spotify_album['id']
    if len(album['tracks']) == spotify_album['total_tracks']:
        print('    Complete album added')
        album['wholeAlbum'] = True
    else:
        print('    Album partially added to library')
        album['wholeAlbum'] = False
    # Usually if the user has the entire album added, we won't perform a
    # per track lookup. However during early stages I want more real test
    # cases for the matching logic
    s_album_results = spotify.get_album_by_id(sp_api, album['spotifyId'])
    # TODO handle empty results
    # TODO handle # tracks > return limit
    _match_tracks(album['tracks'], s_album_results['tracks']['items'])


def query_gm_album_in_spotify(sp_api: spotify.SpApi, gm_album: gmusic.GMusicAlbum):
    print(f'Processing {gm_album.title} - {gm_album.album_artist}')

    q = spotify.SpQueryBuilder(
        album=gm_album.title,
        album_artist=gm_album.album_artist,
        year=gm_album.year
    ).build()

    sp_album_query_resp = sp_api.execute_query(q)

    if not sp_album_query_resp.albums.total:
        print(
            f'No results found for: {gm_album.title} - {gm_album.album_artist}')
        print(f'Now querying by album_title {gm_album.title}')

        sp_album_query_resp = sp_api.query_album_by_title(title=gm_album.title)

    if sp_album_query_resp.albums.total == 1:
        print('    Found exactly one match')

        spotify_album = sp_album_query_resp.albums.items[0]
        # _process_album(sp_api, gm_album, spotify_album)
    elif sp_album_query_resp.albums.total > 1:
        print(
            f'Could not accurately look up: {gm_album.title} - {gm_album.album_artist}')
        # TODO handle this
    else:
        print(
            f'No results found after querying for artist or album title: {gm_album.title} - {gm_album.album_artist}')


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
        query_gm_album_in_spotify(sp_api, gm_album)

    # Generate report on what could be matched and what couldn't

    # Ask user what they would like added


if __name__ == '__main__':
    main()
