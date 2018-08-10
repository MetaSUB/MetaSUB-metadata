
from json import loads, dumps
import click
from sys import stdout, stdin, stderr
import pandas as pd
from os import makedirs, path

from .mappers import MAPPERS
from .sample import Sample
from .constants import *


@click.group()
def main():
    pass


@main.command(name='best-effort')
@click.option('--csv/--json', default=True)
@click.option('-s', '--sample-names', default=None)
def best_effort(csv, sample_names):
    """Generate a metadata table from a list of sample names 
    and various sources of documentary evidence."""
    if not sample_names:
        sample_names = SAMPLE_NAMES_FILE
    with open(sample_names) as f:
        samples = [Sample.from_name(line.strip()) for line in f]

    for _ in range(10):
        for mapper in MAPPERS:
            for sample in samples:
                try:
                    mapper.map(sample)
                except:
                    print(f'Mapper: {mapper.filename} Sample: {sample}', file=stderr)
                    raise

    if csv:
        tbl = pd.DataFrame([sample.to_son() for sample in samples])
        print(tbl.to_csv())
    else:
        stdout.write(dumps([sample.to_son() for sample in samples]))


@main.command(name='name-map')
@click.argument('metadata_table', type=str)
@click.argument('sample_names', type=click.File('r'))
def name_map(metadata_table, sample_names):
    sample_names = {line.strip().lower() for line in sample_names}
    mdata = pd.read_csv(metadata_table, dtype=str, index_col=False)
    for _, row in mdata.iterrows():
        for id_col_name in IDS:
            try:
                if str(row[id_col_name]).lower() in sample_names:
                    if row[METASUB_NAME]:
                        sname, msub_name = row[id_col_name].upper(), row[METASUB_NAME]
                        print(f'{sname},{msub_name}')
                        break
            except KeyError:
                pass


@main.command(name='uploadable')
@click.option('-s', '--sample-names', default=SAMPLE_NAMES_FILE, type=click.File('r'))
@click.argument('metadata_table', type=str)
def uploadable(sample_names, metadata_table):
    sample_names = {line.strip() for line in sample_names}
    mdata = pd.read_csv(metadata_table, dtype=str, index_col=False)
    tbl = {}
    for rowname, row in mdata.iterrows():
        for idcol in IDS:
            try:
                if row[idcol] in sample_names:
                    rowid = row[idcol]
                    break
            except KeyError:
                pass
        allowed_cols = set([
            CITY,
            CITY_CODE,
            SURFACE_MATERIAL,
            SURFACE,
            SETTING,
            ELEVATION,
            TRAFFIC_LEVEL,
            SAMPLE_TYPE,
            LOCATION_TYPE,
            PROJECT,
        ])
        tbl[rowid] = {
            col: val
            for col, val in row.iteritems()
            if col in allowed_cols
        }

    tbl = pd.DataFrame.from_dict(tbl, orient='index')
    tbl_csv_str = tbl.to_csv()
    tbl_csv_str = '-'.join(tbl_csv_str.split('.'))
    print(tbl_csv_str)


@main.command(name='by-city')
@click.argument('dirname')
@click.argument('metadata_table')
def split_metadata_by_city(dirname, metadata_table):
    makedirs(dirname, exist_ok=True)
    mdata = pd.read_csv(metadata_table, dtype=str, index_col=False)
    cities = getattr(mdata, CITY).unique()
    for city in cities:
        city_tbl = mdata[mdata[CITY] == city]
        city = '_'.join(city.split())
        fname = path.join(dirname, f'{city}_metadata.csv')
        city_tbl.to_csv(fname)


if __name__ == '__main__':
    main()
