from src.python.vector2 import is_shared_cardinal, is_shared_diag, subtract, v2_abs, v2_range


def test_is_shared_diag():
    assert is_shared_diag([(1, 1), (2, 2), (3, 3)])
    assert is_shared_diag([(1, 1), (1, 1), (2, 2), (3, 3)])
    assert is_shared_diag([(-1, 1), (-3, 3), (-2, 2)])
    assert is_shared_diag([(5, 0), (3, 2), (0, 5)])
    assert not is_shared_diag([(-1, 1), (2, 2), (-3, 3)])
    assert not is_shared_diag([(2, 1), (5, 4), (2, 7)])


def test_is_shared_cardinal():
    assert is_shared_cardinal([(0, 2), (0, 1), (0, 3)])
    assert is_shared_cardinal([(0, 1), (0, 1), (0, 2), (0, 3)])
    assert is_shared_cardinal([(1, 0), (1, 2), (1, 1)])
    assert not is_shared_cardinal([(-1, 1), (2, 2), (-3, 3)])


def test_subtract():
    assert subtract((0, 1), (3, 4)) == (-3, -3)
    assert subtract((-5, -3), (3, 4)) == (-8, -7)
    assert subtract((5, 7), (2, 1)) == (3, 6)


def test_v2_abs():
    assert v2_abs((-3, -3)) == (3, 3)
    assert v2_abs((-8, 7)) == (8, 7)
    assert v2_abs((3, 6)) == (3, 6)


def test_v2_range():
    assert list(v2_range((-3, -3), (2, 2))) == [(-2, -2), (-1, -1), (0, 0), (1, 1)]
    assert list(v2_range((-5, 0), (0, 0))) == [(-4, 0), (-3, 0), (-2, 0), (-1, 0)]
    assert list(v2_range((3, 6), (3, 3))) == [(3, 5), (3, 4)]
