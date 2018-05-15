
from json import loads, dumps
import click
from sys import stdout, stdin

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
        for sample in samples:
            print(sample.to_csv())
    else:
        stdout.write(dumps([sample.to_son() for sample in samples]))


@main.command(name='convert-tags')
def convert_tags():
    stems = []
    tag_list = []
    tag_names = set()

    for line in stdin:
        tkns = line.strip().split(',')
        if ':' in tkns[-1]:
            stems.append(tkns[:-1])
            tags = tkns[-1]
            tags = [tag.split(':') for tag in tags.split()]
            try:
                tags = {tag[0]: tag[1] for tag in tags}
            except IndexError:
                print(line)
                print(tags)
                raise
            tag_list.append(tags)
            for tag_name in tags:
                tag_names.add(tag_name)

    tag_names = sorted([tag_name for tag_name in tag_names])

    for i, stem_tkns in enumerate(stems):
        tags = tag_list[i]
        tag_tkns = []
        for tag_name in tag_names:
            try:
                tag_tkns.append(tags[tag_name])
            except KeyError:
                tag_tkns.append(NA_TOKEN)
        tkns = stem_tkns + tag_tkns
        msg = '{},' * len(tkns)
        msg = msg[:-1]
        msg = msg.format(*tkns)
        print(msg)


if __name__ == '__main__':
    main()
