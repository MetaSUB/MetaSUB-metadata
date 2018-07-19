import click

'''
This script generates a clean version of the metadata table produced
by Alina F. (named gCSD2017_metadata_joint-1.txt on my system).

It produces only a limited number of output fields, this is intended to be
conservative.

Typically I name the output of this script cleaned_simplified_metadata.csv
'''

NA_TOKEN = ''

CITY_COl = 8
LAT_COL = 19
LONG_COL = 20
MATERIAL_COL = 30  # AE
TRAFFIC_COL = 38  # AM
STATION_COL = 16  # Q
LINE_COL = 17  # R
SAMPLING_PLACE_COL = 26  # AA
SAMPLE_NAME_COL = 23  # X
SETTING_COL = 24  # Y
GROUND_LEVEL_COL = 25  # Z
BC_COL = 46
NAME_TABLE_FILE = '/Users/dcdanko/Dev/metasub-scripts/city_names.csv'


city_name_table = None


def parse_name_table_file():
    table_file_name = NAME_TABLE_FILE
    with open(table_file_name) as tf:
        tf.readline()
        city_name_table = {}
        for line in tf:
            tkns = line.strip().split(',')
            if len(tkns) == 2:
                city_name, country_name = tkns[0], tkns[1]
                try:
                    city_name_table[city_name].add(country_name)
                except KeyError:
                    city_name_table[city_name] = set()
                    city_name_table[city_name].add(country_name)

    return city_name_table


def parse_name_table():
    global city_name_table
    if city_name_table is not None:  # this is a dirty hack, forgive me
        return city_name_table
    city_name_table = parse_name_table_file()
    return city_name_table


def bc_search(tkns, col):
    try:
        maybe_bc = tkns[col]
    except IndexError:
        return None
    try:
        int(maybe_bc)
    except ValueError:
        return bc_search(tkns, col + 1)
    while len(maybe_bc) < 9:
        maybe_bc = '0' + maybe_bc
    return maybe_bc


city_map = {
    'bogot\xe1': 'bogota',
    'hong kong': 'hong_kong',
    'its': 'ilorin',
    'kuala lumpur': 'kuala_lumpur',
    'nyc': 'new_york_city',
    'ribeir\xe3o preto': 'Ribeirao_Preto',
    'rio de janeiro': 'rio_de_janeiro',
    '"saint louis, mo"': 'St_Louis',
    'san francisco': 'san_francisco',
    'sao paulo': 'sao_paulo',
}

null_cities = set([
    'n/a'
])


def sample_name_search(tkns):
    try:
        sname = tkns[SAMPLE_NAME_COL]
        if 'CSD' in sname.upper() and len(sname.split('-')) == 3:
            return sname
    except IndexError:
        pass
    return NA_TOKEN


def uppercase_city(city):
    wrds = city.split('_')
    wrds = [wrd[0].upper() + wrd[1:] for wrd in wrds]
    return '_'.join(wrds)


def city_search(tkns):
    try:
        city = tkns[CITY_COl].lower().strip()
        if city in city_map:
            city = city_map[city].lower()
        if city in null_cities:
            return None
    except IndexError:
        return None
    city_tbl = parse_name_table()
    city = uppercase_city(city)
    assert city in city_tbl, city + ' \n ' + str(tkns)
    return city


def generic_search(tkns, col):
    try:
        return tkns[col]
    except KeyError:
        return NA_TOKEN
    except IndexError:
        return NA_TOKEN


def latlong_search(tkns):
    try:
        lat = tkns[LAT_COL]
        lon = tkns[LONG_COL]
        return lat, lon
    except KeyError:
        return NA_TOKEN, NA_TOKEN
    except IndexError:
        return NA_TOKEN, NA_TOKEN


def clean_token(tkn):
    if tkn is None:
        tkn = NA_TOKEN
    tkn = tkn.lower().strip()
    if tkn in ['n/a', 'na']:
        tkn = NA_TOKEN
    return tkn


def handle_tkns(tkns):
    bc = bc_search(tkns, BC_COL)
    city = city_search(tkns)
    lat, lon = latlong_search(tkns)
    sample_name = sample_name_search(tkns)

    tkn_list = [
        city,
        bc,
        generic_search(tkns, MATERIAL_COL),
        generic_search(tkns, SAMPLING_PLACE_COL),
        generic_search(tkns, SETTING_COL),
        generic_search(tkns, GROUND_LEVEL_COL),
        generic_search(tkns, TRAFFIC_COL),
        lat,
        lon,
        sample_name,
        generic_search(tkns, STATION_COL),
        generic_search(tkns, LINE_COL),
    ]
    if (bc and city) or (sample_name != NA_TOKEN):
        tkn_list = [clean_token(tkn) for tkn in tkn_list]
        msg = '{},' * len(tkn_list)
        msg = msg[:-1]
        print(msg.format(*tkn_list))


@click.command()
@click.argument('tbl')
def main(tbl):
    with open(tbl, encoding='latin-1') as t:
        t.readline()  # header
        for line in t:
            tkns = line.strip().split('\t')
            if len(tkns) < 2:
                continue
            handle_tkns(tkns)


if __name__ == '__main__':
    main()
