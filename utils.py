import re

ARTIST_MATCH_REGEX = '[A-Za-z0-9\ ]+'
FTS = [
    'ft', 
    'feat', 
    'featuring' 
]

def sum(arg):
    total = 0
    for val in arg:
        total += val
    return total

GEN_FITS = []
for ft in FTS:
    GEN_FITS.append('{}. '.format(ft))
    GEN_FITS.append('({}'.format(ft))
    GEN_FITS.append(' {}'.format(ft))

def strip_ft_artist_from_title(title):
    """
    Takes in a track title and removes the featuring artist (if any) from it
    If there was a featuring artist then this is returned too
    Variation could have:
        - period and space after the word
        - space or open bracket before the word
    """
    if not any(ft in title for ft in GEN_FITS):
        return title, None
    for ft in GEN_FITS:
        if ft in title:
            title_split = title.split(ft)
            stripped_title = title_split[0]
            feat_artist = title_split[1]
            # Logic to handle parenthesis
            # All of this could probably be replaced with regex
            if stripped_title[len(stripped_title) - 1] == '(':
                stripped_title = stripped_title[:len(stripped_title) - 1]
                if feat_artist[len(feat_artist) -1] != ')':
                    print('Title expected to end with ) but does not: {}'.format(title))
                    break
                # TODO handle multiple featuring artists
                feat_artist = feat_artist[:len(feat_artist) - 1]
            return stripped_title.strip(), feat_artist.strip()


def strip_str(str):
    """
        Remove symbols and lowercase from strings.
        Primarily used for artist and title matching.
        E.g.  GM would have artist name as 'Walter Bishop Jr.'
              Spotify might eliminate the full-stop 'Walter Bishop Jr'
    """
    return ''.join(re.findall(ARTIST_MATCH_REGEX, str)).lower()