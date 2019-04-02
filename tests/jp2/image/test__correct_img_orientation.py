import pathlib

from PIL import Image


from app.jp2.image import (
    is_tile_optimised_jp2,
    _correct_img_orientation
)


def test_is_tile_optimised_jp2_true():
    path = pathlib.Path('/path/to/a.jp2')
    assert is_tile_optimised_jp2(path)


def test_is_tile_optimised_jp2_false():
    path = pathlib.Path('/path/to/a.png')
    assert not is_tile_optimised_jp2(path)


def _compare_pil_images(img1, img2):
    assert img1.size == img2.size
    for x in range(img1.width):
        for y in range(img1.height):
            assert img1.getpixel((x, y)) == img2.getpixel((x, y))


def test_correct_img_orientation_jpeg_none():
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    _compare_pil_images(img, corrected_img)


def test_correct_img_orientation_jpeg_1():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/1.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    _compare_pil_images(base_img, corrected_img)


def test_correct_img_orientation_jpeg_2():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/2.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    _compare_pil_images(base_img, corrected_img)


def test_correct_img_orientation_jpeg_3():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/3.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    _compare_pil_images(base_img, corrected_img)


def test_correct_img_orientation_jpeg_4():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/4.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    _compare_pil_images(base_img, corrected_img)


def test_correct_img_orientation_jpeg_5():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/5.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    _compare_pil_images(base_img, corrected_img)


def test_correct_img_orientation_jpeg_6():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/6.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    _compare_pil_images(base_img, corrected_img)


def test_correct_img_orientation_jpeg_7():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/7.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    _compare_pil_images(base_img, corrected_img)


def test_correct_img_orientation_jpeg_8():
    base_img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/0.jpeg'
    img_path = pathlib.Path(__file__).parent / \
        'fixtures/_correct_img_orientation/8.jpeg'
    base_img = Image.open(base_img_path)
    img = Image.open(img_path)
    corrected_img = _correct_img_orientation(img)
    _compare_pil_images(base_img, corrected_img)
