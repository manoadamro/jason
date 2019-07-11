from jason import props


def test_handles_prop_types():
    class MyModel(props.Model):
        x = props.Int
        _y = props.Int

    assert isinstance(MyModel.__props__["x"], props.Int)


def test_ignored_underscore_prefixed():
    class MyModel(props.Model):
        x = props.Int()
        _y = props.Int()

    assert MyModel.__props__ == {"x": MyModel.x}
