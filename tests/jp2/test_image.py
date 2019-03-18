import os
import pathlib
import pytest

from PIL import Image


from app.jp2.image import (
    is_tile_optimised_jp2,
    _correct_img_orientation
)


def test_is_tile_optimised_jp2_true():
    path = pathlib.Path('/path/to/a.jp2')
    assert is_tile_optimised_jp2(path) == True


def test_is_tile_optimised_jp2_false():
    path = pathlib.Path('/path/to/a.png')
    assert is_tile_optimised_jp2(path) == False


def test_correct_img_orientation_none():
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    assert img.size == corrected_img.size
    assert img.tobytes() == corrected_img.tobytes()


def test_correct_img_orientation_1():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/1.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    assert img.size == corrected_img.size
    assert base_img.tobytes() == corrected_img.tobytes()

def test_correct_img_orientation_2():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/2.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    assert img.size == corrected_img.size
    assert base_img.tobytes() == corrected_img.tobytes()


def test_correct_img_orientation_3():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/3.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    assert img.size == corrected_img.size
    assert base_img.tobytes() == corrected_img.tobytes()


def test_correct_img_orientation_4():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/4.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    assert img.size == corrected_img.size
    assert base_img.tobytes() == corrected_img.tobytes()


def test_correct_img_orientation_5():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/5.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    assert img.size == corrected_img.size
    assert base_img.tobytes() == corrected_img.tobytes()


def test_correct_img_orientation_6():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/6.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    assert img.size == corrected_img.size
    assert base_img.tobytes() == corrected_img.tobytes()


def test_correct_img_orientation_7():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/7.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    assert img.size == corrected_img.size
    assert base_img.tobytes() == corrected_img.tobytes()


def test_correct_img_orientation_8():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/8.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    assert img.size == corrected_img.size
    assert base_img.tobytes() == corrected_img.tobytes()
