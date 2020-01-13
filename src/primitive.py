from itertools import chain
import functools
import math

lowest = float("-inf")
highest = float("inf")


def set_(dictionary, key, val):
    next_ = dictionary
    if len(key):
        keys = key.split(".")
        last = keys.pop()
        for k in keys:
            if k in next_:
                next_ = next_[k]
            else:
                next_[k] = {}
                next_ = next_[k]
        next_[last] = val
    return dictionary


def get_(dictionary, key):
    next_ = dictionary
    if len(key):
        for k in key.split("."):
            if (type(next_) is dict and k in next_):
                next_ = next_[k]
            else:
                return None
        return next_
    else:
        return dictionary


BREAK = object()


def fold(cb, iter_, acc_=None):
    nxt = next(iter_, BREAK)
    acc = acc_
    while nxt is not BREAK:
        acc = cb(acc, nxt)
        nxt = next(iter_, BREAK)
    return acc


def subtract(base_str, remove_str):
    s = set(remove_str)
    return fold(lambda a, n: a + n if n not in s else a, iter(base_str), "")


def intersect(str1, str2):
    return set(str1).intersection(str2)


def clamp(l, v, h=highest):
    return max(l, min(v, h))


sign = functools.partial(math.copysign, 1)


def interleave(*iterables):
    return chain.from_iterable(zip(*iterables))
