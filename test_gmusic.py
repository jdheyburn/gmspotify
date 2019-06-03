import unittest

from gmusic import GMusicTrack, GMusicAlbum
from typing import List

id = 'Bi5vplouym4ugzrtyyx7c7jh5fa'
album_artist = 'Various Artists'
title = 'Mono No Aware'
album = GMusicAlbum(id, title, album_artist)
track = GMusicTrack('Limerence', 'Yves Tumor')


class TestClasses(unittest.TestCase):

    def test_track_constructor_no_rating(self):
        """
        Should construct track correctly with empty rating
        """
        title = 'Good Times'
        artist = 'Chic'
        actual = GMusicTrack(title, artist)
        self.assertEqual(actual.title, title)
        self.assertEqual(actual.artist, artist)
        self.assertEqual(actual.rating, '')
    
    def test_track_constructor_with_rating(self):
        """
        Should construct track correctly with rating
        """
        title = 'Good Times'
        artist = 'Chic'
        rating = '5'
        actual = GMusicTrack(title, artist, rating)
        self.assertEqual(actual.title, title)
        self.assertEqual(actual.artist, artist)
        self.assertEqual(actual.rating, rating)

    def test_album_constructor_no_year(self):
        """
        Should construct album correctly with no year specified
        """
        id = 'Bi5vplouym4ugzrtyyx7c7jh5fa'
        album_artist = 'Various Artists'
        title = 'Mono No Aware'
        actual = GMusicAlbum(id, title, album_artist)
        self.assertEqual(actual.id, id)
        self.assertEqual(actual.album_artist, album_artist)
        self.assertEqual(actual.title, title)
        self.assertEqual(actual.year, '')
        self.assertDictEqual(actual.tracks, {})
    

    # def test_album_constructor_with_year(self):
    #     """
    #     Should construct album correctly with year specified
    #     """
    #     id = 'Bi5vplouym4ugzrtyyx7c7jh5fa'
    #     album_artist = 'Various Artists'
    #     title = 'Mono No Aware'
    #     year = '2017'
    #     actual = GMusicAlbum(id, title, album_artist, year)
    #     self.assertEqual(actual.id, id)
    #     self.assertEqual(actual.album_artist, album_artist)
    #     self.assertEqual(actual.title, title)
    #     self.assertEqual(actual.year, year)
    #     self.assertDictEqual(actual.tracks, {})

    # TODO this breaks above test?
    def test_add_track_to_album(self):
        """
        Should add track to album
        """
        album.add_track(3, track)
        self.assertEqual(album.tracks.get(3).title, 'Limerence')



if __name__ == '__main__':
    unittest.main()
