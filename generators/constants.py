"""Constants used while generating metadata tables."""

from os.path import dirname, join
from .parsing import parse_csv


METADATA_DIR = join(dirname(dirname(__file__)), 'spreadsheets')

CITY_NAMES_FILE = join(METADATA_DIR, 'city_names.csv')
CITY_NAMES = set([
    tkns[0].lower()
    for tkns in parse_csv(CITY_NAMES_FILE, assert_len=2, skip=1)
])


SAMPLE_NAMES_FILE = join(METADATA_DIR, 'sample_names.txt')

CSD16_CODE = 'CSD16'
CSD17_CODE = 'CSD17'
CSD17_AIR_CODE = 'CSD17_AIR'
OLYMPIOME_CODE = 'OLY'
PATHOMAP_WINTER_CODE = 'PATHOMAP_WINTER'
TIGRESS_CODE = 'TIGRESS'
PILOT_CODE = 'PILOT'


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
MAYBE_METASUB_NAME = 'maybe_metasub_name'
METASUB_NAME = 'metasub_name'
HAUID = 'hudson_alpha_uid'
OTHER_PROJ_UID = 'other_project_uid'
GENERIC_UID = 'uuid'
HA_PROJ = 'hudson_alpha_project'
HA_FLOWCELL = 'hudson_alpha_flowcell'
HA_ID = 'ha_id'
SL_NAME = 'sl_name'
PROJECT = 'project'
SAMPLE_TYPE = 'sample_type'
LOCATION_TYPE = 'location_type'
IDS = set([HAUID, HA_ID, BC, METASUB_NAME, SL_NAME, OTHER_PROJ_UID])
CONTROL_STATUS = 'control_type'
STATION = 'station'
LINE = 'line'
INDEX_SEQ = 'index_sequence'
TEMPERATURE = 'temperature'
CORE_PROJECT = 'core_project'

POSITIVE_CONTROL = 'positive_control'
NEGATIVE_CONTROL = 'negative_control'

READ_COUNTS = 'num_reads'

CITY_LAT = 'city_latitude'
CITY_LON = 'city_longitude'
CITY_COASTAL = 'coastal_city'
CITY_POP = 'city_total_population'
CITY_DENSITY = 'city_population_density'
CITY_AREA = 'city_land_area_km2'
CITY_TEMP = 'city_ave_june_temp_c'
CITY_ELEV = 'city_elevation_meters'
CITY_CONTINENT = 'continent'
