
from json import loads, dumps
import click
from sys import stdout, stdin
import pandas as pd

from .mappers import MAPPERS
from .sample import Sample
from .constants import SAMPLE_NAMES_FILE, NA_TOKEN, IDS


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
                mapper.map(sample)

    if csv:
        tbl = pd.DataFrame([sample.to_son() for sample in samples])
        print(tbl.to_csv())
    else:
        stdout.write(dumps([sample.to_son() for sample in samples]))


@main.command(name='uploadable')
@click.argument('metadata_table', type=str)
@click.argument('sample_names', type=click.File('r'))
def uploadable(metadata_table, sample_names):
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
        tbl[rowid] = {
            col: val
            for col, val in row.iteritems()
            if col not in IDS
        }

    tbl = pd.DataFrame.from_dict(tbl, orient='index')
    print(tbl.to_csv())



if __name__ == '__main__':
    main()
