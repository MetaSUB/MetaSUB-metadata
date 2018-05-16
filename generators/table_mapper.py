from .parsing import parse_csv
from .constants import *

def token_mapper(*tokens):

    def map_func(sample, sample_id, vec):
        for tkn in tokens:
            sample[tkn] = vec[tkn]

    return map_func


class Table:

    def __init__(self, filename, col_inds, mapper,
                 sep=',', skip=0, assert_len=-1,
                 name_func=lambda x, y: x, val_func=lambda x, y: x):
        self.mapper = mapper
        for tkns in parse_csv(filename, sep=sep, skip=skip, assert_len=assert_len):
            vec = {}
            for name, index in col_inds.items():
                vec[name] = val_func(tkns[index], name)
            self.store = {}
            for id_token in IDS:
                if id_token in vec:
                    key = name_func(vec[id_token], id_token)
                    self.store[key] = vec

    def map(self, sample):
        for id_token in IDS:
            sample_id = sample[id_token]
            if sample_id and sample_id in self.store:
                self.mapper(sample, sample_id, self.store[sample_id])
                return
