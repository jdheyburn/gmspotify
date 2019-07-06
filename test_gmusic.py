import unittest

from gmusic import GMusicTrack, GMusicAlbum, DuplicateTrackError, parse_lib
from typing import List
import json

id = 'Bi5vplouym4ugzrtyyx7c7jh5fa'
album_artist = 'Various Artists'
title = 'Mono No Aware'
track = GMusicTrack('Limerence', 'Yves Tumor')
track2 = GMusicTrack('Zhao Hua', 'HVAD & Pan Daijing')

gm_response_fname = 'gm_tracks_dump_small.json'
with open(gm_response_fname, 'r', encoding='utf-8') as f:
    gm_response = json.load(f)


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

    def test_album_total_tracks_count_one_disc(self):
        """
        Given tracks have been added to tracks across 1 disc
        Should return the correct number of tracks added
        """
        album = GMusicAlbum(id, title, album_artist)
        album.add_track(1, 3, track)
        album.add_track(1, 2, track)
        expected = 2
        actual = album.total_tracks()
        self.assertEqual(actual, expected)

    def test_album_total_tracks_count_two_discs(self):
        """
        Given tracks have been added to tracks across 2 discs
        Should return the correct number of tracks added
        """
        album = GMusicAlbum(id, title, album_artist)
        album.add_track(1, 3, track)
        album.add_track(1, 2, track)
        album.add_track(2, 1, track)
        expected = 3
        actual = album.total_tracks()
        self.assertEqual(actual, expected)

    def test_discs_added(self):
        """
        Given tracks have been added to tracks across 2 discs
        Should return the correct number of discs
        """
        album = GMusicAlbum(id, title, album_artist)
        album.add_track(1, 3, track)
        album.add_track(1, 2, track)
        album.add_track(2, 1, track)
        expected = set([1,2])
        actual = album.discs_added()
        self.assertEqual(actual, expected)


# class TestOther(unittest.TestCase):
    # TODO way of testing this properly using equality?
    # def test_parse_gm_lib(self):
    #     """
    #     Should correctly parse list of tracks retrieved from Google Music to correct map
    #     """
        
    #     expected_album1_tracks = {
    #         1: {
    #             3: GMusicTrack('Elegant Design', 'Pond'),
    #             4: GMusicTrack('Sorry I Was Under The Sky', 'Pond')
    #         }
    #     }
    #     expected_album1 = GMusicAlbum(
    #         'Byqh4iypmkshcvqpvscncu62faa',
    #         'Beard, Wives, Denim',
    #         'Pond',
    #         '2012',
    #         expected_album1_tracks
    #     )

    #     expected_album2_tracks = {
    #         2: {
    #             10: GMusicTrack('B.E. (Unmixed Version)', 'Calvin Keys'),
    #             11: GMusicTrack('Time and Space (Unmixed Version)', 'Rudolph Johnson'),
    #             12: GMusicTrack('Blue Bossa (Unmixed Version)', 'Walter Bishop Jr.')
    #         }
    #     }
    #     expected_album2 = GMusicAlbum(
    #         'Bzcy7ul6glqnhuthtp7dnmrudbi',
    #         'Black Jazz Signature',
    #         'Theo Parrish',
    #         '',
    #         expected_album2_tracks
    #     )

    #     albums: MutableMapping[str, GMusicAlbum] = {
    #         'Bzcy7ul6glqnhuthtp7dnmrudbi': expected_album2,
    #         'Byqh4iypmkshcvqpvscncu62faa': expected_album1
            
    #     }

    #     actual = parse_lib(gm_response)
    #     self.maxDiff = None
    #     self.assertEqual(actual, albums)


if __name__ == '__main__':
    unittest.main()
