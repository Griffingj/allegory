from itertools import chain
import functools
import math

highest = float('inf')
lowest = -highest


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


def subtract_str(base_str, remove_str):
    s = set(remove_str)
    return fold(lambda a, n: a + n if n not in s else a, iter(base_str), "")


def intersect_str(str1, str2):
    return set(str1).intersection(str2)


def clamp(l, v, h=highest):
    return max(l, min(v, h))


sign = functools.partial(math.copysign, 1)


def interleave(*iterables):
    return chain.from_iterable(zip(*iterables))


def compare(i1, i2):
    d = i1 - i2
    return d if d == 0 else sign(d)


class DllNode():
    def __init__(self, left, right, key, val):
        self.left = left
        self.right = right
        self.key = key
        self.val = val


class DoublyList():
    def __init__(self, l_head=None, r_head=None, length=0):
        self.l_head = l_head
        self.r_head = r_head
        self.length = length

    def append_node(self, node):
        if self.l_head is None:
            self.r_head = self.l_head = node
        else:
            node.left = self.r_head
            self.r_head = self.r_head.right = node
        self.length += 1
        return node

    def append(self, key, val):
        return self.append_node(DllNode(None, None, key, val))

    def pop(self):
        if self.r_head is not None:
            node = self.r_head
            if self.length == 1:
                self.l_head = self.r_head = None
            else:
                self.r_head = self.r_head.left
            node.right = node.left = None
            self.length -= 1
            return node

    def del_node(self, node):
        if node == self.l_head:
            self.l_head = node.right

        if node.right is not None:
            node.right.left = node.left

        if node == self.r_head:
            self.r_head = node.left

        if node.left is not None:
            node.left.right = node.right

        node.right = node.left = None
        self.length -= 1
        return node

    def popleft(self):
        if self.r_head is not None:
            node = self.l_head
            if self.length == 1:
                self.r_head = self.l_head = None
            else:
                self.l_head = self.l_head.right
            node.right = node.left = None
            self.length -= 1
            return node

    def prepend_node(self, node):
        if self.l_head is None:
            self.r_head = self.l_head = node
        else:
            node.right = self.l_head
            self.l_head = self.l_head.left = node
        self.length += 1
        return node

    def prepend(self, key, val):
        return self.append_node(DllNode(None, None, key, val))


NO_VAL = object()


class LruMap():
    def __init__(self, maxlen=highest):
        self.map = dict()
        self.dll = DoublyList()
        self.maxlen = maxlen
        self.length = 0

    def put(self, key, val):
        if key in self.map:
            node = self.map[key]
            node.val = val
        else:
            node = self.dll.append(key, val)
            self.map[key] = node
            self.length += 1

            if self.length > self.maxlen:
                self.length -= 1
                removed = self.dll.popleft()
                self.map.pop(removed.key)

        return self

    def get(self, key, or_else=None):
        node = self.map.get(key, NO_VAL)
        if node == NO_VAL:
            return or_else
        self.dll.del_node(node)
        self.dll.append_node(node)
        return node.val
