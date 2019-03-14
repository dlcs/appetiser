import pathlib

from app.jp2.image import (
    is_tile_optimised_jp2,
)


def test_is_tile_optimised_jp2_true():
    path = pathlib.Path('/path/to/a.jp2')
    assert is_tile_optimised_jp2(path) == True


def test_is_tile_optimised_jp2_false():
    path = pathlib.Path('/path/to/a.png')
    assert is_tile_optimised_jp2(path) == False
