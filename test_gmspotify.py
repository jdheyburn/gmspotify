import unittest
import json

import gmspotify
import gmusic

gm_response_fname = 'gm_tracks_dump_small.json'
with open(gm_response_fname, 'r', encoding='utf-8') as f:
    gm_response = json.load(f)

class TestUtils(unittest.TestCase):

    # TODO way of testing this properly using equality?
    def test_parse_gm_lib(self):
        """
        Should correctly parse list of tracks retrieved from Google Music to correct map
        """
        
        expected_album1_tracks = {
            1: {
                3: gmusic.GMusicTrack('Elegant Design', 'Pond'),
                4: gmusic.GMusicTrack('Sorry I Was Under The Sky', 'Pond')
            }
        }
        expected_album1 = gmusic.GMusicAlbum(
            'Byqh4iypmkshcvqpvscncu62faa',
            'Beard, Wives, Denim',
            'Pond',
            '2012',
            expected_album1_tracks
        )

        expected_album2_tracks = {
            2: {
                10: gmusic.GMusicTrack('B.E. (Unmixed Version)', 'Calvin Keys'),
                11: gmusic.GMusicTrack('Time and Space (Unmixed Version)', 'Rudolph Johnson'),
                12: gmusic.GMusicTrack('Blue Bossa (Unmixed Version)', 'Walter Bishop Jr.')
            }
        }
        expected_album2 = gmusic.GMusicAlbum(
            'Bzcy7ul6glqnhuthtp7dnmrudbi',
            'Black Jazz Signature',
            'Theo Parrish',
            '',
            expected_album2_tracks
        )

        albums: MutableMapping[str, gmusic.GMusicAlbum] = {
            'Bzcy7ul6glqnhuthtp7dnmrudbi': expected_album2,
            'Byqh4iypmkshcvqpvscncu62faa': expected_album1
            
        }

        actual = gmspotify.parse_lib(gm_response)
        self.maxDiff = None
        self.addTypeEqualityFunc
        self.assertEqual(actual, albums)
        


if __name__ == '__main__':
    unittest.main()
