from src.primitive import BREAK, sign


def v2_range(v1, v2):
    step0 = int(sign(v2[0] - v1[0])) if v2[0] != v1[0] else 0
    step1 = int(sign(v2[1] - v1[1])) if v2[1] != v1[1] else 0
    next_ = (v1[0] + step0, v1[1] + step1)
    while next_ != v2:
        yield next_
        n0 = next_[0] + step0 if next_[0] != v2[0] else 0
        n1 = next_[1] + step1 if next_[1] != v2[1] else 0
        next_ = (n0, n1)


def is_shared_diag(positions):
    iter_ = iter(positions)
    left = next(iter_)
    last_sign = None

    while True:
        right = next(iter_, BREAK)

        if right is BREAK:
            return True

        d_y = left[0] - right[0]
        d_x = left[1] - right[1]

        v_sign = sign(d_y) == sign(d_x)
        same_mag = abs(d_y) == abs(d_x)

        if not same_mag or (last_sign is not None and last_sign != v_sign):
            return False

        last_sign = v_sign
        left = right


def is_shared_cardinal(positions):
    iter_ = iter(positions)
    left = next(iter_)
    right = next(iter_)

    while left == right:
        right = next(iter_)

    v = 0

    if left[1] == right[1]:
        v = 1
    elif left[0] != right[0]:
        return False

    while True:
        left = right
        right = next(iter_, BREAK)

        if right is BREAK:
            return True

        if left[v] != right[v]:
            return False


def difference(v1, v2):
    return (v1[0] - v2[0], v1[1], v2[1])


def v2_abs(v1):
    return (abs(v1[0]), abs(v1[1]))
