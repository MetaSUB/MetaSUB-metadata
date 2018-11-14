from .constants import *
from sys import stderr


def turn_off_checking(sample):
    sample.check_overwrite = False


def uppercase_token(token):
    def do_the_case(sample):
        if not isinstance(sample[token], str):
            return
        sample[token] = sample[token].upper()
    return do_the_case


def case_ha_proj(sample):
    if not isinstance(sample[HA_PROJ], str):
        return
    sample[HA_PROJ] = 'haib' + sample[HA_PROJ].split('haib')[1].upper()


def case_hauid(sample):
    if not isinstance(sample[HAUID], str):
        return
    hauid = sample[HAUID].split('_')
    haib = 'haib' + hauid[0].split('haib')[1].upper()
    flow = hauid[1].upper()
    sl = hauid[2].upper()
    sample[HAUID] = f'{haib}_{flow}_{sl}'


CLEANERS = [
    turn_off_checking,
    uppercase_token(SL_NAME),
    uppercase_token(HA_FLOWCELL),
    uppercase_token(INDEX_SEQ),
    case_hauid,
    case_ha_proj,
]