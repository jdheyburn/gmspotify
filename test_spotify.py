import unittest
import spotify
from unittest.mock import MagicMock
import json
import munch

album_id_fname = 'sp_get_album_by_id.json'
with open(album_id_fname, 'r', encoding='utf-8') as f:
    album_id_response = json.load(f)


class TestClasses(unittest.TestCase):
    
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

    
    def test_get_album_by_id(self):
        """
        Should hit spotify API and return munchified object
        """
        api = spotify.SpApi('id', 'secret')
        expected = spotify.SpAlbumApiResp(album_id_response)
        api.client = MagicMock(album=MagicMock(return_value=album_id_response))
        actual = api.get_album_by_id('album_id')

        api.client.album.assert_called_once_with('album_id')
        self.assertEqual(actual, expected)

        




if __name__ == '__main__':
    unittest.main()
