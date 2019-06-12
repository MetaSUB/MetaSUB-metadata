from .parsing import parse_csv
from .constants import *
from .utils import (
    getOrNone,
    clean_ha_id,
    mdata_dir,
)
from .ha_filename_tables import HA_FILENAME_TABLES
from .simple_tables import SIMPLE_TABLES
from sys import stderr
import pandas as pd


class CityMetadataMapper:

    def __init__(self):
        self.tbl = pd.read_csv(mdata_dir('city_metadata.csv'), index_col=0)

    def map(self, sample):
        if not sample[CITY]:
            return
        city_name = sample[CITY].lower()
        if city_name not in self.tbl.index:
            return

        sample[CITY_LAT] = self.tbl['latitude'][city_name]
        sample[CITY_LON] = self.tbl['longitude'][city_name]
        sample[CITY_COASTAL] = self.tbl['coastal'][city_name]
        sample[CITY_POP] = self.tbl['total_population'][city_name]
        sample[CITY_DENSITY] = self.tbl['population_density_km2'][city_name]
        sample[CITY_AREA] = self.tbl['land_area_km2'][city_name]
        sample[CITY_TEMP] = self.tbl['ave_june_temp_celsius'][city_name]
        sample[CITY_ELEV] = self.tbl['elevation_meters'][city_name]
        sample[CITY_CONTINENT] = self.tbl['continent'][city_name]


class CoreProjMapper:

    def map(self, sample):
        if not sample[PROJECT]:
            return
        proj = sample[PROJECT]
        if proj in [CSD16_CODE, CSD17_CODE, PILOT_CODE]:
            if sample[CITY] != 'antarctica':
                sample[CORE_PROJECT] = 'core'
        else:
            sample[CORE_PROJECT] = 'not_core'


class OtherProjToBarcelona:

    def map(self, sample):
        if not sample[OTHER_PROJ_UID]:
            return
        if 'sossowski' in sample[OTHER_PROJ_UID].lower():
            sample[CITY] = 'barcelona'
            if 'ms0' in  sample[OTHER_PROJ_UID].lower():
                sample[PROJECT] = PILOT_CODE


class ControlAsCity:

    def map(self, sample):
        if sample[CITY]:
            return
        if sample[CONTROL_STATUS]:
            sample[CITY] = 'other_control'
        elif sample[METASUB_NAME] and 'control' in sample[METASUB_NAME].lower():
            sample[CITY] = 'other_control'
        elif sample[HA_ID] and sample[HA_ID].upper() == '4959-DB_PC':
            sample[CITY] = 'other_control'
            sample[CONTROL_STATUS] = POSITIVE_CONTROL


class MapUUID:

    def map(self, sample):
        if sample[HAUID] and not sample[OTHER_PROJ_UID]:
            sample[GENERIC_UID] = sample[HAUID]
        elif sample[OTHER_PROJ_UID] and not sample[HAUID]:
            sample[GENERIC_UID] = sample[OTHER_PROJ_UID]


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
                sample[PROJECT] = CSD16_CODE
                return
            tkns = sample[METASUB_NAME].split('-')
            if len(tkns) == 3:
                sample[CITY_CODE] = tkns[1]
            return


        tkns = sample[METASUB_NAME].split('_')
        if 'INBOUNDCONTROL' not in sample[METASUB_NAME] and len(tkns) == 3:
            sample[CITY] = 'berlin'


class MetaSUBNameToProject:

    def map(self, sample):
        code_map = {
            'CSD-16': CSD16_CODE,
            'CSD16': CSD16_CODE,
            'CSD17': CSD17_CODE,
            'CSD-17': CSD17_CODE,
            'WINTER_NYC': PATHOMAP_WINTER_CODE,
        }
        if sample[METASUB_NAME]:
            for key, val in code_map.items():
                if key.lower() in sample[METASUB_NAME].lower():
                    sample[PROJECT] = val
                    break


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
            'LSB': 'lisbon',
            'MXC': 'mexico_city',
            'MVD': 'montevideo',
            'SHG': 'shanghai',
            'BCN': 'barcelona',
            'LIS': 'lisbon',
            'BOS': 'boston',
            'MEL': 'melbourne',
            'NAP': 'naples',
            'PAR': 'paris',
            'PXO': 'porto',
            'RAO': 'sao_paulo',
        }
        city_map = {v: k for k, v in code_map.items()}
        if sample[CITY_CODE]:  #and not sample[CITY]:
            try:
                sample[CITY] = code_map[sample[CITY_CODE].strip().upper()]
            except KeyError:
                if sample[CITY_CODE].lower() != 'csd':
                    pass #raise
        elif sample[CITY] and not sample[CITY_CODE]:
            try:
                sample[CITY_CODE] = city_map[sample[CITY]]
            except KeyError:
                pass


class Handle5106HANames:
    """HA IDs matching 5106-CEM come from either London gCSD17
    or NYC winter   ap.
    """

    def __init__(self):
        self.conv_tbl = {
            tkns[5]: (tkns[0], (tkns[1], tkns[2]))
            for tkns in parse_csv(
                mdata_dir('Conversion Tables-Table 1.csv')
            )
        }
        self.pathomap_winter_coversion = [
            tkns[0] for tkns in parse_csv(mdata_dir('winter_pathomap_conversion.csv'))
        ]

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
                snum = int(sample[HA_ID].split('-')[2])
                code = self.pathomap_winter_coversion[snum - 1]
                sample[METASUB_NAME] = code
                if code == 'pos':
                    sample[CONTROL_STATUS] = 'positive_control'
                elif code == 'neg':
                    sample[CONTROL_STATUS] = 'negative_control'
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


class OtherProjUidToMetaSubName:

    def map(self, sample):
        if not sample[OTHER_PROJ_UID]:
            return
        uid = sample[OTHER_PROJ_UID].lower()
        if 'csd16' in uid.lower():
            msub = 'csd16' + uid.split('csd16')[1].split('_')[0]
            msub = '-'.join(msub.split('-')[:3])
            sample[METASUB_NAME] = msub


class OtherProjUidToCity:

    def map(self, sample):
        if not sample[OTHER_PROJ_UID]:
            return
        uid = sample[OTHER_PROJ_UID].lower()
        if 'pilot' not in uid:
            return
        pilot_cities = [
            ('hong_kong', 'HKG'),
            ('lisbon', 'LSB'),
            ('mexico_city', 'MXC'),
            ('montevideo', 'MVD'),
            ('oslo', 'OSL'),
            ('sacramento', 'SAC'),
            ('seoul', 'SEL'),
            ('shanghai', 'SHG')
        ]
        for city_name, city_code in pilot_cities:
            city_name_viz = ''.join(city_name.split('_'))
            if city_name_viz in uid:
                sample[CITY] = city_name
                sample[CITY_CODE] = city_code
                break

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


class GuessProj:
    """Use the MetaSUB name to guess the project."""

    def map(self, sample):
        if sample[PROJECT]:
            return  # use this as a last resort
        if sample[OTHER_PROJ_UID] and 'pilot_' in sample[OTHER_PROJ_UID]:
            sample[PROJECT] = PILOT_CODE
            return
        if sample[METASUB_NAME] and 'porto_' in sample[METASUB_NAME].lower():
            sample[PROJECT] = PILOT_CODE
            return
        if sample[METASUB_NAME] and 'csd_denver' in sample[METASUB_NAME].lower():
            sample[PROJECT] = CSD16_CODE
            return
        if sample[HA_ID] and '5080-cem' in sample[HA_ID]:
            ha_num = int(sample[HA_ID].split('-')[2])
            if 1 <= ha_num <= 79:
                sample[PROJECT] = TIGRESS_CODE
                return
        if sample[BC]:
            sample[PROJECT] = CSD17_CODE
            return

class AirSamplingProj:
    """Use the MetaSUB name to guess the project."""

    def map(self, sample):
        msub = sample[METASUB_NAME]
        if msub and 'csd17' in msub.lower() and '-as' in msub.lower():
            sample[PROJECT] = CSD17_AIR_CODE

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


class HARemap:

    def map(self, sample):
        if sample[HA_ID]:
            sample[HA_ID] = clean_ha_id(sample[HA_ID])


class CleanCityName:

    def map(self, sample):
        if sample[CITY]:
            sample[CITY] = '_'.join(sample[CITY].lower().split())


MAPPERS = [
    CleanCityName(),
    OtherProjToBarcelona(),
    ControlAsCity(),
    CityMetadataMapper(),
    CoreProjMapper(),
    HARemap(),
    HAUIDSplitter(),
    PosToBC(),
    MSubToCity(),
    CityCodeToCity(),
    Handle5106HANames(),
    GuessProjFromMSUBName(),
    SampleType(),
    MetaSUBNameToProject(),
    OtherProjUidToMetaSubName(),
    OtherProjUidToCity(),
    GuessProj(),
    AirSamplingProj(),
    MapUUID(),
] + HA_FILENAME_TABLES + SIMPLE_TABLES
