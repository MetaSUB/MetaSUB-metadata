
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
def best_effort(csv):
    """Generate a metadata table from a list of sample names 
    and various sources of documentary evidence."""
    with open(SAMPLE_NAMES_FILE) as f:
        samples = [Sample.from_name(line.strip()) for line in f]

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
