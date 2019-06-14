import re
from typing import Tuple

ARTIST_MATCH_REGEX = r'[A-Za-z0-9\ ]+'
FEAT_REGEX = r'\-?\ \(?(feat\.?\ |ft\.?\ |featuring\ )([^)]+)\)?'
COMPILED_FEAT_REGEX = re.compile(FEAT_REGEX)


def strip_ft_artist_from_title(title: str) -> Tuple[str, str]:
    """
    Takes in a track title and removes the featuring artist (if any) from it
    If there was a featuring artist then this is returned too
    Variation could have:
        - period and space after the word
        - space or open bracket before the word
    """
    ft_regex_results = COMPILED_FEAT_REGEX.search(title)
    if not ft_regex_results:
        return title, None
    feat_artist = ft_regex_results.group(2)
    stripped_title = re.sub(FEAT_REGEX, '', title)
    return stripped_title.strip(), feat_artist.strip()


def strip_str(str: str) -> str:
    """
    Remove symbols and lowercase from strings.
    Primarily used for artist and title matching.
    E.g.  GM would have artist name as 'Walter Bishop Jr.'
            Spotify might eliminate the full-stop 'Walter Bishop Jr'
    """
    return ''.join(re.findall(ARTIST_MATCH_REGEX, str)).lower()
