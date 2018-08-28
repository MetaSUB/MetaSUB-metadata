from .parsing import parse_csv
from .constants import *
from sys import stderr
from .utils import remove_leading_char


def token_specific_val_func(**tokens):

    def val_func(val, token):
        if token in tokens:
            return tokens[token](val)
        return val

    return val_func


def token_mapper(*tokens, strict=True):

    def map_func(sample, sample_id, vec):
        for tkn in tokens:
            try:
                if False and (sample[tkn] is not None):  # Turn off this check for now
                    assert sample[tkn].lower() == vec[tkn].lower(), \
                        f'\nToken {tkn}\nSample {sample[tkn]}\nSample ID {sample_id}\nVec {vec[tkn]}'
                sample[tkn] = vec[tkn]
            except KeyError:
                if strict:
                    print(
                        f'\nToken {tkn}\nSample {sample}\nSample ID {sample_id}\nVec {vec}',
                        file=stderr
                    )
                    raise

    return map_func


def ha_filename_table(filename, description_key=None, strict=True, token_val_funcs=None):
    skip = 0
    if filename[:-4] == '.txt':
        skip = 2
    token_positions = {INDEX_SEQ: 1, SL_NAME: 2, HA_ID: 3}
    if description_key:
        token_positions[description_key] = 5

    if token_val_funcs is not None:
        pass
    elif description_key == BC:
        token_val_funcs = {BC: remove_leading_char('0')}
    elif description_key == METASUB_NAME:
        token_val_funcs = {METASUB_NAME: remove_leading_char('g')}


    val_func = lambda x, y: x
    if token_val_funcs:
        val_func = token_specific_val_func(**token_val_funcs)

    my_tokens = [INDEX_SEQ, SL_NAME, HA_ID]
    if description_key in IDS:
        my_tokens.append(description_key)
    my_token_mapper = token_mapper(*my_tokens, strict=strict)

    return Table(
        filename,
        token_positions,
        my_token_mapper,
        name_func=token_specific_val_func(**{SL_NAME: lambda x: x.lower()}),
        val_func=val_func,
        sep='\t',
        skip=skip,
    )


class Table:

    def __init__(self, filename, col_inds, mapper,
                 sep=',', skip=0, assert_len=-1,
                 name_func=lambda x, y: x, val_func=lambda x, y: x,
                 strict=False, debug=False):
        self.filename = filename
        self.mapper = mapper
        self.name_func = name_func
        self.store = {}
        self.debug = debug
        for tkns in parse_csv(filename,
                              sep=sep, skip=skip, assert_len=assert_len):
            vec = {}
            for name, index in col_inds.items():
                try:
                    vec[name] = val_func(tkns[index], name)
                except IndexError:
                    if strict:
                        raise

            for id_token in IDS:
                if id_token in vec:
                    key = self.name_func(vec[id_token], id_token)
                    self.store[key] = vec
        if self.debug:
            print(self.store, file=stderr)

    def map(self, sample):
        for id_token in IDS:
            if not sample[id_token]:
                continue
            sample_id = self.name_func(sample[id_token], id_token)
            if sample_id and sample_id in self.store:
                if self.debug:
                    print(f'{self.filename} {sample_id} {id_token}', file=stderr)
                self.mapper(sample, sample_id, self.store[sample_id])
                return
