import spotify
import uuid
import munch

from typing import List


def construct_sp_track(artists: List[str],
                       disc_num: int,
                       title: str,
                       track_num: int) -> spotify.SpAlbumTrack:
    sp_artists = []
    for artist in artists:
        obj = munch.munchify({'id': str(uuid.uuid4()), 'name': artist})
        sp_artists.append(obj)
           
    obj = munch.munchify({
        'id': str(uuid.uuid4()),
        'artists': sp_artists,
        'disc_number': disc_num,
        'track_number': track_num,
        'name': title
    })
    return spotify.SpAlbumTrack(obj)
