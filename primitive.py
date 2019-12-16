def set_(d, key, val):
    n = d
    keys = key.split(".")
    if (len(key)):
        last = keys.pop()
        for k in keys:
            if (k in n):
                n = n[k]
            else:
                n[k] = {}
                n = n[k]
        n[last] = val
    return d


def get_(d, key):
    n = d
    keys = key.split(".")
    if (len(key)):
        for k in keys:
            if (type(n) is dict and k in n):
                n = n[k]
            else:
                return None
        return n
    else:
        return d
