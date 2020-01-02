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


BREAK = object()


def fold(cb, iter, acc_=None):
    nxt = next(iter, BREAK)
    acc = acc_
    while nxt is not BREAK:
        acc = cb(acc, nxt)
        nxt = next(iter, BREAK)
    return acc


def subtract(base_str, remove_str):
    s = set(remove_str)
    return fold(lambda a, n: a + n if n not in s else a, iter(base_str), "")


def intersect(str1, str2):
    return set(str1).intersection(str2)
