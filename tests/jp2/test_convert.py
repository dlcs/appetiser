import pathlib
from app.jp2.convert import (
    _error,
    _format_paths,
)


def test_error_default():
    expected_error = {
        'status': 'error',
        'message': 'Unknown operation'
    }

    assert _error() == expected_error


def test_error_message():
    message = 'A test message'
    expected_error = {
        'status': 'error',
        'message': message
    }

    assert _error(message) == expected_error


def test_format_paths_default():
    source = '/path/to/source.png'
    dest = '/opt/tizer/out/source.jp2'
    source_path, dest_path = _format_paths(source)
    assert isinstance(source_path, pathlib.Path)
    assert isinstance(dest_path, pathlib.Path)
    assert str(source_path) == source
    assert str(dest_path) == dest


def test_format_paths_with_dest():
    source = '/path/to/source.png'
    dest = '/path/to/a/dest.jp2'
    source_path, dest_path = _format_paths(source, dest)
    assert isinstance(source_path, pathlib.Path)
    assert isinstance(dest_path, pathlib.Path)
    assert str(source_path) == source
    assert str(dest_path) == dest
