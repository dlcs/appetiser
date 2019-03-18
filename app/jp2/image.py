import logging
import pathlib

from PIL import (
    Image,
)

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
    """ Checks whether a tiff file has been saved with compression,
        and if so, will save an uncompressed version under a new name.
        """
    with Image.open(filepath) as img:
        if img.info['compression'] != 'raw':
            logger.debug(
                '%s is using a compression method. Saving an uncompressed version.')
            filepath = filepath.parent / ('raw_' + filepath.name)
            img.save(filepath, compression='None')
    return filepath


def _correct_img_orientation(img: Image) -> Image:
    """ If the image has EXIF data, and the orientation of the image in the EXIF
        data is anything
        """
    EXIF_ORIENTATION_TAG = 274
    EXIF_TRANSPOSE_OPERATIONS = [
        [],                                        # do nothing for images without
        [],  # 1   top      left
        [Image.FLIP_LEFT_RIGHT],  # 2   top      right
        [Image.ROTATE_180],  # 3   bottom   right
        [Image.FLIP_TOP_BOTTOM],  # 4   bottom   left
        [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],  # 5   left     top
        [Image.ROTATE_270],  # 6   right    top
        [Image.FLIP_TOP_BOTTOM, Image.ROTATE_90],  # 7   right    bottom
        [Image.ROTATE_90],  # 8   left     bottom
    ]
    orientation = 0
    img_filename = img.filename  # property is lost after one transpose operation
    if hasattr(img, '_getexif'):
        exif = img._getexif()
        if exif:
            logger.debug('%s has EXIF data.', img_filename)
            orientation = exif.get(EXIF_ORIENTATION_TAG, 0)
            print('\n')
            print("orientation: " + str(orientation))
            logger.debug('%s has EXIF orientation %s',
                         img_filename, orientation)

    for transpose_operation in EXIF_TRANSPOSE_OPERATIONS[orientation]:
        logger.debug('%s is having transpose operation %s applied',
                     img_filename, transpose_operation)
        print("transpose: " + str(transpose_operation))
        img = img.transpose(transpose_operation)
    return img


def _convert_img_to_tiff(filepath: pathlib.Path) -> pathlib.Path:
    """ Attempts to open a file with Pillow, correct image orienation,
        set the colour profile, and save the image as a tiff.
        """


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
        '.jp2': _identity,  # TODO convert to tiff if JP2 not tile-ready.
        '.pdf': _rasterise_pdf,
        '.tif': _uncompress_tiff,
        '.tiff': _uncompress_tiff,
    }
    f = img_file_funcs.get(filepath.suffix, _convert_img_to_tiff)
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
