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
        if not sample.ha_name:
            return
        sample.pos = getOrNone(self.ha_names_to_pos, sample.ha_name.lower())


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
        sample.bc = getOrNone(self.pos_to_bc, sample.pos)


class BCToMetadata:
    '''Return a table mapping barcodes to a list of metadata values.'''

    def __init__(self):
        self.bc_to_meta = {}
        for tkns in parse_csv(CLEAN_KOBO_METADATA_CSD17_FILE):
            try:
                bc = tkns[1]
                mdata = [tkns[0]] + tkns[2:]
                mdata = {
                    'city': mdata[0],
                    'surface_material': mdata[1],
                    'surface': mdata[2],
                    'setting': mdata[3],
                    'elevation': mdata[4],
                    'traffic': mdata[5],
                    'latitude': mdata[6],
                    'longitude': mdata[7],
                }
                self.bc_to_meta[bc] = mdata
            except IndexError:
                pass
        assert len(self.bc_to_meta) > 0

    def map(self, sample):
        vals = getOrNone(self.bc_to_meta, sample.bc)
        if vals:
            for key, val in vals.items():
                sample.metadata[key] = val


class MSubToCity:
    """Guess the city or city code from the MetaSUB name."""

    def map(self, sample):
        if not sample.msub_name:
            return

        if 'oly' in sample.msub_name.lower():
            sample.metadata['city'] = 'rio_de_janeiro'
            return
        if 'porto' in sample.msub_name.lower():
            sample.metadata['city'] = 'porto'
            return
        if 'csd16' in sample.msub_name.lower():
            tkns = sample.msub_name.split('-')
            if len(tkns) == 3:
                sample.metadata['city_code'] = tkns[1]
            return

        tkns = sample.msub_name.split('_')
        if len(tkns) == 3:
            sample.metadata['city'] = 'berlin'


class SLNameToHAName:
    """Convert an SL Name to an HA ID."""

    def __init__(self):
        self.tbl = {
            tkns[2]: tkns[3]
            for tkns in parse_csv(SL_NAME_TO_HA_ID_FILE, sep='\t')
        }

    def map(self, sample):
        if not sample.sl_name:
            return
        if sample.sl_name.lower() in self.tbl:
            sample.ha_name = self.tbl[sample.sl_name.lower()]
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
                ('city', 'london'),
                ('setting', tkns[31]),
                ('project', 'CSD17'),
                ('latitude', tkns[26]),
                ('longitude', tkns[27]),
                ('surface_material', tkns[37]),
                ('surface', tkns[33]),
                ('elevation', tkns[32]),
            ]
            for tkns in parse_csv(LONDON_METADATA_FILE)
        }

    def map(self, sample):
        if not sample.ha_name:
            return
        if sample.ha_name.lower() not in self.conv_tbl:
            if '5106-cem' in sample.ha_name.lower():
                sample.metadata['city'] = 'new_york_city'
                sample.metadata['project'] = PATHOMAP_WINTER_CODE
            return

        internal_name, pos = self.conv_tbl[sample.ha_name.lower()]
        sample.pos = pos
        for k, v in self.mdata_tbl[internal_name]:
            sample.metadata[k] = v


class GuessProjFromMSUBName:
    """Use the MetaSUB name to guess the project."""

    def map(self, sample):
        if sample.msub_name:
            if 'oly' in sample.msub_name.lower():
                sample.metadata['project'] = OLYMPIOME_CODE
                return
            if 'csd16' in sample.msub_name.lower():
                sample.metadata['project'] = CSD16_CODE
                return
            if 'porto' in sample.msub_name.lower():
                sample.metadata['project'] = CSD16_CODE
                return
            tkns = sample.msub_name.split('_')
            if len(tkns) == 3:
                sample.metadata['project'] = CSD16_CODE
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

