from .parsing import parse_csv
from .constants import *
from .utils import getOrNone
from .table_mapper import Table, token_mapper, token_specific_val_func
from sys import stderr


sl_name_to_ha_name = Table(
    join(METADATA_DIR, 'filenames_HCY5HCCXY.tsv'),
    {SL_NAME: 2, HA_ID: 3},
    token_mapper(HA_ID),
    name_func=token_specific_val_func(**{SL_NAME: lambda x: x.lower()}),
    sep='\t'
)


ha_name_to_pos = Table(
    join(METADATA_DIR, 'HA Submissions-Grid view.csv'),
    {HA_ID: 0, PLATE_NUM: 8, PLATE_POS: 14},
    token_mapper(PLATE_NUM, PLATE_POS),
    assert_len=15
)


airsample_sl_to_ha = Table(
    join(METADATA_DIR, 'air_samples.filenames_HK7G5CCXY.txt'),
    {SL_NAME: 2, HA_ID: 3},
    token_mapper(HA_ID),
    name_func=token_specific_val_func(**{SL_NAME: lambda x: x.lower()}),
    skip=2,
    sep='\t'
)


def airsample_ha_to_msub_mapper(sample, sample_id, vec):
    sample[METASUB_NAME] = vec[METASUB_NAME]
    sample[PROJECT] = CSD17_CODE


airsample_ha_to_msub = Table(
    join(METADATA_DIR, 'airsamples_ha_id_to_msub_name.csv'),
    {HA_ID: 1, METASUB_NAME: 4},
    airsample_ha_to_msub_mapper,
    val_func=token_specific_val_func(**{METASUB_NAME: lambda x: x[1:]}),
    assert_len=5,
    skip=1

)


bc_to_meta = Table(
    join(METADATA_DIR, 'cleaned_simplified_metadata.csv'),
    {
        CITY: 0,
        BC: 1,
        SURFACE_MATERIAL: 2,
        SURFACE: 3,
        SETTING: 4,
        ELEVATION: 5,
        TRAFFIC_LEVEL: 6,
        LAT: 7,
        LON: 8,
        METASUB_NAME: 9,
    },
    token_mapper(
        CITY, SURFACE_MATERIAL, SURFACE, SETTING,
        ELEVATION, TRAFFIC_LEVEL, LAT, LON, METASUB_NAME
    )
)


def csd16_metadata_name_func(name, name_type):
    name = name.lower()
    name = '-'.join(name.split('_'))
    if 'csd2016' in name:
        name = 'csd16'.join(name.split('csd2016'))
    return name


csd16_metadata = Table(
    join(METADATA_DIR, 'collated_metadata_csd16.csv'),
    {
        METASUB_NAME: 31,
        CITY: 14,
        SURFACE_MATERIAL: 36,
        SURFACE: 35,
        TRAFFIC_LEVEL: 23,
        LAT: 17,
        LON: 20,
    },
    token_mapper(CITY, SURFACE, SURFACE_MATERIAL, TRAFFIC_LEVEL, LAT, LON),
    name_func=csd16_metadata_name_func,
)


akl_metadata_csd16 = Table(
    join(METADATA_DIR, 'auckland_csd16.csv'),
    {
        METASUB_NAME: 5,
        CITY: 32,
        SURFACE_MATERIAL: 9,
        SETTING: 8,
        LAT: 30,
        LON: 29,
    },
    token_mapper(CITY, SURFACE_MATERIAL, SETTING, LAT, LON),
    name_func=lambda x, y: x.upper(),
    skip=1
)


def fairbanks_metadata_csd16_val_func(val, token):
    if token == SURFACE:
        return '_'.join(val.split())
    return val


fairbanks_metadata_csd16 = Table(
    join(METADATA_DIR, 'Fairbanks_corralled_CSD16.csv'),
    {
        METASUB_NAME: 0,
        SURFACE_MATERIAL: 5,
        SURFACE: 4,
    },
    token_mapper(SURFACE, SURFACE_MATERIAL),
    name_func=lambda x, y: x.upper(),
    val_func=fairbanks_metadata_csd16_val_func,
    skip=1
)


tigress_metadata = Table(
    join(METADATA_DIR, 'metadata.MetaSUB_UK2017.csv'),
    {
        HA_ID: 8,
        CITY: 0,
        LOCATION_TYPE: 1,
        LAT: 2,
        LON: 3,
        SETTING: 4,
        ELEVATION: 5,
        SURFACE: 6,
        SURFACE_MATERIAL: 7,
    },
    token_mapper(
        CITY, LOCATION_TYPE, LAT, LON, SETTING, ELEVATION, SURFACE,
        SURFACE_MATERIAL
    ),
    name_func=lambda x, y: '-'.join(x.lower().split('_')),
)


class MSubToCity:
    """Guess the city or city code from the MetaSUB name."""

    def map(self, sample):
        if not sample[METASUB_NAME]:
            return
        codes = {
            'oly': 'rio_de_janeiro',
            'porto': 'porto',
        }
        for code, city_name in codes.items():
            if code in sample[METASUB_NAME].lower():
                sample[CITY] = city_name
                return

        if 'csd' in sample[METASUB_NAME].lower():
            tkns = sample[METASUB_NAME].split('-')
            if len(tkns) == 3:
                sample[CITY_CODE] = tkns[1]
            return

        tkns = sample[METASUB_NAME].split('_')
        if len(tkns) == 3:
            sample[CITY] = 'berlin'


class CityCodeToCity:

    def map(self, sample):
        code_map = {
            'FAI': 'fairbanks',
            'NYC': 'new_york_city',
            'OFA': 'ofa',
            'AKL': 'auckland',
            'HAM': 'hamilton',
            'SAC': 'sacramento',
            'SCL': 'santiago',
            'BOG': 'bogota',
            'ILR': 'ilorin',
            'TOK': 'tokyo',
            'LON': 'london',
            'HKG': 'hong_kong',
            'OSL': 'oslo',
            'DEN': 'denver',
            'STO': 'stockholm',
            'RIO': 'rio_de_janeiro',
            'POR': 'porto',
            'BER': 'berlin',
            'SAP': 'sao_paulo',
        }
        city_map = {v: k for k, v in code_map.items()}
        if sample[CITY_CODE] and not sample[CITY]:
            try:
                sample[CITY] = code_map[sample[CITY_CODE]]
            except KeyError:
                pass
        elif sample[CITY] and not sample[CITY_CODE]:
            try:
                sample[CITY_CODE] = city_map[sample[CITY]]
            except KeyError:
                pass


class Handle5106HANames:
    """HA IDs matching 5106-CEM come from either London gCSD17
    or NYC winter pathomap.
    """

    def __init__(self):
        self.conv_tbl = {
            tkns[5]: (tkns[0], (tkns[1], tkns[2]))
            for tkns in parse_csv(
                join(METADATA_DIR, 'Conversion Tables-Table 1.csv')
            )
        }

        self.mdata_tbl = {
            tkns[0]: [
                (CITY, 'london'),
                (SETTING, tkns[31]),
                (PROJECT, CSD17_CODE),
                (LAT, tkns[26]),
                (LON, tkns[27]),
                (SURFACE_MATERIAL, tkns[37]),
                (SURFACE_MATERIAL, tkns[33]),
                (ELEVATION, tkns[32]),
            ]
            for tkns in parse_csv(join(METADATA_DIR, 'Metadata-Table 1.csv'))
        }

    def map(self, sample):
        if not sample[HA_ID]:
            return
        if sample[HA_ID].lower() not in self.conv_tbl:
            if '5106-cem' in sample[HA_ID].lower():
                sample[CITY] = 'new_york_city'
                sample[PROJECT] = PATHOMAP_WINTER_CODE
            return

        internal_name, pos = self.conv_tbl[sample[HA_ID].lower()]
        if '_pos' in internal_name.lower():
            sample[CONTROL_STATUS] = POSITIVE_CONTROL
        elif '_neg' in internal_name.lower():
            sample[CONTROL_STATUS] = NEGATIVE_CONTROL

        sample[PLATE_NUM] = pos[0]
        sample[PLATE_POS] = pos[1]
        for k, v in self.mdata_tbl[internal_name]:
            sample[k] = v


class PosToBC:
    '''Return a table mapping position to a barcode.

    This function returns a map from tuples of the form
    (plate-name, plate-position) to barcodes.
    '''
    def __init__(self):
        self.pos_to_bc = {
            (tkns[2], tkns[3]): tkns[4]
            for tkns in parse_csv(join(METADATA_DIR, 'CSD2017_DAVID.csv'))
        }
        assert len(self.pos_to_bc) > 0

    def map(self, sample):
        bc = getOrNone(
            self.pos_to_bc,
            (sample[PLATE_NUM], sample[PLATE_POS])
        )
        if bc:
            sample[BC] = bc


class GuessProjFromMSUBName:
    """Use the MetaSUB name to guess the project."""

    def map(self, sample):
        if not sample[METASUB_NAME]:
            return
        codes = {
            'oly': OLYMPIOME_CODE,
            'csd16': CSD16_CODE,
            'porto': CSD16_CODE,
        }
        for key, code in codes.items():
            if code in sample[METASUB_NAME].lower():
                sample[PROJECT] = code

        if len(sample[METASUB_NAME].split('_')) == 3:
            sample[PROJECT] = CSD16_CODE
            return


class SampleType:

    def __init__(self):
        self.stype_map = {}
        parsed = parse_csv(
            join(METADATA_DIR, 'sample_names_types.tsv'),
            assert_len=2,
            sep='\t'
        )
        for tkns in parsed:
            name = tkns[0].lower()
            stype = tkns[1]
            if name and stype:
                self.stype_map[name] = stype

    def map(self, sample):
        if sample[HA_ID] and sample[HA_ID].lower() in self.stype_map:
            sample[SAMPLE_TYPE] = self.stype_map[sample[HA_ID].lower()]
        elif sample[METASUB_NAME] and sample[METASUB_NAME].lower() in self.stype_map:
            sample[SAMPLE_TYPE] = self.stype_map[sample[METASUB_NAME].lower()]
        elif sample[SL_NAME] and  sample[SL_NAME].lower() in self.stype_map:
            sample[SAMPLE_TYPE] = self.stype_map[sample[SL_NAME].lower()]


MAPPERS = [
    sl_name_to_ha_name,
    ha_name_to_pos,
    airsample_sl_to_ha,
    airsample_ha_to_msub,
    PosToBC(),
    bc_to_meta,
    MSubToCity(),
    CityCodeToCity(),
    Handle5106HANames(),
    GuessProjFromMSUBName(),
    csd16_metadata,
    akl_metadata_csd16,
    fairbanks_metadata_csd16,
    SampleType(),
    tigress_metadata,
]
