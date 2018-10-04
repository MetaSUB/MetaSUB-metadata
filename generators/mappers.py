from .parsing import parse_csv
from .constants import *
from .utils import getOrNone, remove_leading_char, remove_trailing_char
from .table_mapper import (
    Table,
    token_mapper,
    token_specific_val_func,
    ha_filename_table
)
from sys import stderr


def mdata_dir(fname):
    return join(METADATA_DIR, fname)


ha_filename_tables = [
    ('filenames_HCY5HCCXY.tsv', {}),
    ('filenames_HMC2KCCXY.tsv', {'description_key': BC}),
    ('filenames_HMCMJCCXY.tsv', {'description_key': BC, 'strict': False}),
    ('air_samples.filenames_HK7G5CCXY.txt', {}),


    ('haib17CEM4890_filenames_H2NYMCCXY.txt', {'description_key': METASUB_NAME}),
    ('haib17CEM4890_filenames_H3KHWCCXY.txt', {'description_key': METASUB_NAME}),
    ('haib17CEM4890_filenames_H75CGCCXY.txt', {'description_key': METASUB_NAME}),
    ('haib17CEM4890_filenames_H7KYMCCXY.txt', {'description_key': METASUB_NAME}),
    ('haib17CEM4890_filenames_HKC32ALXX.txt', {'description_key': METASUB_NAME}),
    ('haib17CEM4890_filenames_HMCMJCCXY.txt', {'description_key': METASUB_NAME}),

    ('haib17CEM5080_filenames_H7VL7CCXY.txt', {}),

    ('haib17CEM5106_filenames_HCCGHCCXY.txt', {}),
    ('haib17CEM5106_filenames_HCV72CCXY.txt', {}),
    ('haib17CEM5106_filenames_HCVMTCCXY.txt', {}),
    ('haib17CEM5106_filenames_HCY5HCCXY.txt', {}),
    ('haib17CEM5106_filenames_HCY5JCCXY.txt', {}),

    ('haib17CEM5241_filenames_HMCMJCCXY.txt', {}),
    ('haib17CEM5241_filenames_HMGTJCCXY.txt', {
        'description_key': BC,
        'token_val_funcs': {BC: lambda x: x.split('_')[-1]}
    }),  # kyiv, ukraine_2_235114675
    ('haib17CEM5241_filenames_HMGW3CCXY.txt', {
        'description_key': BC,
        'token_val_funcs': {BC: lambda x: x.split('_')[-1]}
    }),  # kyiv, ukraine_2_235114675
    ('haib17CEM5241_filenames_HMGMHCCXY.txt', {
        'description_key': BC,
        'token_val_funcs': {BC: lambda x: x.split('_')[-1]}
    }),  # kyiv, ukraine_2_235114672

    ('haib17DB4959_filenames_H3MGVCCXY.txt', {}),
    ('haib17DB4959_filenames_HMCMJCCXY.txt', {}),
    ('haib17DB4959_filenames_HMGTJCCXY.txt', {}),  # Inbound5_B_2
    ('haib17DB4959_filenames_HMGW3CCXY.txt', {}),  # Inbound2_A_7

    ('haib17KIU4866_filenames_H7HJMCCXY.txt', {}),  # standard DNA prep with sequencing on the X
    ('haib17KIU4866_filenames_HMCMJCCXY.txt', {}),  # standard DNA prep with sequencing on the X

    ('haib18CEM5332_filenames_HK7G5CCXY.txt', {'description_key': METASUB_NAME}),  # gCSD17-HKG-AS1
    ('haib18CEM5332_filenames_HMCMJCCXY.txt', {'description_key': METASUB_NAME}),  # gCSD17-OSL-AS17
    ('haib18CEM5332_filenames_HMGTJCCXY.txt', {'description_key': METASUB_NAME}),  # gCSD17-NYC-AS01
    ('haib18CEM5332_filenames_HMGW3CCXY.txt', {'description_key': METASUB_NAME}),  # gCSD17-NYC-AS01

    ('haib18CEM5453_filenames_HMC2KCCXY.txt', {'description_key': BC}),  # 0235023170
    ('haib18CEM5453_filenames_HMCMJCCXY.txt', {}),
    ('haib18CEM5453_filenames_HMGTJCCXY.txt', {'description_key': BC}),  # 235185269
    ('haib18CEM5453_filenames_HMGW3CCXY.txt', {'description_key': BC}),  # 0235075616
    ('haib18CEM5453_filenames_HNGH3CCXY.txt', {'description_key': BC}),  
    ('haib18CEM5453_filenames_HMGN5CCXY.txt', {'description_key': BC}),
    ('haib18CEM5453_filenames_HNHKFCCXY.txt', {'description_key': BC}),          

    ('haib18CEM5526_filenames_HMGTJCCXY.txt', {'description_key': BC}),  # 232023295
    ('haib18CEM5526_filenames_HMGW3CCXY.txt', {'description_key': BC}),  # 232023295
    ('haib18CEM5526_filenames_HMGMHCCXY.txt', {'description_key': BC}),  # 235040613
]
ha_filename_tables = [
    ha_filename_table(
        mdata_dir(filename),
        **kwargs
    )
    for filename, kwargs in ha_filename_tables
]


haid_to_barcode_4959DB = Table(
    mdata_dir('4959DB_barcodes.csv'),
    {HA_ID: 0, BC: 1},
    token_mapper(BC),
    name_func=lambda x, y: remove_trailing_char('R')(x.lower()),
    skip=1,
)


def normalize_plate_num(raw):
    raw = raw.lower()
    if 'zymo plate' in raw:
        plate_num = raw.split()[2]
        while len(plate_num) < 4:
            plate_num = '0' + plate_num
        return f'plate_{plate_num}'
    return raw

ha_name_to_pos = Table(
    mdata_dir('HA Submissions-Grid view.csv'),
    {HA_ID: 0, PLATE_NUM: 8, PLATE_POS: 14},
    token_mapper(PLATE_NUM, PLATE_POS),
    val_func=token_specific_val_func(**{PLATE_NUM: normalize_plate_num}),
    assert_len=15
)


def airsample_ha_to_msub_mapper(sample, sample_id, vec):
    sample[METASUB_NAME] = vec[METASUB_NAME]
    sample[PROJECT] = CSD17_CODE


airsample_ha_to_msub = Table(
    mdata_dir('airsamples_ha_id_to_msub_name.csv'),
    {HA_ID: 1, METASUB_NAME: 4},
    airsample_ha_to_msub_mapper,
    val_func=token_specific_val_func(**{METASUB_NAME: lambda x: x[1:]}),
    assert_len=5,
    skip=1

)

olympiome_metadata = Table(
    mdata_dir('samples_oly_meta_all_information_e.csv'),
    {
        METASUB_NAME: 0,
        PROJECT: 5,
        STATION: 6,
        LAT: 7,
        LON: 8,
        SURFACE: 9,
    },
    token_mapper(PROJECT, STATION, LAT, LON, SURFACE),
    name_func=lambda x, y: x.upper()
)


bc_to_meta = Table(
    mdata_dir('cleaned_simplified_metadata.csv'),
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
        STATION: 10,
        LINE: 11,
    },
    token_mapper(
        CITY, SURFACE_MATERIAL, SURFACE, SETTING,
        ELEVATION, TRAFFIC_LEVEL, LAT, LON, METASUB_NAME,
        STATION, LINE, strict=False
    ),
    name_func=token_specific_val_func(**{METASUB_NAME: remove_leading_char('g')}),
    val_func=token_specific_val_func(**{METASUB_NAME: remove_leading_char('g')}),
)


def csd16_metadata_name_func(name, name_type):
    name = name.lower()
    name = '-'.join(name.split('_'))
    if 'csd2016' in name:
        name = 'csd16'.join(name.split('csd2016'))
    return name


csd16_metadata = Table(
    mdata_dir('collated_metadata_csd16.csv'),
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
    mdata_dir('auckland_csd16.csv'),
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
    mdata_dir('Fairbanks_corralled_CSD16.csv'),
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


oslo_air_metadata_csd16 = Table(
    mdata_dir('oslo_air_sample_metadata.csv'),
    {
        METASUB_NAME: 0,
        CITY: 1,
        STATION: 3,
        LAT: 4,
        LON: 5,
        LINE: 6,
        ELEVATION: 8,
        SETTING: 9,
        TRAFFIC_LEVEL: 10,
    },
    token_mapper(
        METASUB_NAME,
        CITY,
        STATION,
        LAT,
        LON,
        LINE,
        ELEVATION,
        SETTING,
        TRAFFIC_LEVEL,
    ),
    name_func=token_specific_val_func(**{METASUB_NAME: remove_leading_char('g')}),
    val_func=token_specific_val_func(**{METASUB_NAME: remove_leading_char('g')}),
    skip=1
)

tigress_metadata = Table(
    mdata_dir('metadata.MetaSUB_UK2017.csv'),
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


tokyo_metadata = Table(
    mdata_dir('Tokyo_MetaSUB_2016_SA_HS_NM_.csv'),
    {
        METASUB_NAME: 0,
        LAT: 8,
        LON: 9,
        SURFACE_MATERIAL: 11,
        TEMPERATURE: 12,
    },
    token_mapper(
        METASUB_NAME, LAT, LON, SURFACE_MATERIAL, TEMPERATURE
    )
)


boston_metadata = Table(
    mdata_dir('Boston_MetaSUB_2016_SA_TH_BGY_TH.csv'),
    {
        METASUB_NAME: 0,
        LINE: 9,
        LAT: 11,
        LON: 12,
        SURFACE_MATERIAL: 14,
        TEMPERATURE: 15,
    },
    token_mapper(
        METASUB_NAME, LINE, LAT, LON, SURFACE_MATERIAL, TEMPERATURE
    )
)


zurich_metadata = Table(
    mdata_dir('Zurich_MetaSUB_2016_SA.csv'),
    {
        METASUB_NAME: 0,
        LINE: 7,
        LAT: 10,
        LON: 11,
        SURFACE_MATERIAL: 13,
        TEMPERATURE: 14,
    },
    token_mapper(
        METASUB_NAME, LINE, LAT, LON, SURFACE_MATERIAL, TEMPERATURE
    )
)


csd16_metadata_bgy = Table(
    mdata_dir('MASTER_MetaSUB_Metadata_BGY_csd16.csv'),
    {
        METASUB_NAME: 0,
        LINE: 8,
        LAT: 10,
        LON: 11,
        SURFACE: 12,
        SURFACE_MATERIAL: 13,
        TEMPERATURE: 14,
    },
    token_mapper(
        METASUB_NAME, LINE, LAT, LON, SURFACE_MATERIAL, TEMPERATURE
    )
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
            if 'csd_denver' in sample[METASUB_NAME].lower():
                sample[CITY_CODE] = 'DEN'
                return
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
            'KL':  'kuala_lumpur',
            'TPE': 'taipei',
            'SIN': 'singapore',
            'VIE': 'vienna',
            'DOH': 'doha',
            'MRS': 'marseille',
            'MSP': 'minneapolis',
            'BNE': 'brisbane',
            'SEL': 'seoul',
        }
        city_map = {v: k for k, v in code_map.items()}
        if sample[CITY_CODE]:  #and not sample[CITY]:
            try:
                sample[CITY] = code_map[sample[CITY_CODE].strip().upper()]
            except KeyError:
                if sample[CITY_CODE].lower() != 'csd':
                    raise
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
                mdata_dir('Conversion Tables-Table 1.csv')
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
                (SURFACE, tkns[33]),
                (ELEVATION, tkns[32]),
            ]
            for tkns in parse_csv(mdata_dir('Metadata-Table 1.csv'))
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
            for tkns in parse_csv(mdata_dir('CSD2017_DAVID.csv'))
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
            mdata_dir('sample_names_types.tsv'),
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


class HAUIDSplitter:

    def map(self, sample):
        if not sample[HAUID]:
            return
        ha_proj, ha_flowcell, sl_name = sample[HAUID].split('_')
        sample[HA_PROJ] = ha_proj
        sample[HA_FLOWCELL] = ha_flowcell
        sample[SL_NAME] = sl_name


MAPPERS = [
    HAUIDSplitter(),
    #ha_name_to_pos,
    haid_to_barcode_4959DB,
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
    oslo_air_metadata_csd16,
    olympiome_metadata,
    SampleType(),
    tigress_metadata,
    boston_metadata,
    tokyo_metadata,
    zurich_metadata,
    csd16_metadata_bgy,
] + ha_filename_tables
