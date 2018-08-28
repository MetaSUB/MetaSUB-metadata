"""Constants used while generating metadata tables."""

from os.path import dirname, join
from .parsing import parse_csv


METADATA_DIR = join(dirname(dirname(__file__)), 'spreadsheets')

CITY_NAMES_FILE = join(METADATA_DIR, 'city_names.csv')
CITY_NAMES = set([
    tkns[0].lower()
    for tkns in parse_csv(CITY_NAMES_FILE, assert_len=2, skip=1)
])


SAMPLE_NAMES_FILE = join(METADATA_DIR, 'new_sample_names.txt')

CSD16_CODE = 'CSD16'
CSD17_CODE = 'CSD17'
OLYMPIOME_CODE = 'OLY'
PATHOMAP_WINTER_CODE = 'PATHOMAP_WINTER'

NA_TOKEN = 'n/a'

PLATE_NUM = 'plate_number'
PLATE_POS = 'plate_pos'
BC = 'barcode'
CITY = 'city'
CITY_CODE = 'city_code'
SURFACE_MATERIAL = 'surface_material'
SURFACE = 'surface'
SETTING = 'setting'
ELEVATION = 'elevation'
TRAFFIC_LEVEL = 'traffic'
LAT = 'latitude'
LON = 'longitude'
METASUB_NAME = 'metasub_name'
HAUID = 'hudson_alpha_uid'
HA_PROJ = 'hudson_alpha_project'
HA_FLOWCELL = 'hudson_alpha_flowcell'
HA_ID = 'ha_id'
SL_NAME = 'sl_name'
PROJECT = 'project'
SAMPLE_TYPE = 'sample_type'
LOCATION_TYPE = 'location_type'
IDS = set([HAUID, HA_ID, BC, METASUB_NAME, SL_NAME])
CONTROL_STATUS = 'control_type'
STATION = 'station'
LINE = 'line'

POSITIVE_CONTROL = 'positive_control'
NEGATIVE_CONTROL = 'negative_control'
