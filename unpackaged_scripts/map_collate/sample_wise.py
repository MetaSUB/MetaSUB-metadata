from sample import Sample
from json import loads, dumps
import click
from sys import stdout
from mappers import *


mappers = [SLNameToHAName(), HANameToPos(), PosToBC(), BCToMetadata(), MSubToCity(), Handle5106HANames(), GuessProj()]


@click.command()
@click.option('--init/--not-init', default=False)
@click.option('--csv/--json', default=False)
@click.argument('db_fname')
def main(init, csv, db_fname):
    if init:
        with open(db_fname) as f:
            samples = [Sample.from_name(line.strip()) for line in f]
    else:
        db = loads(open(db_fname).read())
        samples = [Sample.from_son(son_obj) for son_obj in db]

    for mapper in mappers:
        for sample in samples:
            mapper.map(sample)

    if csv:
        for sample in samples:
            print(sample.to_csv())
    else:
        stdout.write(dumps([sample.to_son() for sample in samples]))


if __name__ == '__main__':
    main()
