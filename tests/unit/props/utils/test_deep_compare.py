from jason import props
from jason.props import utils


def test_compare_instance():
    assert (
        utils.deep_compare(
            props.Int(min_value=1, max_value=2), props.Int(min_value=1, max_value=2)
        )
        is True
    )


def test_compare_modified_instance():
    mod_prop = props.Int(min_value=1, max_value=2)
    del mod_prop.range.min_value
    assert utils.deep_compare(props.Int(min_value=1, max_value=2), mod_prop) is False


def test_compare_different_values():
    mod_prop = props.Int(min_value=1, max_value=2)
    del mod_prop.range.min_value
    mod_prop.range.thing = False
    assert utils.deep_compare(props.Int(min_value=1, max_value=2), mod_prop) is False
