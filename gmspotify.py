import gmusic
import spotify
import argparse
import pprint
import re
import utils
from typing import List, MutableMapping


albums = {'Bi5vplouym4ugzrtyyx7c7jh5fa': {'title': 'Mono No Aware', 'albumArtist': 'Various Artists', 'year': 2017, 'tracks': [{'title': 'VXOMEG', 'artist': 'Bill Kouligas', 'rating': ''}, {'title': 'Justforu', 'artist': 'Mya Gomez', 'rating': ''}, {'title': 'Stretch Deep (feat. Eve Essex)', 'artist': 'James K', 'rating': ''}, {'title': 'Heretic', 'artist': 'Oli XL', 'rating': ''}, {'title': 'Lugere', 'artist': 'Flora Yin-Wong', 'rating': ''}, {'title': 'Exasthrus (Pane)', 'artist': 'M.E.S.H.', 'rating': ''}, {'title': 'C6 81 56 28 09 34 31 D2 F9 9C D6 BD 92 ED FC 6F 6C A9 D4 88 95 8C 53 B4 55 DF 38 C4 AB E7 72 13', 'artist': 'TCF', 'rating': ''}, {'title': 'Ok, American Medium', 'artist': 'Jeff Witscher', 'rating': ''}, {'title': 'Open Invitation', 'artist': 'ADR', 'rating': ''}, {'title': 'Huit', 'artist': 'SKY H1', 'rating': ''}, {'title': 'Held', 'artist': 'Malibu', 'rating': ''}, {'title': 'Second Mistake', 'artist': 'AYYA', 'rating': ''}, {'title': 'Fr3sh', 'artist': 'Kareem Lotfy', 'rating': ''}, {'title': 'Eliminator', 'artist': 'Helm', 'rating': ''}, {'title': 'Limerence', 'artist': 'Yves Tumor', 'rating': '5'}, {'title': 'Zhao Hua', 'artist': 'HVAD & Pan Daijing', 'rating': '5'}]}}
multiple_artists = [{'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/25BObiRSDCMwVrBGIVaLIf'}, 'href': 'https://api.spotify.com/v1/artists/25BObiRSDCMwVrBGIVaLIf', 'id': '25BObiRSDCMwVrBGIVaLIf', 'name': 'James K', 'type': 'artist', 'uri': 'spotify:artist:25BObiRSDCMwVrBGIVaLIf'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/1g80vffuPrdapR6S4WyxN3'}, 'href': 'https://api.spotify.com/v1/artists/1g80vffuPrdapR6S4WyxN3', 'id': '1g80vffuPrdapR6S4WyxN3', 'name': 'Eve Essex', 'type': 'artist', 'uri': 'spotify:artist:1g80vffuPrdapR6S4WyxN3'}]}], [{'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/25BObiRSDCMwVrBGIVaLIf'}, 'href': 'https://api.spotify.com/v1/artists/25BObiRSDCMwVrBGIVaLIf', 'id': '25BObiRSDCMwVrBGIVaLIf', 'name': 'James K', 'type': 'artist', 'uri': 'spotify:artist:25BObiRSDCMwVrBGIVaLIf'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/1g80vffuPrdapR6S4WyxN3'}, 'href': 'https://api.spotify.com/v1/artists/1g80vffuPrdapR6S4WyxN3', 'id': '1g80vffuPrdapR6S4WyxN3', 'name': 'Eve Essex', 'type': 'artist', 'uri': 'spotify:artist:1g80vffuPrdapR6S4WyxN3'}], 'available_markets': ['AD', 'AE', 'AR', 'AT', 'AU', 'BE', 'BG', 'BH', 'BO', 'BR', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GR', 'GT', 'HK', 'HN', 'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT', 'JO', 'JP', 'KW', 'LB', 'LI', 'LT', 'LU', 'LV', 'MA', 'MC', 'MT', 'MX', 'MY', 'NI', 'NL', 'NO', 'NZ', 'OM', 'PA', 'PE', 'PH', 'PL', 'PS', 'PT', 'PY', 'QA', 'RO', 'SA', 'SE', 'SG', 'SK', 'SV', 'TH', 'TN', 'TR', 'TW', 'US', 'UY', 'VN', 'ZA'], 'disc_number': 1, 'duration_ms': 260446, 'explicit': False, 'external_urls': {'spotify': 'https://open.spotify.com/track/1mh4GpKKrmlaUkVzoNqhRt'}, 'href': 'https://api.spotify.com/v1/tracks/1mh4GpKKrmlaUkVzoNqhRt', 'id': '1mh4GpKKrmlaUkVzoNqhRt', 'is_local': False, 'name': 'Stretch Deep - feat. Eve Essex', 'preview_url': 'https://p.scdn.co/mp3-preview/ebb7e70b97a5d29e05044a1f920d1fc594f92b26?cid=ea3ef49a097b42d682d3c7bc98832d65', 'track_number': 12, 'type': 'track', 'uri': 'spotify:track:1mh4GpKKrmlaUkVzoNqhRt'}, {'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/1QXjEEDCHutVkOzAD6g13J'}, 'href': 'https://api.spotify.com/v1/artists/1QXjEEDCHutVkOzAD6g13J', 'id': '1QXjEEDCHutVkOzAD6g13J', 'name': 'HVAD', 'type': 'artist', 'uri': 'spotify:artist:1QXjEEDCHutVkOzAD6g13J'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/2OA8e1A4qJVqDHbjnc86dR'}, 'href': 'https://api.spotify.com/v1/artists/2OA8e1A4qJVqDHbjnc86dR', 'id': '2OA8e1A4qJVqDHbjnc86dR', 'name': 'Pan Daijing', 'type': 'artist', 'uri': 'spotify:artist:2OA8e1A4qJVqDHbjnc86dR'}], 'available_markets': ['AD', 'AE', 'AR', 'AT', 'AU', 'BE', 'BG', 'BH', 'BO', 'BR', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GR', 'GT', 'HK', 'HN', 'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT', 'JO', 'JP', 'KW', 'LB', 'LI', 'LT', 'LU', 'LV', 'MA', 'MC', 'MT', 'MX', 'MY', 'NI', 'NL', 'NO', 'NZ', 'OM', 'PA', 'PE', 'PH', 'PL', 'PS', 'PT', 'PY', 'QA', 'RO', 'SA', 'SE', 'SG', 'SK', 'SV', 'TH', 'TN', 'TR', 'TW', 'US', 'UY', 'VN', 'ZA'], 'disc_number': 1, 'duration_ms': 406706, 'explicit': False, 'external_urls': {'spotify': 'https://open.spotify.com/track/6gUT2cVE1AjuZyFmqE7MLz'}, 'href': 'https://api.spotify.com/v1/tracks/6gUT2cVE1AjuZyFmqE7MLz', 'id': '6gUT2cVE1AjuZyFmqE7MLz', 'is_local': False, 'name': 'Zhao Hua', 'preview_url': 'https://p.scdn.co/mp3-preview/081e244c58ffb22bb5f9cf6ab9fbe5348e354a86?cid=ea3ef49a097b42d682d3c7bc98832d65', 'track_number': 16, 'type': 'track', 'uri': 'spotify:track:6gU'}]
ma_gm = [
    {'title': 'Stretch Deep (feat. Eve Essex)', 'artist': 'James K', 'rating': ''},
    {'title': 'Zhao Hua', 'artist': 'HVAD & Pan Daijing', 'rating': '5'}    
]
# TODO include test for matching these two tracks:
#Eartheater
# gm_title: MMXXX (ft Moor Mother)
# s_title:  MMXXX - feat. Moor Mother


def parse_lib(lib: List) -> MutableMapping[str, gmusic.GMusicAlbum]:
    # TODO do we need to define the type here?
    albums: MutableMapping[str, gmusic.GMusicAlbum] = {}
    for track in lib:
        albumId = track['albumId']
        if albumId not in albums: 
            albums[albumId] = gmusic.GMusicAlbum(
                id,
                track['album'],
                track['albumArtist'],
                track['year'] if 'year' in track else '' # TODO better way to handle this?
            )
        album = albums[albumId]
    
        try:
            album.add_track(
                track['discNumber'], 
                track['trackNumber'], gmusic.GMusicTrack(
                    track['title'],
                    track['artist'],
                    track['rating'] if 'rating' in track else ''
                )
            )
        except gmusic.DuplicateTrackError as e:
            # TODO just raise it for now for testing, implement a failsafe later
            raise e
    return albums






def _get_all_artists_from_tracks(gm_track, s_track) -> List[str]:
    gm_artist = gm_track['artist']
    s_artists = s_track['artists'] # TODO this isn't right




def titles_match(gm_title, s_title):
    stripped_gm_title, _ = utils.strip_ft_artist_from_title(gm_title)
    return stripped_gm_title == s_title

# TODO implement this - but need to create classes first
def match_tracks(gm_track: gmusic.GMusicTrack, s_track: spotify.STrack):
    pass


def _match_tracks(gm_tracks, s_tracks):
    s_tracks_added = []
    for gm_track in gm_tracks:
        for s_track in s_tracks:
            s_track_id = s_track['id']
            if s_track_id in s_tracks_added:
                continue
            gm_artists = [utils.strip_str(gm_track['artist'])]
            
            if len(s_track['artists']) > 1:
                print('s_track {} has more than one artist! {}'.format(gm_track['title'], [x['name'] for x in s_track['artists']]))
                gm_title, ft_artists = utils.strip_ft_artist_from_title(gm_track['title'])
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



def match(sp_api, albums):
    for albumId, album in albums.items():
        album_title = album['title']
        album_artist = album['albumArtist']
        print('Processing {} - {}'.format(album_title, album_artist))
        results = spotify.query_album_by_artist(sp_api, album_title, album_artist)
        num_results = results['albums']['total']
        if not num_results:
            print('No results found for: {} - {}'.format(album_title,album_artist))
            print('Now querying by album_title {}'.format(album_title))
            results = spotify.query_albums_by_title(sp_api, album_title)
            num_results = results['albums']['total']
        if num_results == 1:
            print('    Found exactly one match')
            spotify_album = results['albums']['items'][0]
            _process_album(sp_api, album, spotify_album)
        elif num_results > 1:
            print('Could not accurately look up: {} - {}'.format(album_title,album_artist))
            break # breaks are temp for testing
        else:
            print('No results found after querying for artist or album title: {} - {}'.format(album_title,album_artist))
            break # breaks are temp for testing
            


def main():
    # Auth with spotify and gmusic
    gm_api = gmusic.get_gm_api()
    sp_api = spotify.get_sp_ccm()
    # Get all songs
    gm_lib = gm_api.get_all_songs()
    gmusic.gen_report(gm_lib)
    # Match with Spotify
    added_lib = gmusic.filter_added_tracks(gm_lib)

    albums = parse_lib(added_lib)
    match(albums)

    # Generate report on what could be matched and what couldn't

    # Ask user what they would like added
    


if __name__ == '__main__':
    main()