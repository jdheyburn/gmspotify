import unittest
import json

import gmspotify
import spotify
import gmusic
import munch
from unittest.mock import MagicMock
from test_helpers import construct_sp_track


sp_track_1 = construct_sp_track(
    ['Ezra Collective', 'Loyle Carner'],
    1,
    'Stretch Deep - feat. Eve Essex',
    12
)

gm_track_1 = gmusic.GMusicTrack(
    title='Stretch Deep (feat. Eve Essex)',
    artist='James K'
)


class TestGetSTrackArtists(unittest.TestCase):

    def test_get_s_track_artists(self):
        """
        Given a s_track record with multiple artists
        Should return a list of those artists
        """
        sp_track = spotify.SpAlbumTrack(munch.munchify({'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/25BObiRSDCMwVrBGIVaLIf'}, 'href': 'https://api.spotify.com/v1/artists/25BObiRSDCMwVrBGIVaLIf', 'id': '25BObiRSDCMwVrBGIVaLIf', 'name': 'James K', 'type': 'artist', 'uri': 'spotify:artist:25BObiRSDCMwVrBGIVaLIf'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/1g80vffuPrdapR6S4WyxN3'}, 'href': 'https://api.spotify.com/v1/artists/1g80vffuPrdapR6S4WyxN3', 'id': '1g80vffuPrdapR6S4WyxN3', 'name': 'Eve Essex', 'type': 'artist', 'uri': 'spotify:artist:1g80vffuPrdapR6S4WyxN3'}], 'available_markets': ['AD', 'AE', 'AR', 'AT', 'AU', 'BE', 'BG', 'BH', 'BO', 'BR', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GR', 'GT', 'HK', 'HN',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT', 'JO', 'JP', 'KW', 'LB', 'LI', 'LT', 'LU', 'LV', 'MA', 'MC', 'MT', 'MX', 'MY', 'NI', 'NL', 'NO', 'NZ', 'OM', 'PA', 'PE', 'PH', 'PL', 'PS', 'PT', 'PY', 'QA', 'RO', 'SA', 'SE', 'SG', 'SK', 'SV', 'TH', 'TN', 'TR', 'TW', 'US', 'UY', 'VN', 'ZA'], 'disc_number': 1, 'duration_ms': 260446, 'explicit': False, 'external_urls': {'spotify': 'https://open.spotify.com/track/1mh4GpKKrmlaUkVzoNqhRt'}, 'href': 'https://api.spotify.com/v1/tracks/1mh4GpKKrmlaUkVzoNqhRt', 'id': '1mh4GpKKrmlaUkVzoNqhRt', 'is_local': False, 'name': 'Stretch Deep - feat. Eve Essex', 'preview_url': 'https://p.scdn.co/mp3-preview/ebb7e70b97a5d29e05044a1f920d1fc594f92b26?cid=ea3ef49a097b42d682d3c7bc98832d65', 'track_number': 12, 'type': 'track', 'uri': 'spotify:track:1mh4GpKKrmlaUkVzoNqhRt'}))
        expected = ['Eve Essex', 'James K']
        actual = gmspotify.get_sp_track_artists(sp_track)
        self.assertEqual(actual, expected)


class TestGetGMTrackArtists(unittest.TestCase):

    def test_get_gm_track_artists_ampersand(self):
        """
        Given a GM Track with an artist string containing multiple artists
        Should return a list of those artists
        """
        gm_track = gmusic.GMusicTrack(
            title='Zhao Hua', artist='HVAD & Pan Daijing')
        expected = ['HVAD', 'Pan Daijing']
        actual = gmspotify.get_gm_track_artists(gm_track)
        self.assertEqual(actual, expected)

    def test_get_gm_track_artists_ft_1(self):
        """
        Given a GM Track with a title featuring an artist
        Should append that artist to main artist
        """
        gm_track = gmusic.GMusicTrack(
            title='Stretch Deep (feat. Eve Essex)',
            artist='James K'
        )
        expected = ['Eve Essex', 'James K']
        actual = gmspotify.get_gm_track_artists(gm_track)
        self.assertEqual(actual, expected)

    def test_get_gm_track_artists_ft_2(self):
        """
        Given a GM Track with a title featuring an artist
        Should append that artist to main artist
        """
        gm_track = gmusic.GMusicTrack(
            title='MMXXX (ft Moor Mother)',
            artist='Earthmother'
        )
        expected = ['Earthmother', 'Moor Mother']
        actual = gmspotify.get_gm_track_artists(gm_track)
        self.assertEqual(actual, expected)


class TestMatchingLogic(unittest.TestCase):

    def test_titles_do_not_match(self):
        """
        Given a GM Track and a S_track with titles that do not match
        Should return false
        """
        gm_title = 'Zhao Hua'
        s_title = 'MMXXX (ft Moor Mother)'
        self.assertFalse(gmspotify.titles_match(gm_title, s_title))

    def test_titles_match_diff_ft_styles(self):
        """
        Given a GM Track and a S_track with same titles
        Should return false
        """
        gm_title = 'Stretch Deep (feat. Eve Essex)'
        s_title = 'Stretch Deep - feat. Eve Essex'
        self.assertTrue(gmspotify.titles_match(gm_title, s_title))

    def test_tracks_match_1(self):
        gm_track = gmusic.GMusicTrack(
            title='Zhao Hua', artist='HVAD & Pan Daijing')


class TestQueryingLogic(unittest.TestCase):

    def get_mock_sp_api(self) -> spotify.SpApi:
        mock_sp_api = spotify.SpApi('id', 'secret')
        mock_sp_api.client = MagicMock(search=MagicMock(
            return_value={'albums': {'href': 'https://api.spotify.com/v1/search?query=album%3AGrafts+artist%3AKara-Lis+Coverdale&type=album&offset=0&limit=10', 'items': [{'album_type': 'single', 'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/5pHUdo5THDtmE9yu3iC2hA'}, 'href': 'https://api.spotify.com/v1/artists/5pHUdo5THDtmE9yu3iC2hA', 'id': '5pHUdo5THDtmE9yu3iC2hA', 'name': 'Kara-Lis Coverdale', 'type': 'artist', 'uri': 'spotify:artist:5pHUdo5THDtmE9yu3iC2hA'}], 'available_markets': ['AD', 'AE', 'AR', 'AT', 'AU', 'BE', 'BG', 'BH', 'BO', 'BR', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GR', 'GT', 'HK', 'HN', 'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT', 'JO', 'JP', 'KW', 'LB', 'LI', 'LT', 'LU', 'LV', 'MA', 'MC', 'MT', 'MX', 'MY', 'NI', 'NL', 'NO', 'NZ', 'OM', 'PA', 'PE', 'PH', 'PL', 'PS', 'PT', 'PY', 'QA', 'RO', 'SA', 'SE', 'SG', 'SK', 'SV', 'TH', 'TN', 'TR', 'TW', 'US', 'UY', 'VN', 'ZA'], 'external_urls': {'spotify': 'https://open.spotify.com/album/6hT28oOwJbnRX9qvxbXbTw'}, 'href': 'https://api.spotify.com/v1/albums/6hT28oOwJbnRX9qvxbXbTw', 'id': '6hT28oOwJbnRX9qvxbXbTw', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/e462332bfd17049e0ed66ee405550eb0a450b036', 'width': 640}, {'height': 300, 'url': 'https://i.scdn.co/image/501f4363400b5844f9378052efdf691c688c933c', 'width': 300}, {'height': 64, 'url': 'https://i.scdn.co/image/10cbb9e4bbfc9057c08a2628e9b6c81d73b9d51f', 'width': 64}], 'name': 'Grafts', 'release_date': '2017-05-05', 'release_date_precision': 'day', 'total_tracks': 1, 'type': 'album', 'uri': 'spotify:album:6hT28oOwJbnRX9qvxbXbTw'}], 'limit': 10, 'next': None, 'offset': 0, 'previous': None, 'total': 1}}))  # None for now to test
        return mock_sp_api

    def test_initial_sp_query(self):
        sp_api = self.get_mock_sp_api()
        gm_album = gmusic.GMusicAlbum(
            id='B5chesvwefhpatizcpdwavg65iu',
            title='Grafts',
            album_artist='Kara-Lis Coverdale',
            year='2017',
            tracks={
                1: {
                    1: gmusic.GMusicTrack(title='Grafts', artist='Kara-Lis Coverdale')
                }
            }
        )

        gmspotify.query_gm_album_in_spotify(sp_api=sp_api, gm_album=gm_album)
        sp_api.client.search.assert_called_once_with(
            q='album:Grafts artist:Kara-Lis Coverdale year:2017', type='album')


if __name__ == '__main__':
    unittest.main()
