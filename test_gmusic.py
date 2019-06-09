import unittest

from gmusic import GMusicTrack, GMusicAlbum, DuplicateTrackError
from typing import List

id = 'Bi5vplouym4ugzrtyyx7c7jh5fa'
album_artist = 'Various Artists'
title = 'Mono No Aware'
track = GMusicTrack('Limerence', 'Yves Tumor')
track2 = GMusicTrack('Zhao Hua', 'HVAD & Pan Daijing')


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
        actual = GMusicAlbum(id, title, album_artist)
        self.assertEqual(actual.id, id)
        self.assertEqual(actual.album_artist, album_artist)
        self.assertEqual(actual.title, title)
        self.assertEqual(actual.year, '')
        self.assertEqual(actual.tracks, {})
    

    def test_album_constructor_with_year(self):
        """
        Should construct album correctly with year specified
        """
        year = '2017'
        actual = GMusicAlbum(id, title, album_artist, year)
        self.assertEqual(actual.id, id)
        self.assertEqual(actual.album_artist, album_artist)
        self.assertEqual(actual.title, title)
        self.assertEqual(actual.year, year)
        self.assertEqual(actual.tracks, {})

    def test_add_track_to_album(self):
        """
        Should add track to album
        """
        album = GMusicAlbum(id, title, album_artist)
        album.add_track(1, 3, track)
        self.assertEqual(len(album.tracks), 1)
        self.assertEqual(len(album.tracks[1]), 1)
        self.assertEqual(album.tracks.get(1).get(3).title, 'Limerence')
    
    def test_throw_error_if_track_exists(self):
        """
        Should throw DuplicateTrackError given track for disc already exists
        """
        album = GMusicAlbum(id, title, album_artist)
        album.add_track(1, 3, track)
        self.assertRaises(DuplicateTrackError, album.add_track, 1, 3, track)

    def test_add_track_to_album_on_another_disc(self):
        """
        Should add track to album given same trackNum on different disc
        """
        album = GMusicAlbum(id, title, album_artist)
        album.add_track(1, 3, track)
        album.add_track(2, 3, track2)
        self.assertEqual(len(album.tracks[2]), 1)
        self.assertEqual(album.tracks.get(2).get(3).title, 'Zhao Hua')

    def test_track_equality(self):
        """Should mark two separate track instances as the same"""
        track1 = GMusicTrack('testtitle', 'testartist')
        track2 = GMusicTrack('testtitle', 'testartist')
        self.assertEqual(track1, track2)

    def test_album_equality(self):
        """Should mark two separate album instances as the same"""
        album1 = GMusicAlbum('123', 'testtitle', 'testalbumartist')
        album2 = GMusicAlbum('123', 'testtitle', 'testalbumartist')
        self.assertEqual(album1, album2)


if __name__ == '__main__':
    unittest.main()
