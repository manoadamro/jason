from unittest import mock

from jason.cli import run


def test_run():
    with mock.patch("jason.cli._import") as mock_import:
        mock_build = mock.Mock()
        mock_import.return_value.build = mock_build
        build_method = run("some_component")
    mock_import.assert_called_with("jason.components.some_component")
    assert build_method is mock_build
