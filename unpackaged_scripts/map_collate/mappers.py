from parsing import parse_csv

MDATA_ROOT = '/Users/dcdanko/Dropbox/Projects/MetaSUB/initial_analysis/metadata/'
DESC_NAMES_FILE = MDATA_ROOT + 'ha_to_msub_name_conversion_for_project_haib17CEM4890_samples_from_csd16.csv'


def getOrNone(tbl, key, default=None):
    if key is None:
        return default
    try:
        return tbl[key]
    except KeyError:
        return default


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
        sname_to_pos_file = MDATA_ROOT + 'HA Submissions-Grid view.csv'
        self.ha_names_to_pos = {
            tkns[0]: (tkns[8], tkns[14])
            for tkns in parse_csv(sname_to_pos_file, assert_len=15)
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
        pos_to_bc_file = MDATA_ROOT + 'CSD2017_DAVID.csv'
        self.pos_to_bc = {
            (tkns[2], tkns[3]): tkns[4]
            for tkns in parse_csv(pos_to_bc_file)
        }
        assert len(self.pos_to_bc) > 0

    def map(self, sample):
        sample.bc = getOrNone(self.pos_to_bc, sample.pos)


class BCToMetadata:
    '''Return a table mapping barcodes to a list of metadata values.'''

    def __init__(self):
        self.bc_to_meta = {}
        for tkns in parse_csv(MDATA_ROOT + 'cleaned_simplified_metadata.csv'):
            try:
                bc = tkns[1]
                mdata = [tkns[0]] + tkns[2:]
                # baltimore,235161834,other,handrail,urban,under_ground,,39.289523,-76.613904
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

    def map(self, sample):
        if not sample.msub_name:
            return

        if 'oly' in sample.msub_name.lower():
            sample.metadata['city'] = 'RIO'
            return
        if 'porto' in sample.msub_name.lower():
            sample.metadata['city'] = 'Porto'
            return
        if 'csd16' in sample.msub_name.lower():
            tkns = sample.msub_name.split('-')
            if len(tkns) == 3:
                sample.metadata['city'] = tkns[1]
            return

        tkns = sample.msub_name.split('_')
        if len(tkns) == 3:
            sample.metadata['city'] = 'Berlin'


class SLNameToHAName:

    def __init__(self):
        self.tbl = {
            tkns[2]: tkns[3]
            for tkns in parse_csv(MDATA_ROOT + 'filenames_HCY5HCCXY.tsv', sep='\t')
        }

    def map(self, sample):
        if not sample.sl_name:
            return
        if sample.sl_name.lower() in self.tbl:
            sample.ha_name = self.tbl[sample.sl_name.lower()]
            return


class Handle5106HANames:

    def __init__(self):
        self.conv_tbl = {
            tkns[5]: (tkns[0], (tkns[1], tkns[2]))
            for tkns in parse_csv(MDATA_ROOT + 'PN1_GCSD17/Conversion Tables-Table 1.csv')
        }

        self.mdata_tbl = {
            tkns[0]: [
                ('city', 'London'),
                ('setting', tkns[31]),
                ('project', 'CSD17'),
                ('latitude', tkns[26]),
                ('longitude', tkns[27]),
                ('surface_material', tkns[37]),
                ('surface', tkns[33]),
                ('elevation', tkns[32]),
            ]
            for tkns in parse_csv(MDATA_ROOT + 'PN1_GCSD17/Metadata-Table 1.csv')
        }

    def map(self, sample):
        if not sample.ha_name:
            return
        if sample.ha_name.lower() not in self.conv_tbl:
            if '5106-cem' in sample.ha_name.lower():
                sample.metadata['city'] = 'NYC'
                sample.metadata['project'] = 'winter-sampling'
            return

        internal_name, pos = self.conv_tbl[sample.ha_name.lower()]
        sample.pos = pos
        for k, v in self.mdata_tbl[internal_name]:
            sample.metadata[k] = v




class GuessProj:

    def map(self, sample):
        if sample.msub_name:
            if 'oly' in sample.msub_name.lower():
                sample.metadata['project'] = 'OLY'
                return
            if 'csd16' in sample.msub_name.lower():
                sample.metadata['project'] = 'CSD16'
                return
            if 'porto' in sample.msub_name.lower():
                sample.metadata['project'] = 'CSD16'
                return
            tkns = sample.msub_name.split('_')
            if len(tkns) == 3:
                sample.metadata['project'] = 'CSD16'
                return






