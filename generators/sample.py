def guess_name_kind(name):
    if name[:2] == 'SL':
        return 'sl_name'
    if 'cem' in name.lower():
        return 'ha_name'
    if 'db' in name.lower():
        return 'ha_name'
    if 'csd16' in name.lower():
        return 'msub_name'
    if 'oly' in name.lower():
        return 'msub_name'
    tkns = name.split('_')
    if len(tkns) == 3:
        return 'msub_name'
    if 'porto' in name.lower():
        return 'msub_name'
    return 'unknown'


def clean_token(tkn):
    tkn = tkn.strip()
    tkn = '_'.join(tkn.split())
    tkn = tkn.lower()
    return tkn


class Sample:

    def __init__(self):
        self.sl_name = None
        self.msub_name = None
        self.ha_name = None
        self.metadata = {}
        self.bc = None
        self.pos = None

    def to_son(self):
        return {
            'sl_name': self.sl_name,
            'msub_name': self.msub_name,
            'ha_name': self.ha_name,
            'metadata': self.metadata,
            'bc': self.bc,
            'pos': self.pos,
        }

    def to_csv(self):
        plate, pos_in_plate = None, None
        if self.pos:
            plate, pos_in_plate = self.pos
        mdata = ''
        for k, v in self.metadata.items():
            mdata += '{}:{} '.format(k, clean_token(v))
        msg = '{},{},{},{},{},{},{}'.format(
            self.sl_name,
            self.msub_name,
            self.ha_name,
            self.bc,
            plate,
            pos_in_plate,
            mdata
        )
        return msg

    def __str__(self):
        return str(self.to_son())

    @classmethod
    def from_son(cls, son):
        obj = cls()
        for k, v in son.items():
            setattr(obj, k, v)
        return obj

    @classmethod
    def from_name(cls, name):
        kind = guess_name_kind(name)
        obj = cls()
        setattr(obj, kind, name)
        return obj
