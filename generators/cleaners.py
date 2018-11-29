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


def case_uuid(sample):
    if not isinstance(sample[GENERIC_UID], str) or 'haib' not in sample[GENERIC_UID]:
        return
    hauid = sample[HAUID].split('_')
    haib = 'haib' + hauid[0].split('haib')[1].upper()
    flow = hauid[1].upper()
    sl = hauid[2].upper()
    sample[HAUID] = f'{haib}_{flow}_{sl}'


def clean_metasub_name(sample):
    if not isinstance(sample[METASUB_NAME], str):
        return
    msub = sample[METASUB_NAME]
    msub = msub.upper()
    msub = ''.join(msub.split(' '))
    msub = '-'.join(msub.split('_'))
    if msub[:4] == 'GCSD':
        msub = msub[1:]

    if 'CSD-DENVER.METASUB-06/21/16' in msub:
        snum = msub.split('-')[-1]
        msub = f'CSD-DEN-{snum}'

    sample[METASUB_NAME] = msub


CLEANERS = [
    turn_off_checking,
    uppercase_token(SL_NAME),
    uppercase_token(HA_FLOWCELL),
    uppercase_token(INDEX_SEQ),
    case_hauid,
    case_ha_proj,
    clean_metasub_name,
    case_uuid,
]