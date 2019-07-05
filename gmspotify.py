import gmusic
import config
import spotify
import argparse
import pprint
import re
import utils
from typing import List, MutableMapping
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
    print(f'Comparing gm_title "{stripped_gm_title}" to "{stripped_sp_title}"')
    return stripped_gm_title == stripped_sp_title


def _tracks_match(gm_track: gmusic.GMusicTrack,
                  sp_track: spotify.SpAlbumTrack):
    # TODO implement - below is draft code

    sp_artists = get_sp_track_artists(sp_track)
    gm_artists = get_gm_track_artists(gm_track)

    print(f'Comparing GM_Track {gm_track.title} - {gm_track.artist} to SP_track {sp_track.title} - {sp_artists}')

    if not titles_match(gm_track.title, sp_track.title):
        print(f'Titles do not match - "{gm_track.title}" - "{sp_track.title}"')
        return False
    
    print(f'Titles do match - "{gm_track.title}" - "{sp_track.title}"')

    if len(sp_artists) > 1:
        print('sp_track has more than one artist')




    # if len(sp_track.artists) > 1:
    #     print(f'sp_track {} has more than one artist! {}'.format(
    #         gm_track['title'], [x['name'] for x in s_track['artists']]))
    #     gm_title, ft_artists = utils.strip_ft_artist_from_title(
    #         gm_track['title'])
    #     if not ft_artists:
    #         print('ft_artist was empty unexpectedly')
    #     else:
    #         gm_title = utils.strip_str(gm_track['title'])

    # s_title = utils.strip_str(s_track['name'])
    # s_artist = utils.strip_str(s_track['artists'][0]['name'])
    # if gm_title == s_title:
    #     if gm_artist == s_artist:
    #         print('Found match for {} - {}'.format(gm_title, gm_artist))
    #     gm_track['spotifyId'] = s_track_id
    #     s_tracks_added.append(s_track_id)
    return False


def _option1(gm_track: gmusic.GMusicTrack,
             sp_tracks: List[spotify.SpAlbumTrack],
             gm_disc_num: int,
             gm_track_num: int):
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
        sp_track = do_stuff_to_get_sp_track()
    else:
        sp_track = corresponding_sp_track[0]

    if _tracks_match(gm_track, sp_track):
        pass
    return False


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
    gm_tracks_added = []
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
            sp_track = _option2(gm_track, sp_tracks)
            gm_track.set_spotify_id(sp_track.id)
            sp_tracks_added.append(sp_track.id)

    no_matches = [
        gm_track for gm_track in gm_tracks if not gm_track.spotify_id]
    if no_matches:
        print('Some tracks could not be matched in spotify:')
        pprint.pprint(no_matches)
    else:
        print('All tracks were matched successfully')


def _process_album(sp_api, gm_album: gmusic.GMusicAlbum,
                   sp_album: spotify.SpQueryAlbum):
    gm_album.set_spotify_id(sp_album.id)

    if gm_album.total_tracks() == sp_album.total_tracks:
        print('    Complete album added')
        gm_album.set_whole_album_added(True)
    else:
        print('    Album partially added to library')
    # Usually if the user has the entire album added, we won't perform a
    # per track lookup. However during early stages I want more real test
    # cases for the matching logic
    sp_album = sp_api.get_album_by_id(sp_album.id)
    # TODO handle empty results
    # TODO handle # tracks > return limit
    _match_tracks(gm_album.tracks, sp_album.tracks)


# TODO tidy up this function
def query_gm_album_in_spotify(sp_api: spotify.SpApi,
                              gm_album: gmusic.GMusicAlbum):
    q_text = f'{gm_album.title} - {gm_album.album_artist} - {gm_album.year}'
    print(f'Processing {q_text}')

    q = spotify.SpQueryBuilder(
        album=gm_album.title,
        album_artist=gm_album.album_artist,
        year=gm_album.year
    ).build()

    sp_album_query_resp = sp_api.execute_query(q)

    if not sp_album_query_resp.albums.total:
        print(
            f'No results found querying by year for: {q_text}')
        q_text = f'{gm_album.title} - {gm_album.album_artist}'
        print(f'Now querying by {q_text}')
        q = spotify.SpQueryBuilder(
            album=gm_album.title,
            album_artist=gm_album.album_artist
        ).build()

        sp_album_query_resp = sp_api.execute_query(q=q)

    if not sp_album_query_resp.albums.total:
        print(
            f'No results found querying by: {q_text}')
        print(f'Now querying by album title: {gm_album.title}')
        sp_album_query_resp = sp_api.query_album_by_title(title=gm_album.title)

    if sp_album_query_resp.albums.total == 1:
        print('    Found exactly one match')

        sp_album = sp_album_query_resp.albums.items[0]
        _process_album(sp_api, gm_album, sp_album)
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
