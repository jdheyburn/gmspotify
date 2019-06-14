import unittest
import json

import gmspotify
import gmusic
import munch



class TestGetSTrackArtists(unittest.TestCase):

    def test_get_s_track_artists(self):
        """
        Given a s_track record with multiple artists
        Should return a list of those artists
        """
        s_track = munch.munchify({'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/25BObiRSDCMwVrBGIVaLIf'}, 'href': 'https://api.spotify.com/v1/artists/25BObiRSDCMwVrBGIVaLIf', 'id': '25BObiRSDCMwVrBGIVaLIf', 'name': 'James K', 'type': 'artist', 'uri': 'spotify:artist:25BObiRSDCMwVrBGIVaLIf'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/1g80vffuPrdapR6S4WyxN3'}, 'href': 'https://api.spotify.com/v1/artists/1g80vffuPrdapR6S4WyxN3', 'id': '1g80vffuPrdapR6S4WyxN3', 'name': 'Eve Essex', 'type': 'artist', 'uri': 'spotify:artist:1g80vffuPrdapR6S4WyxN3'}], 'available_markets': ['AD', 'AE', 'AR', 'AT', 'AU', 'BE', 'BG', 'BH', 'BO', 'BR', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GR', 'GT', 'HK', 'HN', 'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT', 'JO', 'JP', 'KW', 'LB', 'LI', 'LT', 'LU', 'LV', 'MA', 'MC', 'MT', 'MX', 'MY', 'NI', 'NL', 'NO', 'NZ', 'OM', 'PA', 'PE', 'PH', 'PL', 'PS', 'PT', 'PY', 'QA', 'RO', 'SA', 'SE', 'SG', 'SK', 'SV', 'TH', 'TN', 'TR', 'TW', 'US', 'UY', 'VN', 'ZA'], 'disc_number': 1, 'duration_ms': 260446, 'explicit': False, 'external_urls': {'spotify': 'https://open.spotify.com/track/1mh4GpKKrmlaUkVzoNqhRt'}, 'href': 'https://api.spotify.com/v1/tracks/1mh4GpKKrmlaUkVzoNqhRt', 'id': '1mh4GpKKrmlaUkVzoNqhRt', 'is_local': False, 'name': 'Stretch Deep - feat. Eve Essex', 'preview_url': 'https://p.scdn.co/mp3-preview/ebb7e70b97a5d29e05044a1f920d1fc594f92b26?cid=ea3ef49a097b42d682d3c7bc98832d65', 'track_number': 12, 'type': 'track', 'uri': 'spotify:track:1mh4GpKKrmlaUkVzoNqhRt'})
        expected = ['Eve Essex', 'James K']
        actual = gmspotify.get_s_track_artists(s_track)
        self.assertEqual(actual, expected)

class TestGetGMTrackArtists(unittest.TestCase):

    def test_get_gm_track_artists_ampersand(self):
        """
        Given a GM Track with an artist string containing multiple artists
        Should return a list of those artists
        """
        gm_track = gmusic.GMusicTrack(title='Zhao Hua', artist='HVAD & Pan Daijing')
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

        


if __name__ == '__main__':
    unittest.main()
