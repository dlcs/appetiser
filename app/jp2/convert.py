import logging
import typing
import os
import pathlib

from .settings import (
    KDU_COMPRESS_CMD,
    OUTPUT_DIR,
)

from .image import (
    is_tile_optimised_jp2,
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


def _ingest_image(source_path: pathlib.Path, dest_path: pathlib.Path):
    kdu_ready, image_mode = get_kdu_ready_file(source_path)
    pass


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
