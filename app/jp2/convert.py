import logging
import typing
import pathlib

from .settings import (
    OUTPUT_DIR,
)

from .image import (
    prepare_source_file,
    resize_and_save_img
)

from .kdu import (
    kdu_compress,
    kdu_expand_to_image
)

logger = logging.getLogger(__name__)


def _error(message: str = 'Unknown operation') -> dict:
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


def _generate_derivatives():
    if file_type != 'jp2':
        return _error(
            'File type must be JPEG2000 for derivatives-only operation.'
        )
    pass


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
    return derivative_info


def _ingest_image(source_path: pathlib.Path, dest_path: pathlib.Path, optimisation: str):
    prepared_source_path, image_mode = prepare_source_file(source_path)
    dest_path = kdu_compress(source_image, dest_path, optimisation, image_mode)


OPERATIONS = {
    'ingest': _ingest_image,
    'derivatives-only': _generate_derivatives
}


def process(
        source: str,
        dest: str = '',
        bounded_sizes: typing.List = list(),
        bounded_dir: str = '',
        optimisation: str = 'kdu_med',
        jpeg_info_id='ID',
        operation: str = 'ingest',
):

    op_func = OPERATIONS.get(operation, _error)
    source_path, dest_path = _format_paths(source, dest)
    # if is_tile_optimised_jp2(source_path):

    return result
