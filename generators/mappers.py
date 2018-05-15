from .parsing import parse_csv
from .constants import *
from .utils import getOrNone


class HANameToPos:
    '''Return a table mapping sample name to positions.

    Ideally this function returns a table mapping a sample name
    to a tuple of (plate-name, plate-position).

    In practice some of this information is missing, typically plate
    position.

    The original source of this information is from H.A. submission
    PDFs.
    '''
    def __init__(self):
        self.ha_names_to_pos = {
            tkns[0]: (tkns[8], tkns[14])
            for tkns in parse_csv(HA_IDS_TO_PLATE_POS_FILE, assert_len=15)
            if len(tkns[14]) == 3
        }
        assert len(self.ha_names_to_pos) > 0

    def map(self, sample):
        if not sample[HA_ID]:
            return
        plate_pos = getOrNone(self.ha_names_to_pos, sample[HA_ID].lower())
        if plate_pos:
            sample[PLATE_NUM] = plate_pos[0]
            sample[PLATE_POS] = plate_pos[1]


class PosToBC:
    '''Return a table mapping position to a barcode.

    This function returns a map from tuples of the form
    (plate-name, plate-position) to barcodes.
    '''
    def __init__(self):
        self.pos_to_bc = {
            (tkns[2], tkns[3]): tkns[4]
            for tkns in parse_csv(PLATE_POS_TO_BC_FILE)
        }
        assert len(self.pos_to_bc) > 0

    def map(self, sample):
        sample[BC] = getOrNone(
            self.pos_to_bc,
            (sample[PLATE_NUM], sample[PLATE_POS])
        )


class BCToMetadata:
    '''Return a table mapping barcodes to a list of metadata values.'''

    def __init__(self):
        self.bc_to_meta = {}
        for tkns in parse_csv(CLEAN_KOBO_METADATA_CSD17_FILE):
            try:
                bc = tkns[1]
                mdata = [tkns[0]] + tkns[2:]
                mdata = {
                    CITY: mdata[0],
                    SURFACE_MATERIAL: mdata[1],
                    SURFACE: mdata[2],
                    SETTING: mdata[3],
                    ELEVATION: mdata[4],
                    TRAFFIC_LEVEL: mdata[5],
                    LAT: mdata[6],
                    LON: mdata[7],
                }
                self.bc_to_meta[bc] = mdata
            except IndexError:
                pass
        assert len(self.bc_to_meta) > 0

    def map(self, sample):
        vals = getOrNone(self.bc_to_meta, sample[BC])
        if vals:
            for key, val in vals.items():
                sample[key] = val


class MSubToCity:
    """Guess the city or city code from the MetaSUB name."""

    def map(self, sample):
        if not sample[METASUB_NAME]:
            return

        if 'oly' in sample[METASUB_NAME].lower():
            sample[CITY] = 'rio_de_janeiro'
            return
        if 'porto' in sample[METASUB_NAME].lower():
            sample[CITY] = 'porto'
            return
        if 'csd16' in sample[METASUB_NAME].lower():
            tkns = sample[METASUB_NAME].split('-')
            if len(tkns) == 3:
                sample[CITY_CODE] = tkns[1]
            return

        tkns = sample[METASUB_NAME].split('_')
        if len(tkns) == 3:
            sample[CITY] = 'berlin'


class SLNameToHAName:
    """Convert an SL Name to an HA ID."""

    def __init__(self):
        self.tbl = {
            tkns[2]: tkns[3]
            for tkns in parse_csv(SL_NAME_TO_HA_ID_FILE, sep='\t')
        }

    def map(self, sample):
        if not sample[SL_NAME]:
            return
        if sample[SL_NAME].lower() in self.tbl:
            sample[HA_ID] = self.tbl[sample[SL_NAME].lower()]
            return


class Handle5106HANames:
    """HA IDs matching 5106-CEM come from either London gCSD17
    or NYC winter pathomap.
    """

    def __init__(self):
        self.conv_tbl = {
            tkns[5]: (tkns[0], (tkns[1], tkns[2]))
            for tkns in parse_csv(CONVERT_LONDON_IDS_FILE)
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
            for tkns in parse_csv(LONDON_METADATA_FILE)
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
        sample[PLATE_NUM] = pos[0]
        sample[PLATE_POS] = pos[1]
        for k, v in self.mdata_tbl[internal_name]:
            sample[k] = v


class GuessProjFromMSUBName:
    """Use the MetaSUB name to guess the project."""

    def map(self, sample):
        if sample[METASUB_NAME]:
            if 'oly' in sample[METASUB_NAME].lower():
                sample[PROJECT] = OLYMPIOME_CODE
                return
            if 'csd16' in sample[METASUB_NAME].lower():
                sample[PROJECT] = CSD16_CODE
                return
            if 'porto' in sample[METASUB_NAME].lower():
                sample[PROJECT] = CSD16_CODE
                return
            tkns = sample[METASUB_NAME].split('_')
            if len(tkns) == 3:
                sample[PROJECT] = CSD16_CODE
                return


MAPPERS = [
    SLNameToHAName(),
    HANameToPos(),
    PosToBC(),
    BCToMetadata(),
    MSubToCity(),
    Handle5106HANames(),
    GuessProjFromMSUBName()
]
