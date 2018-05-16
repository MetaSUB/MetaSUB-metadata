from .parsing import parse_csv
from .constants import *
from sys import stderr


def token_specific_val_func(**tokens):

    def val_func(val, token):
        if token in tokens:
            return tokens[token](val)
        return val

    return val_func


def token_mapper(*tokens):

    def map_func(sample, sample_id, vec):
        for tkn in tokens:
            sample[tkn] = vec[tkn]

    return map_func


class Table:

    def __init__(self, filename, col_inds, mapper,
                 sep=',', skip=0, assert_len=-1,
                 name_func=lambda x, y: x, val_func=lambda x, y: x,
                 strict=False):
        self.mapper = mapper
        self.name_func = name_func
        self.store = {}
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

    def map(self, sample):
        for id_token in IDS:
            if not sample[id_token]:
                continue
            sample_id = self.name_func(sample[id_token], id_token)
            if sample_id and sample_id in self.store:
                self.mapper(sample, sample_id, self.store[sample_id])
                return
