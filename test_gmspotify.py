import unittest
import json

import gmspotify


class TestUtils(unittest.TestCase):

    def test_parse_gm_lib(self):
        """
        Should correctly parse list of tracks retrieved from Google Music to correct map
        """
        lib = json.loads('spotify_songs_dump.json')
        


if __name__ == '__main__':
    unittest.main()
