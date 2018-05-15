
def getOrNone(tbl, key, default=None):
    if key is None:
        return default
    try:
        return tbl[key]
    except KeyError:
        return default
