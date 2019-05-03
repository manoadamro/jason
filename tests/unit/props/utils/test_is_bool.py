from jason.props import utils


def test_int():
    assert utils.is_bool(1) == False


def test_true():
    assert utils.is_bool(True) == True


def test_false():
    assert utils.is_bool(False) == True
