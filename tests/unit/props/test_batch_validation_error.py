from jason.props import BatchValidationError


def test_error():
    err = BatchValidationError(
        "something went wrong", ("a thing", "another thing", "and another thing")
    )
    assert (
        str(err)
        == """failed to load batch (3 errors):
something went wrong
    - a thing
    - another thing
    - and another thing"""
    )


def test_nested_error():
    nested = BatchValidationError(
        "something went wrong", ("a thing", "another thing", "and another thing")
    )
    err = BatchValidationError("something else went wrong", ("a thing", nested))
    assert (
        str(err)
        == """failed to load batch (4 errors):
something else went wrong
    - a thing
    - something went wrong
        - a thing
        - another thing
        - and another thing"""
    )
