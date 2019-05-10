import gmusic
import argparse

{
    "ALBUM_NAME": {
        "ARTIST_NAME": ,
        "YEAR": 2001
    }
}   


albums = {}
#albums = {'Bi5vplouym4ugzrtyyx7c7jh5fa': {'title': 'Mono No Aware', 'albumArtist': 'Various Artists', 'year': 2017, 'tracks': [{'title': 'VXOMEG', 'artist': 'Bill Kouligas', 'rating': ''}, {'title': 'Justforu', 'artist': 'Mya Gomez', 'rating': ''}, {'title': 'Stretch Deep (feat. Eve Essex)', 'artist': 'James K', 'rating': ''}, {'title': 'Heretic', 'artist': 'Oli XL', 'rating': ''}, {'title': 'Lugere', 'artist': 'Flora Yin-Wong', 'rating': ''}, {'title': 'Exasthrus (Pane)', 'artist': 'M.E.S.H.', 'rating': ''}, {'title': 'C6 81 56 28 09 34 31 D2 F9 9C D6 BD 92 ED FC 6F 6C A9 D4 88 95 8C 53 B4 55 DF 38 C4 AB E7 72 13', 'artist': 'TCF', 'rating': ''}, {'title': 'Ok, American Medium', 'artist': 'Jeff Witscher', 'rating': ''}, {'title': 'Open Invitation', 'artist': 'ADR', 'rating': ''}, {'title': 'Huit', 'artist': 'SKY H1', 'rating': ''}, {'title': 'Held', 'artist': 'Malibu', 'rating': ''}, {'title': 'Second Mistake', 'artist': 'AYYA', 'rating': ''}, {'title': 'Fr3sh', 'artist': 'Kareem Lotfy', 'rating': ''}, {'title': 'Eliminator', 'artist': 'Helm', 'rating': ''}, {'title': 'Limerence', 'artist': 'Yves Tumor', 'rating': '5'}, {'title': 'Zhao Hua', 'artist': 'HVAD & Pan Daijing', 'rating': '5'}]}}

def parse_lib(lib):
    for track in lib:
        albumId = track['albumId']
        if albumId not in albums:
            album = {}
            album['title'] = track['album']
            album['albumArtist'] = track['albumArtist']
            album['year'] = track['year']
            album['tracks'] = []
            albums[albumId] = album
        album = albums[albumId]
        track_rating = track['rating'] if 'rating' in track else ''
        album['tracks'].append({
            'title': track['title'],
            'artist': track['artist'],
            'rating': track_rating
        })



def match(lib):



def main():
    # Auth with spotify and gmusic
    gm_api = gmusic.get_gm_api()
    # Get all songs
    gm_lib = gm_api.get_all_songs()
    gmusic.gen_report(gm_lib)
    match(gmusic.filter_added_tracks(gm_lib))
    


if __name__ == '__main__':
    main()