from src.python.primitive import BREAK, sign


def v2_range(l, r):
    step_l = int(sign(r[0] - l[0])) if r[0] != l[0] else 0
    step_r = int(sign(r[1] - l[1])) if r[1] != l[1] else 0
    next_ = (l[0] + step_l, l[1] + step_r)
    while next_ != r:
        yield next_
        next_ = (
            next_[0] + (step_l if next_[0] != r[0] else 0),
            next_[1] + (step_r if next_[1] != r[1] else 0)
        )


def is_shared_diag(v2):
    iter_ = iter(v2)
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


def is_shared_cardinal(v2):
    iter_ = iter(v2)
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


def is_shared_union_jack(v2):
    return is_shared_cardinal(v2) or is_shared_diag(v2)


def difference(l, r):
    return (l[0] - r[0], l[1] - r[1])


def v2_abs(v2):
    return (abs(v2[0]), abs(v2[1]))


def sqr_mag(v2):
    return v2[0] ** 2 + v2[1] ** 2
