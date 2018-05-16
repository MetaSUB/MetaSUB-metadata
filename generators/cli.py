
from json import loads, dumps
import click
from sys import stdout, stdin
import pandas as pd

from .mappers import MAPPERS
from .sample import Sample
from .constants import SAMPLE_NAMES_FILE, NA_TOKEN


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

    for _ in range(3):
        for mapper in MAPPERS:
            for sample in samples:
                mapper.map(sample)

    if csv:
        tbl = pd.DataFrame([sample.to_son() for sample in samples])
        print(tbl.to_csv())
    else:
        stdout.write(dumps([sample.to_son() for sample in samples]))


if __name__ == '__main__':
    main()
