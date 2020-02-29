from matter.utils import flatmap


def test_flatmap():
    assert list(flatmap(lambda x: [x + 1], [1, 2, 3])) == [2, 3, 4]
