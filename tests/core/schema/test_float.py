from jason.core.schema import Float


def test_converts_int_to_float():
    prop = Float()
    assert prop.load(12) == 12.0
