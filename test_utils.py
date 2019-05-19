import unittest

import utils

class TestUtils(unittest.TestCase):


    def test_strip_str(self):
        """
        Should strip a string to remove symbols and lowercase it
        """
        artist = 'Walter Bishop Jr.'
        expected = 'walter bishop jr'
        actual = utils.strip_str(artist)
        self.assertEqual(actual, expected)


    def test_strip_ft_artist_no_fts(self):
        """
        Should return the title as is with no featuring artists
        """
        title = 'Defeat'
        expected = (title, None)
        actual = utils.strip_ft_artist_from_title(title)
        self.assertTupleEqual(actual, expected)
    

    def test_strip_ft_artist_one_ft_brackets(self):
        """
        Given featuring one Artist in brackets, should return stripped title and that one artist
        """
        title = 'Jim Jones At Botany Bay (From "The Hateful Eight" Soundtrack) (feat. Kurt Russell)'
        expected = ('Jim Jones At Botany Bay (From "The Hateful Eight" Soundtrack)', 'Kurt Russell')
        actual = utils.strip_ft_artist_from_title(title)
        self.assertTupleEqual(actual, expected)


    def test_strip_ft_artist_one_ft_no_brackets(self):
        """
        Given featuring one Artist not in brackets, should return stripped title and that one artist
        """
        title = 'Tha Lyot Remix feat. DJ Roy'
        expected = ('Tha Lyot Remix', 'DJ Roy')
        actual = utils.strip_ft_artist_from_title(title)
        self.assertTupleEqual(actual, expected)

    
    def test_strip_ft_artist_one_ft_brackets_more_content(self):
        """
        Given featuring one Artist in brackets and more text after the Feat
        Should return stripped title and that one artist
        """
        title = 'WYWD (feat. Kelela) (Remix)'
        expected = ('WYWD', 'Kelela')
        actual = utils.strip_ft_artist_from_title(title)
        self.assertTupleEqual(actual, expected)
    





if __name__ == '__main__':
    unittest.main()