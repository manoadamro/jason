from jason.props import Float


def test_converts_int_to_float():
    prop = Float()
    assert prop.load(12) == 12.0