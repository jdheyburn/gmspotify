import gmusic
import spotify
import argparse
import pprint
import re

albums = {}
ARTIST_MATCH_REGEX = '[A-Za-z0-9\ ]+'
albums = {'Bi5vplouym4ugzrtyyx7c7jh5fa': {'title': 'Mono No Aware', 'albumArtist': 'Various Artists', 'year': 2017, 'tracks': [{'title': 'VXOMEG', 'artist': 'Bill Kouligas', 'rating': ''}, {'title': 'Justforu', 'artist': 'Mya Gomez', 'rating': ''}, {'title': 'Stretch Deep (feat. Eve Essex)', 'artist': 'James K', 'rating': ''}, {'title': 'Heretic', 'artist': 'Oli XL', 'rating': ''}, {'title': 'Lugere', 'artist': 'Flora Yin-Wong', 'rating': ''}, {'title': 'Exasthrus (Pane)', 'artist': 'M.E.S.H.', 'rating': ''}, {'title': 'C6 81 56 28 09 34 31 D2 F9 9C D6 BD 92 ED FC 6F 6C A9 D4 88 95 8C 53 B4 55 DF 38 C4 AB E7 72 13', 'artist': 'TCF', 'rating': ''}, {'title': 'Ok, American Medium', 'artist': 'Jeff Witscher', 'rating': ''}, {'title': 'Open Invitation', 'artist': 'ADR', 'rating': ''}, {'title': 'Huit', 'artist': 'SKY H1', 'rating': ''}, {'title': 'Held', 'artist': 'Malibu', 'rating': ''}, {'title': 'Second Mistake', 'artist': 'AYYA', 'rating': ''}, {'title': 'Fr3sh', 'artist': 'Kareem Lotfy', 'rating': ''}, {'title': 'Eliminator', 'artist': 'Helm', 'rating': ''}, {'title': 'Limerence', 'artist': 'Yves Tumor', 'rating': '5'}, {'title': 'Zhao Hua', 'artist': 'HVAD & Pan Daijing', 'rating': '5'}]}}

def parse_lib(lib):
    albums = {}
    for track in lib:
        albumId = track['albumId']
        if albumId not in albums:
            album = {}
            album['title'] = track['album']
            album['albumArtist'] = track['albumArtist']
            if 'year' in track:    
                album['year'] = track['year']
            album['tracks'] = []
            albums[albumId] = album
        album = albums[albumId]
        track_rating = track['rating'] if 'rating' in track else ''
        # TODO should be mapped by track number?
        album['tracks'].append({
            'title': track['title'],
            'artist': track['artist'],
            'rating': track_rating
        })
    return albums


def _strip_str(str):
    return ''.join(re.findall(ARTIST_MATCH_REGEX, str)).lower()


def _match_tracks(gm_tracks, s_tracks):
    s_tracks_added = []
    for gm_track in gm_tracks:
        for s_track in s_tracks:
            s_track_id = s_track['id']
            if s_track_id in s_tracks_added:
                continue
            if len(s_track['artists']) > 1:
                print('s_track gm_has more than one artist! {}'.format(s_track['artists']))
            gm_title = _strip_str(gm_track['title'])
            gm_artist =_strip_str(gm_track['artist'])
            s_title = _strip_str(s_track['name'])
            s_artist = _strip_str(s_track['artists'][0]['name'])
            if gm_title == s_title and gm_artist == s_artist:
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
    # Look up each track to get its ID
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