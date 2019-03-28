import logging
import typing
import pathlib

from PIL import (
    Image,
)

from .settings import (
    OUTPUT_DIR,
)

from .image import (
    is_tile_optimised_jp2,
    get_img_info,
    prepare_source_file,
    resize_and_save_img
)

from .kdu import (
    kdu_compress,
    kdu_expand_to_image
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
        dest_path = pathlib.Path(OUTPUT_DIR).joinpath(
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
    img = kdu_expand_to_image(source_path)
    derivative_info = []
    for size in sorted(derivative_sizes, reverse=True):
        dest_path = output_dir / '{}_{}.jpg'.format(source_path.stem, size)
        img = resize_and_save_img(img, size, dest_path)
        derivative_info.append(
            _format_derivative_info(img, dest_path)
        )
    return {'thumbs': derivative_info}


def _ingest_image(source_path: pathlib.Path, dest_path: pathlib.Path, optimisation: str):
    """
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
        kdu_compress(source_image, dest_path, optimisation, image_mode)
        return dest_path, image_info


def _derivatives_operation(source_path: pathlib.Path, thumbnail_dir: pathlib.Path, thumbnail_sizes: [int], **kwargs) -> (pathlib.Path, dict, dict):
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
        return source_path, image_info, derivative_info


def _ingest_operation(source_path: pathlib.Path, dest_path: pathlib.Path, thumbnail_dir: pathlib.Path, thumbnail_sizes: typing.List = list(), kakadu_optimisation: str = 'kdu_med', image_id='ID') -> (pathlib.Path, dict, dict):
    ingested_path, image_info = _ingest_image(
        source_path, dest_path, kakadu_optimisation)
    derivative_info = _make_derivatives(
        ingested_image, thumbnail_sizes, thumbnail_dir)
    return ingested_path, image_info, derivative_info


def process(source_path: pathlib.Path, dest_path: pathlib.Path, thumbnail_dir: pathlib.Path, thumbnail_sizes: typing.List = list(), kakadu_optimisation: str = 'kdu_med', image_id='ID', operation: str = 'ingest'):

    OPERATIONS = {
        'ingest': _ingest_operation,
        'derivatives-only': _derivatives_operation
    }

    op_func = OPERATIONS.get(operation, _error)
    result = op_func(source_path, dest_path, thumbnail_dir,
                     thumbnail_sizes, kakadu_optimisation, image_id)

    return result
