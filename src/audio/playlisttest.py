from playlist import querify, Track


def test_querify():
    assert (
        querify(Track(name="Electric Shock", artists=["f(x)"]))
        == "Electric Shock - f(x)"
    )
    assert querify(Track(name="A", artists=["B", "C", "D"])) == "A - B, C, D"
    assert querify(Track(name="A", artists=["B C", "D E"])) == "A - B C, D E"
