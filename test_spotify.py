import unittest
import spotify
from unittest.mock import MagicMock
import json
import munch

get_album_by_id_response_fname = 'sp_get_album_by_id.json'
with open(get_album_by_id_response_fname, 'r', encoding='utf-8') as f:
    get_album_by_id_response = json.load(f)


class TestQueryBuilderClass(unittest.TestCase):
    
    def test_query_builder_album(self):
        """
        Should construct correct query for album title
        """
        title = 'Grafts'
        expected = 'album:Grafts'
        actual = spotify.SpQueryBuilder(album=title).build()
        self.assertEqual(actual, expected)

    def test_query_builder_album_artist(self):
        """
        Should construct correct query for album title and artist
        """
        title = 'Grafts'
        artist = 'Kara-Lis Coverdale'
        expected = 'album:Grafts artist:Kara-Lis Coverdale'
        actual = spotify.SpQueryBuilder(album=title, album_artist=artist).build()
        self.assertEqual(actual, expected)

    def test_query_builder_artist_year(self):
        """
        Should construct correct query for artist and year
        """
        artist = 'Kara-Lis Coverdale'
        year = '2017'
        expected = 'artist:Kara-Lis Coverdale year:2017'
        actual = spotify.SpQueryBuilder(album_artist=artist, year=year).build()
        self.assertEqual(actual, expected)

class TestSpApiClass(unittest.TestCase):
    def test_get_album_by_id(self):
        """
        Given a request is made to Spotify API for Album ID
        Should verify that the API is hit
        """
        api = spotify.SpApi('id', 'secret')
        expected = spotify.SpAlbum(munch.munchify(get_album_by_id_response))
        api.client = MagicMock(album=MagicMock(return_value=get_album_by_id_response))
        actual = api.get_album_by_id('album_id')

        api.client.album.assert_called_once_with('album_id')
        self.assertEqual(actual, expected)


class TestSpApiClasses(unittest.TestCase):

    def test_sp_artist_equality(self):
        sp_artist_1 = spotify.SpArtist(munch.munchify({'id': 'id1', 'name': 'Joji Koyama'}))
        sp_artist_2 = spotify.SpArtist(munch.munchify({'id': 'id1', 'name': 'Joji Koyama'}))
        self.assertEqual(sp_artist_1, sp_artist_2)

    def test_sp_artist_inequality(self):
        sp_artist_1 = spotify.SpArtist(munch.munchify({'id': 'id1', 'name': 'Joji Koyama'}))
        sp_artist_2 = spotify.SpArtist(munch.munchify({'id': 'id2', 'name': 'Tujiko Noriko'}))
        self.assertNotEqual(sp_artist_1, sp_artist_2)

    def test_sp_album_track_equality(self):
        sp_track_1 = spotify.SpAlbumTrack(munch.munchify({'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/25BObiRSDCMwVrBGIVaLIf'}, 'href': 'https://api.spotify.com/v1/artists/25BObiRSDCMwVrBGIVaLIf', 'id': '25BObiRSDCMwVrBGIVaLIf', 'name': 'James K', 'type': 'artist', 'uri': 'spotify:artist:25BObiRSDCMwVrBGIVaLIf'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/1g80vffuPrdapR6S4WyxN3'}, 'href': 'https://api.spotify.com/v1/artists/1g80vffuPrdapR6S4WyxN3', 'id': '1g80vffuPrdapR6S4WyxN3', 'name': 'Eve Essex', 'type': 'artist', 'uri': 'spotify:artist:1g80vffuPrdapR6S4WyxN3'}], 'available_markets': ['AD', 'AE', 'AR', 'AT', 'AU', 'BE', 'BG', 'BH', 'BO', 'BR', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GR', 'GT', 'HK', 'HN', 'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT', 'JO', 'JP', 'KW', 'LB', 'LI', 'LT', 'LU', 'LV', 'MA', 'MC', 'MT', 'MX', 'MY', 'NI', 'NL', 'NO', 'NZ', 'OM', 'PA', 'PE', 'PH', 'PL', 'PS', 'PT', 'PY', 'QA', 'RO', 'SA', 'SE', 'SG', 'SK', 'SV', 'TH', 'TN', 'TR', 'TW', 'US', 'UY', 'VN', 'ZA'], 'disc_number': 1, 'duration_ms': 260446, 'explicit': False, 'external_urls': {'spotify': 'https://open.spotify.com/track/1mh4GpKKrmlaUkVzoNqhRt'}, 'href': 'https://api.spotify.com/v1/tracks/1mh4GpKKrmlaUkVzoNqhRt', 'id': '1mh4GpKKrmlaUkVzoNqhRt', 'is_local': False, 'name': 'Stretch Deep - feat. Eve Essex', 'preview_url': 'https://p.scdn.co/mp3-preview/ebb7e70b97a5d29e05044a1f920d1fc594f92b26?cid=ea3ef49a097b42d682d3c7bc98832d65', 'track_number': 12, 'type': 'track', 'uri': 'spotify:track:1mh4GpKKrmlaUkVzoNqhRt'}))
        sp_track_2 = spotify.SpAlbumTrack(munch.munchify({'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/25BObiRSDCMwVrBGIVaLIf'}, 'href': 'https://api.spotify.com/v1/artists/25BObiRSDCMwVrBGIVaLIf', 'id': '25BObiRSDCMwVrBGIVaLIf', 'name': 'James K', 'type': 'artist', 'uri': 'spotify:artist:25BObiRSDCMwVrBGIVaLIf'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/1g80vffuPrdapR6S4WyxN3'}, 'href': 'https://api.spotify.com/v1/artists/1g80vffuPrdapR6S4WyxN3', 'id': '1g80vffuPrdapR6S4WyxN3', 'name': 'Eve Essex', 'type': 'artist', 'uri': 'spotify:artist:1g80vffuPrdapR6S4WyxN3'}], 'available_markets': ['AD', 'AE', 'AR', 'AT', 'AU', 'BE', 'BG', 'BH', 'BO', 'BR', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GR', 'GT', 'HK', 'HN', 'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT', 'JO', 'JP', 'KW', 'LB', 'LI', 'LT', 'LU', 'LV', 'MA', 'MC', 'MT', 'MX', 'MY', 'NI', 'NL', 'NO', 'NZ', 'OM', 'PA', 'PE', 'PH', 'PL', 'PS', 'PT', 'PY', 'QA', 'RO', 'SA', 'SE', 'SG', 'SK', 'SV', 'TH', 'TN', 'TR', 'TW', 'US', 'UY', 'VN', 'ZA'], 'disc_number': 1, 'duration_ms': 260446, 'explicit': False, 'external_urls': {'spotify': 'https://open.spotify.com/track/1mh4GpKKrmlaUkVzoNqhRt'}, 'href': 'https://api.spotify.com/v1/tracks/1mh4GpKKrmlaUkVzoNqhRt', 'id': '1mh4GpKKrmlaUkVzoNqhRt', 'is_local': False, 'name': 'Stretch Deep - feat. Eve Essex', 'preview_url': 'https://p.scdn.co/mp3-preview/ebb7e70b97a5d29e05044a1f920d1fc594f92b26?cid=ea3ef49a097b42d682d3c7bc98832d65', 'track_number': 12, 'type': 'track', 'uri': 'spotify:track:1mh4GpKKrmlaUkVzoNqhRt'}))
        self.assertEqual(sp_track_1, sp_track_2)

    def test_sp_album_track_constructor(self):
        sp_track = spotify.SpAlbumTrack(munch.munchify({'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/25BObiRSDCMwVrBGIVaLIf'}, 'href': 'https://api.spotify.com/v1/artists/25BObiRSDCMwVrBGIVaLIf', 'id': '25BObiRSDCMwVrBGIVaLIf', 'name': 'James K', 'type': 'artist', 'uri': 'spotify:artist:25BObiRSDCMwVrBGIVaLIf'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/1g80vffuPrdapR6S4WyxN3'}, 'href': 'https://api.spotify.com/v1/artists/1g80vffuPrdapR6S4WyxN3', 'id': '1g80vffuPrdapR6S4WyxN3', 'name': 'Eve Essex', 'type': 'artist', 'uri': 'spotify:artist:1g80vffuPrdapR6S4WyxN3'}], 'available_markets': ['AD', 'AE', 'AR', 'AT', 'AU', 'BE', 'BG', 'BH', 'BO', 'BR', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GR', 'GT', 'HK', 'HN', 'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT', 'JO', 'JP', 'KW', 'LB', 'LI', 'LT', 'LU', 'LV', 'MA', 'MC', 'MT', 'MX', 'MY', 'NI', 'NL', 'NO', 'NZ', 'OM', 'PA', 'PE', 'PH', 'PL', 'PS', 'PT', 'PY', 'QA', 'RO', 'SA', 'SE', 'SG', 'SK', 'SV', 'TH', 'TN', 'TR', 'TW', 'US', 'UY', 'VN', 'ZA'], 'disc_number': 1, 'duration_ms': 260446, 'explicit': False, 'external_urls': {'spotify': 'https://open.spotify.com/track/1mh4GpKKrmlaUkVzoNqhRt'}, 'href': 'https://api.spotify.com/v1/tracks/1mh4GpKKrmlaUkVzoNqhRt', 'id': '1mh4GpKKrmlaUkVzoNqhRt', 'is_local': False, 'name': 'Stretch Deep - feat. Eve Essex', 'preview_url': 'https://p.scdn.co/mp3-preview/ebb7e70b97a5d29e05044a1f920d1fc594f92b26?cid=ea3ef49a097b42d682d3c7bc98832d65', 'track_number': 12, 'type': 'track', 'uri': 'spotify:track:1mh4GpKKrmlaUkVzoNqhRt'}))
        self.assertEqual(sp_track.artists[0].name, 'James K')

    def test_sp_album_equality(self):
        sp_album_1 = spotify.SpAlbum(munch.munchify(get_album_by_id_response))
        sp_album_2 = spotify.SpAlbum(munch.munchify(get_album_by_id_response))
        self.assertEqual(sp_album_1, sp_album_2)

    def test_sp_query_albums_resp_equality(self):
        sp_query_album_1 = spotify.SpQueryRespWrapper(munch.munchify({'albums': {'href': 'https://api.spotify.com/v1/search?query=album%3AGrafts+artist%3AKara-Lis+Coverdale&type=album&offset=0&limit=10', 'items': [{'album_type': 'single', 'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/5pHUdo5THDtmE9yu3iC2hA'}, 'href': 'https://api.spotify.com/v1/artists/5pHUdo5THDtmE9yu3iC2hA', 'id': '5pHUdo5THDtmE9yu3iC2hA', 'name': 'Kara-Lis Coverdale', 'type': 'artist', 'uri': 'spotify:artist:5pHUdo5THDtmE9yu3iC2hA'}], 'available_markets': ['AD', 'AE', 'AR', 'AT', 'AU', 'BE', 'BG', 'BH', 'BO', 'BR', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GR', 'GT', 'HK', 'HN', 'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT', 'JO', 'JP', 'KW', 'LB', 'LI', 'LT', 'LU', 'LV', 'MA', 'MC', 'MT', 'MX', 'MY', 'NI', 'NL', 'NO', 'NZ', 'OM', 'PA', 'PE', 'PH', 'PL', 'PS', 'PT', 'PY', 'QA', 'RO', 'SA', 'SE', 'SG', 'SK', 'SV', 'TH', 'TN', 'TR', 'TW', 'US', 'UY', 'VN', 'ZA'], 'external_urls': {'spotify': 'https://open.spotify.com/album/6hT28oOwJbnRX9qvxbXbTw'}, 'href': 'https://api.spotify.com/v1/albums/6hT28oOwJbnRX9qvxbXbTw', 'id': '6hT28oOwJbnRX9qvxbXbTw', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/e462332bfd17049e0ed66ee405550eb0a450b036', 'width': 640}, {'height': 300, 'url': 'https://i.scdn.co/image/501f4363400b5844f9378052efdf691c688c933c', 'width': 300}, {'height': 64, 'url': 'https://i.scdn.co/image/10cbb9e4bbfc9057c08a2628e9b6c81d73b9d51f', 'width': 64}], 'name': 'Grafts', 'release_date': '2017-05-05', 'release_date_precision': 'day', 'total_tracks': 1, 'type': 'album', 'uri': 'spotify:album:6hT28oOwJbnRX9qvxbXbTw'}], 'limit': 10, 'next': None, 'offset': 0, 'previous': None, 'total': 1}}))
        sp_query_album_2 = spotify.SpQueryRespWrapper(munch.munchify({'albums': {'href': 'https://api.spotify.com/v1/search?query=album%3AGrafts+artist%3AKara-Lis+Coverdale&type=album&offset=0&limit=10', 'items': [{'album_type': 'single', 'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/5pHUdo5THDtmE9yu3iC2hA'}, 'href': 'https://api.spotify.com/v1/artists/5pHUdo5THDtmE9yu3iC2hA', 'id': '5pHUdo5THDtmE9yu3iC2hA', 'name': 'Kara-Lis Coverdale', 'type': 'artist', 'uri': 'spotify:artist:5pHUdo5THDtmE9yu3iC2hA'}], 'available_markets': ['AD', 'AE', 'AR', 'AT', 'AU', 'BE', 'BG', 'BH', 'BO', 'BR', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GR', 'GT', 'HK', 'HN', 'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT', 'JO', 'JP', 'KW', 'LB', 'LI', 'LT', 'LU', 'LV', 'MA', 'MC', 'MT', 'MX', 'MY', 'NI', 'NL', 'NO', 'NZ', 'OM', 'PA', 'PE', 'PH', 'PL', 'PS', 'PT', 'PY', 'QA', 'RO', 'SA', 'SE', 'SG', 'SK', 'SV', 'TH', 'TN', 'TR', 'TW', 'US', 'UY', 'VN', 'ZA'], 'external_urls': {'spotify': 'https://open.spotify.com/album/6hT28oOwJbnRX9qvxbXbTw'}, 'href': 'https://api.spotify.com/v1/albums/6hT28oOwJbnRX9qvxbXbTw', 'id': '6hT28oOwJbnRX9qvxbXbTw', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/e462332bfd17049e0ed66ee405550eb0a450b036', 'width': 640}, {'height': 300, 'url': 'https://i.scdn.co/image/501f4363400b5844f9378052efdf691c688c933c', 'width': 300}, {'height': 64, 'url': 'https://i.scdn.co/image/10cbb9e4bbfc9057c08a2628e9b6c81d73b9d51f', 'width': 64}], 'name': 'Grafts', 'release_date': '2017-05-05', 'release_date_precision': 'day', 'total_tracks': 1, 'type': 'album', 'uri': 'spotify:album:6hT28oOwJbnRX9qvxbXbTw'}], 'limit': 10, 'next': None, 'offset': 0, 'previous': None, 'total': 1}}))
        self.assertEqual(sp_query_album_1, sp_query_album_2)





if __name__ == '__main__':
    unittest.main()
