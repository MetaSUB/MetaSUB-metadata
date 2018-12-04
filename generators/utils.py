
from os.path import join
from .constants import METADATA_DIR


def mdata_dir(fname):
    return join(METADATA_DIR, fname)


def getOrNone(tbl, key, default=None):
    if key is None:
        return default
    try:
        return tbl[key]
    except KeyError:
        return default


def remove_leading_char(char, ignore_case=True):
    def remover(val):
        leader = val[0]
        my_char = char
        if ignore_case:
            leader = leader.upper()
            my_char = my_char.upper()
        if leader == my_char:
            #print(f'{leader} {char} {val[1:]}', file=stderr)
            return val[1:]
        return val
    return remover


def remove_trailing_char(char, ignore_case=True):
    def remover(val):
        trailer = val[-1]
        my_char = char
        if ignore_case:
            trailer = trailer.upper()
            my_char = my_char.upper()
        if trailer == my_char:
            #print(f'{leader} {char} {val[1:]}', file=stderr)
            return val[:-1]
        return val
    return remover


def clean_ha_id(ha_id):
    return ha_id.lower().split('r')[0]
