from src.vector2 import is_shared_cardinal, is_shared_diag


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
