from .constants import *


def guess_name_kind(name):
    if name[:2] == 'SL':
        return SL_NAME
    if 'cem' in name.lower():
        return HA_ID
    if 'db' in name.lower():
        return HA_ID
    if 'csd16' in name.lower():
        return METASUB_NAME
    if 'oly' in name.lower():
        return METASUB_NAME
    tkns = name.split('_')
    if len(tkns) == 3:
        return METASUB_NAME
    if 'porto' in name.lower():
        return METASUB_NAME
    return 'unknown'


def clean_token(tkn):
    tkn = tkn.strip()
    tkn = '_'.join(tkn.split())
    tkn = tkn.lower()
    return tkn


class Sample:

    def __init__(self):
        self.props = {}

    def to_son(self):
        rough = {k: clean_token(v) for k, v in self.props.items() if v}
        to_upper = [HA_ID, METASUB_NAME, PROJECT, CITY_CODE]
        for k in to_upper:
            if k in rough:
                rough[k] = rough[k].upper()
        return rough

    def __str__(self):
        return str(self.to_son())

    def __getitem__(self, key):
        try:
            return self.props[key]
        except KeyError:
            return None

    def __setitem__(self, key, val):
        self.props[key] = val

    @classmethod
    def from_name(cls, name):
        kind = guess_name_kind(name)
        obj = cls()
        obj[kind] = name
        return obj
