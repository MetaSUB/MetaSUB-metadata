from sys import stderr


def parse_csv_to_tkns(csv_str, sep=','):
    in_quote = False
    cur_token = ''
    for c in csv_str:
        if c == '"':
            in_quote = not in_quote
        elif (not in_quote) and (c == sep):
            yield cur_token, False
            cur_token = ''
        elif (not in_quote) and (c == '\n'):
            yield cur_token, True
            cur_token = ''
        else:
            cur_token += c
    yield cur_token, True


def parse_csv_str(csv_str, sep=','):
    cur_tkns = []
    for tkn, newline in parse_csv_to_tkns(csv_str, sep=sep):
        cur_tkns.append(tkn.strip().lower())
        if newline:
            yield cur_tkns
            cur_tkns = []


def parse_csv(fname, assert_len=-1, skip=0, sep=','):
    codec = 'utf-8'
    try:
        csv_str = open(fname, encoding=codec).read()
    except UnicodeDecodeError:
        raise Exception(f'Cannot parse {fname} with {codec}')
    for i, tkns in enumerate(parse_csv_str(csv_str, sep=sep)):
        if i < skip:
            continue
        if assert_len > 0:
            try:
                msg = """
                        expected: {}
                        observed: {}
                        tokens: {}
                      """.format(assert_len, len(tkns), tkns)
                assert len(tkns) == assert_len, msg
            except AssertionError as ae:
                #print(ae, file=stderr)
                continue
        if len(tkns) > 0:
            yield tkns
