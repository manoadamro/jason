from jason.props import utils


def test_is_type():
    assert utils.is_type(int) is True


def test_is_not_type():
    assert utils.is_type(123) is False


def test_is_specific_type():
    assert utils.is_type(int, int) is True


def test_is_not_specific_type():
    assert utils.is_type(str, int) is False
