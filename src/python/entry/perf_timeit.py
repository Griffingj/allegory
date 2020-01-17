import timeit

if __name__ == "__main__":
    # code snippet to be executed only once
    mysetup = '''
from src.python.primitive import sign
import math

BREAK = object()

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

b=[(1, 1), (1, 1), (2, 2), (3, 3)]
'''

    # code snippet whose execution time is to be measured
    mycode = '''
is_shared_diag(b)
'''

    # timeit statement
    print(timeit.timeit(setup=mysetup, stmt=mycode, number=10000))
