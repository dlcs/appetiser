import logging
import shutil
import typing
import os
import pathlib

from PIL import (
    Image,
)

from .image import (
    is_tile_optimised_jp2,
    get_img_info,
    prepare_source_file,
    resize_and_save_img
)

from .jp2 import (
    compress,
    expand_to_image
)

from .settings import (
    OUTPUT_DIR
)

logger = logging.getLogger(__name__)


def _error(message: str = 'Unknown operation', **kwargs) -> dict:
    return {
        'status': 'error',
        'message': message
    }


def _format_paths(source: str, dest: str = '') -> typing.Tuple[pathlib.Path, pathlib.Path]:
    """ Casts provided pair of paths to pathlib.Path, and generates
        the output path from the source if not provided.
        """
    source_path = pathlib.Path(source)
    if dest:
        dest_path = pathlib.Path(dest)
    else:
        dest_path = OUTPUT_DIR.joinpath(
            source_path.stem).with_suffix('.jp2')
    return source_path, dest_path


def _format_derivative_info(img: Image, dest_path: pathlib.Path) -> dict:
    logger.debug('%s: formatting thumbnail information', dest_path)
    return {
        'path': str(dest_path),
        'width': img.width,
        'height': img.height
    }


def _make_derivatives(source_path: pathlib.Path, derivative_sizes: [int], output_dir: pathlib.Path) -> list:
    """ Manages the creation of derivatives (only thumbnails at present) for a given JPEG200 file,
        returning information about the derivatives and where they're located.
        """
    img = expand_to_image(source_path)
    derivative_info = []
    for size in sorted(derivative_sizes, reverse=True):
        dest_path = output_dir / '{}_{}.jpg'.format(source_path.stem, size)
        img = resize_and_save_img(img, size, dest_path)
        derivative_info.append(
            _format_derivative_info(img, dest_path)
        )
    return derivative_info


def _ingest_image(source_path: pathlib.Path, dest_path: pathlib.Path, optimisation: str) -> (pathlib.Path, dict):
    """ Manages the initial conversion of the provided source image file to a
        tile optimised JPEG2000 file using the provided optimisation type.
        """
    logger.debug('%s: Preparing file for ingest.', source_path)
    prepared_source_path, image_info = prepare_source_file(source_path)
    if is_tile_optimised_jp2(prepared_source_path):
        logger.debug('%s: Already a JPEG2000, copying to %s.',
                     source_path, dest_path)
        shutil.copy(source_path, dest_path)
        return dest_path, image_info
    else:
        image_mode = image_info.get('mode')
        logger.debug('%s: Being used for conversion to JPEG2000, with colour mode: %s',
                     prepared_source_path, image_mode)
        compress(prepared_source_path, dest_path, optimisation, image_mode)
        return dest_path, image_info


def _derivatives_operation(source_path: pathlib.Path,
                           thumbnail_dir: pathlib.Path,  # TODO: shouldn't need to provide thumbnail dir
                           thumbnail_sizes: [int], **kwargs) -> dict:
    """ Only
        """
    if not is_tile_optimised_jp2(source_path):
        return _error(
            'File type must be JPEG2000 for derivatives-only operation.'
        )
    else:
        _, image_info = get_img_info(source_path)
        derivative_info = _make_derivatives(
            source_path, thumbnail_sizes, thumbnail_dir)
        return {
            'jp2': str(source_path),
            'height': image_info.get('height'),
            'width': image_info.get('width'),
            'thumbs': derivative_info
        }


def _ingest_operation(source_path: pathlib.Path,
                      dest_path: pathlib.Path,
                      thumbnail_dir: pathlib.Path,  # TODO: shouldn't need to provide thumbnail_dir
                      thumbnail_sizes: typing.List = list(),
                      optimisation: str = 'kdu_med',
                      image_id='ID') -> dict:
    ingested_path, image_info = _ingest_image(
        source_path, dest_path, optimisation)
    derivative_info = _make_derivatives(
        ingested_path, thumbnail_sizes, thumbnail_dir)
    return {
        'jp2': str(ingested_path),
        'height': image_info.get('height'),
        'width': image_info.get('width'),
        'thumbs': derivative_info
    }


def process(**kwargs) -> dict:

    OPERATIONS = {
        'ingest': _ingest_operation,
        'derivatives-only': _derivatives_operation
    }
    op_func = OPERATIONS.get(kwargs.pop('operation', 'error'), _error)
    result = op_func(**kwargs)
    return result
