import logging
import pathlib

logger = logging.getLogger(__name__)


def is_tile_optimised_jp2(filepath: pathlib.Path) -> bool:
    """ Determines if a file is a JPEG2000 and whether it is optimised.
        TODO: check for optimisation rather than just based on extension.
        """
    return filepath.suffix == '.jp2'


def _identity(filepath: pathlib.Path) -> pathlib.Path:
    logger.debug('%s is an acceptable file format.', filepath)
    return filepath


def _uncompress_tiff(filepath: pathlib.Path) -> pathlib.Path:
    with Image.open(filepath) as img:
        if img.info['compression'] != 'raw':
            logger.debug(
                '%s is using a compression method. Saving an uncompressed version.')
            filepath = filepath.parent / ('raw_' + filepath.name)
            img.save(filepath, compression='None')
    return filepath


def _rasterise_pdf(filepath: pathlib.Path) -> pathlib.Path:
    pass


def prepare_source_file(filepath: pathlib.Path) -> pathlib.Path:
    """ Prepares a source file for processing by kakadu by establishing the
        format and converting as required.
        From kdu_compress -usage:
        "Currently accepted image file formats are: TIFF (including BigTIFF),
        RAW (big-endian), RAWL (little-endian), BMP, PBM, PGM and PPM (including
        PNM files with sample precisions from 1 to 16), and PFM (i.e. floating
        point files), as determined by the file suffix.
        """
    img_file_funcs = {
        '.bmp': _identity,
        '.raw': _identity,
        '.pbm': _identity,
        '.pgm': _identity,
        '.ppm': _identity,
        '.jp2': _get_tiff_from_kdu,
        '.pdf': _rasterise_pdf,
        '.tif': _uncompress_tiff,
        '.tiff': _uncompress_tiff,
    }
    f = img_file_funcs.get(filepath.suffix, _get_tiff_from_pillow)
    logger.debug('%s() to be applied to %s', f.__name__, filepath)
    return f(filepath)


def get_tiff_from_pillow(filepath):
    pass


def get_orientation(image):
    pass


def rotate_as_required(image, orienation):
    pass


def _kdu_compress(img_source_path, jp2_dest_path, optimisation, image_mode=None):
    pass


def make_derivatives():
    pass


def get_reduced_image_from_kdu(jp2, size):
    pass


def get_scale_factors(width, height):
    pass


def scales_to_reduce_arg(jp2, size):
    pass


def confine(w, h, req_w, req_h):
    pass


def get_closest_scale(req_w, req_h, full_w, full_h, scales):
    pass


def scale_dim(dim, scale):
    pass
