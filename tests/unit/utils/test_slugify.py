from jason import slugify


def test_slugify():
    assert slugify("šömę THįñg çøõL") == "some-thing-cool"
