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
        self.check_overwrite = True
        self.no_check = set([CITY, HA_ID])
        self.current_setter = 'unknown'
        self.unchangeable = set()

    def to_son(self):
        rough = {k: v for k, v in self.props.items() if v}
        to_upper = [HA_ID, METASUB_NAME, PROJECT, CITY_CODE]
        for k in to_upper:
            if k in rough:
                rough[k] = str(rough[k]).upper()
        return rough

    def __str__(self):
        return str(self.to_son())

    def __getitem__(self, key):
        try:
            return self.props[key]
        except KeyError:
            return None

    def set_current_setter(self, val):
        self.current_setter = val

    def set_unchangeable(self, val):
        self.unchangeable.add(val)

    def __setitem__(self, key, val):
        self.setitem(key, val)

    def setitem(self, key, val, setter='unknown'):
        val = str(val).strip()
        if not val or val in ['na', 'other', 'inbetween', 'nan']:
            return
        if key in self.unchangeable:
            return

        if self.check_overwrite and (key in self.props) and (key not in self.no_check):
            current = str(self.props[key]).lower().strip().replace('\n', ' ')
            val = val.lower().strip().replace('\n', ' ')
            if current not in ['other']:
                try:
                    current, val = float(current), float(val)
                    test = abs(val - current) < 0.1
                    if key in ['latitude', 'longitude'] and current == 0.01:
                        test = True
                    if key == 'latitude':
                        city_lat = float(self.props.get('city_latitude', current))
                        if abs(current - city_lat) > 1:
                            test = True
                        elif abs(val - city_lat) > 1:
                            test = True
                            val = current
                    if key == 'longitude':
                        city_lat = float(self.props.get('city_longitude', current))
                        if abs(current - city_lat) > 1:
                            test = True
                        elif abs(val - city_lat) > 1:
                            test = True
                            val = current
                except ValueError:
                    test = current == val
                    if val in current:
                        test = True
                        val = current
                    if current in val:
                        test = True
                    if val.replace(' ', '_') == current.replace(' ', '_'):
                        test = True
                    if val.replace('-', '_') == current.replace('-', '_'):
                        test = True
                    if val.replace('/', '_') == current.replace('/', '_'):
                        test = True
                    if 'csd_denver' in current and 'csd16-den' in val:
                        test = True
                for allowed_pair in [
                    ('positive_control', 'ctrl cities'),
                    ('csd16-scl copan control 3/3', 'csd16-scl-ctrl-3-3'),
                    ('csd16-bog-negative control 2', 'csd16-bog-neg-2'),
                    ('csd denver 2016 control 2', 'csd16-den-cntr-2'),
                    ('shrine', 'church'),
                    ('winter2014', 'pathomap_winter'),
                    ('winter_nyc', 'pathomap_winter'),
                ]:
                    if tuple(sorted((current, val))) == tuple(sorted(allowed_pair)):
                        test = True

                if key == 'line':
                    val = current
                    test = True
                if key == METASUB_NAME:
                    try:
                        int(val)  # val is actually a barcode, common swap
                        test = True
                        val = current
                    except ValueError:
                        pass
                    try:
                        int(current) # current is actually a barcode, common swap
                        test = True
                    except ValueError:
                        pass

                if key == INDEX_SEQ and current != val:
                    test = True
                    val = f'{current};{val}'
                if key == SURFACE and current != val:
                    test = True
                    val = f'{current};{val}'
                if key == METASUB_NAME and 'csd_denver' in str(val):
                    test = True
                    val = current
                if key.lower() == PROJECT.lower() and 'pilot_' in self.props[GENERIC_UID].lower() and current.lower() == PILOT_CODE.lower():
                    test = True
                    val = PILOT_CODE
                try:
                    msg = f'{self.props[GENERIC_UID]} {key}\n\tSetter: {self.setby[key]}\n\tCUR: [{current}]\n\tNEW: [{val}]'
                except KeyError:
                    raise
                assert test, msg
        if setter == 'unknown':
            setter = self.current_setter
        if val:
            self.props[key] = str(val)
            self.setby[key] = setter

    @classmethod
    def from_name(cls, name, setter='unknown'):
        kind = guess_name_kind(name)
        obj = cls()
        obj.setitem(kind, name, setter=setter)
        obj.set_unchangeable(kind)
        return obj
