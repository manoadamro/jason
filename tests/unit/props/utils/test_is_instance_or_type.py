from jason.props import utils


def test_is_instance():
    assert utils.is_instance_or_type(123, int) is True


def test_is_not_instance():
    assert utils.is_instance_or_type("nope", int) is False


def test_is_type():
    assert utils.is_instance_or_type(int, int) is True


def test_is_not_type():
    assert utils.is_instance_or_type(str, int) is False
