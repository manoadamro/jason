from jason.props import utils


def test_returns_value():
    assert utils.maybe_call("hello") == "hello"


def test_calls():
    assert utils.maybe_call(lambda: "thing") == "thing"
