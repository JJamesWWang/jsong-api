import pytest
from playlist import querify, Track


@pytest.fixture
def track1():
    return Track(name="Electric Shock", artists=["f(x)"], duration=0)


@pytest.fixture
def track2():
    return Track(name="A", artists=["B", "C", "D"], duration=0)


@pytest.fixture
def track3():
    return Track(name="A", artists=["B C", "D E"], duration=0)


def test_querify(track1: Track, track2: Track, track3: Track):
    assert querify(track1) == "Electric Shock - f(x)"
    assert querify(track2) == "A - B, C, D"
    assert querify(track3) == "A - B C, D E"
