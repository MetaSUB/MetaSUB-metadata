from .constants import *
from sys import stderr


def guess_name_kind(name):
    if name[:4] == 'haib':
        return HAUID
    if name[:2] == 'SL':
        return SL_NAME
    if name[:6].lower() == 'pilot_':
        return OTHER_PROJ_UID
    if name[:10].lower() == 'sossowski_':
        return OTHER_PROJ_UID
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
        self.setby = {}
        self.check_overwrite = False
        self.no_check = set([CITY])

    def to_son(self):
        rough = {k: v for k, v in self.props.items() if v}
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
        if self.check_overwrite and (key in self.props) and (key not in self.no_check):
            assert self.props[key].lower() == val.lower(), \
                f'{self.props[HAUID]} {key} CUR: {self.props[key]} NEW: {val}'
        if val is None:
            return
        val = str(val).strip()
        if val:
            self.props[key] = val


    @classmethod
    def from_name(cls, name):
        kind = guess_name_kind(name)
        obj = cls()
        obj[kind] = name
        return obj
