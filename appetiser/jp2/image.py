import decimal
import io
import logging
import pathlib

from PIL import (
    Image,
    ImageCms,
)

from .kdu import image_modes

logger = logging.getLogger(__name__)

# Allows images of any size to be processed without raising a
# warning or an error.
Image.MAX_IMAGE_PIXELS = None


def is_tile_optimised_jp2(filepath: pathlib.Path) -> bool:
    """ Determines if a file is a JPEG2000 and whether it is optimised.
        TODO: check for optimisation rather than just based on extension.
        """
    return filepath.suffix == '.jp2'


def _extract_img_info(img: Image) -> dict:
    """ Extract a properties from a PIL Image and store in a dict
        for use as part of subsequent processing.
        """
    logger.debug('%s: mode - %s, width - %s, height - %s',
                 img.filename, img.mode, img.width, img.height)
    return {
        'mode': img.mode,
        'height': img.height,
        'width': img.width
    }


def get_img_info(filepath: pathlib.Path) -> (pathlib.Path, dict):
    """ For file formats that don't require conversion or other preparation
        before being converted to JPEG2000, this will open the file
        and get the image height, width and mode for use in the conversion
        process.
        """
    logger.debug('%s: file does not require preparation', filepath)
    with Image.open(filepath) as img:
        img_info = _extract_img_info(img)
    return filepath, img_info


def _convert_tiff_mode(filepath: pathlib.Path, img: Image, img_info: dict) -> (pathlib.Path, dict):
    """
    Image is already a TIFF but with a mode that we don't have KDU commands for
    Convert it to RGB + ensure XResolution + YResolution tags are set
    """
    x_resolution_tag = 282
    y_resolution_tag = 283

    x_res = img.tag_v2.get(x_resolution_tag, -1)
    y_res = img.tag_v2.get(y_resolution_tag, -1)

    img = _convert_img_colour_profile(img, img.filename)
    tiff_filepath = filepath.parent / ('raw_' + filepath.name)

    image_data = io.BytesIO()

    # write data to BytesIO and read again to get as PIL.TiffImagePlugin.TiffImageFile
    img.save(image_data, format='TIFF', compression=None)
    with Image.open(image_data, formats=['TIFF']) as new_img:
        if not new_img.tag_v2.get(x_resolution_tag, None):
            logger.debug('%s: has no XResolution tag, setting from original %s', filepath, x_res)
            new_img.tag_v2[x_resolution_tag] = x_res

        if not new_img.tag_v2.get(y_resolution_tag, None):
            logger.debug('%s: has no YResolution tag, setting from original %s', filepath, y_res)
            new_img.tag_v2[y_resolution_tag] = y_res

        logger.debug('%s: saving as raw to %s', filepath, tiff_filepath)
        new_img.save(tiff_filepath, compression=None)
        img_info['mode'] = new_img.mode

    return tiff_filepath, img_info


def _uncompress_tiff(filepath: pathlib.Path) -> (pathlib.Path, dict):
    """ Checks whether a tiff file has been saved with compression,
        and if so, will save an uncompressed version under a new name.
        While the image is open gets the image mode for use in the
        conversion process.
        """
    with Image.open(filepath) as img:
        img_info = _extract_img_info(img)
        compression = img.info.get('compression')
        if compression != 'raw':
            logger.debug(
                '%s: uses compression method %s', filepath, compression)
            tiff_filepath = filepath.parent / ('raw_' + filepath.name)
            logger.debug('%s: saving as raw to %s', filepath, tiff_filepath)
            img.save(tiff_filepath, compression=None)
            filepath = tiff_filepath

        img_mode = img_info.get('mode')
        if img_mode not in image_modes:
            logger.debug('%s: has unknown image mode: %s', filepath, img_mode)
            return _convert_tiff_mode(filepath, img, img_info)

    return filepath, img_info


def _correct_img_orientation(img: Image, img_filename: str = '') -> Image:
    """ If the image has EXIF data, and the orientation of the image in the EXIF
        data is anything
        """
    EXIF_ORIENTATION_TAG = 274
    EXIF_TRANSPOSE_OPERATIONS = [
        [],
        [],
        [Image.FLIP_LEFT_RIGHT],
        [Image.ROTATE_180],
        [Image.FLIP_TOP_BOTTOM],
        [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],
        [Image.ROTATE_270],
        [Image.FLIP_TOP_BOTTOM, Image.ROTATE_90],
        [Image.ROTATE_90],
    ]
    orientation = 0
    if hasattr(img, '_getexif'):
        exif = img._getexif()
        if exif:
            logger.debug(
                '%s: extracting orientation from EXIF data', img_filename)
            orientation = exif.get(EXIF_ORIENTATION_TAG, 0)
            logger.debug('%s: EXIF orientation %s',
                         img_filename, orientation)

    for transpose_operation in EXIF_TRANSPOSE_OPERATIONS[orientation]:
        logger.debug('%s: applying transpose operation %s',
                     img_filename, transpose_operation)
        img = img.transpose(transpose_operation)

    return img


def _convert_img_colour_profile(img: Image, img_filename: str = '') -> Image:
    """ If the image has ICC profile information, apply a transformation to this
        image from that ICC colour profile to the sRGB colour profile.
        """
    img_colour_profile_bytes = img.info.get('icc_profile')
    if img_colour_profile_bytes:
        logger.debug(
            '%s: extracting embedded colour profile', img_filename)
        img_colour_profile = ImageCms.ImageCmsProfile(
            io.BytesIO(img_colour_profile_bytes))
        img_colour_profile_name = ImageCms.getProfileName(img_colour_profile)
        logger.debug('%s: icc colour profile %s', img_filename,
                     img_colour_profile_name)
        sRGB_profile = ImageCms.createProfile('sRGB')
        logger.debug('%s: converting colour profile from %s to %s',
                     img_filename,
                     img_colour_profile_name,
                     sRGB_profile.profile_description
                     )
        img = ImageCms.profileToProfile(
            img, img_colour_profile, sRGB_profile, outputMode='RGB')

    return img


def _convert_img_to_tiff(filepath: pathlib.Path) -> (pathlib.Path, dict):
    """ Attempts to open a file with Pillow, correct image orienation,
        set the colour profile, and save the image as a tiff.
        While the image is open gets the image mode for use in the
        conversion process.
        """
    with Image.open(filepath) as img:
        img_filename = img.filename
        img_info = _extract_img_info(img)
        img = _correct_img_orientation(img, img_filename)
        img = _convert_img_colour_profile(img, img_filename)
        tiff_filepath = filepath.parent.joinpath(
            'raw_' + filepath.stem).with_suffix('.tiff')
        logger.debug('%s: saving as raw to %s',
                     filepath, tiff_filepath)
        img.save(tiff_filepath, compression=None)
    return tiff_filepath, img_info


def _rasterise_pdf(filepath: pathlib.Path) -> pathlib.Path:
    pass


def prepare_source_file(filepath: pathlib.Path) -> (pathlib.Path, dict):
    """ Prepares a source file for processing by kakadu by establishing the
        format and converting as required.
        From kdu_compress -usage:
        "Currently accepted image file formats are: TIFF (including BigTIFF),
        RAW (big-endian), RAWL (little-endian), BMP, PBM, PGM and PPM (including
        PNM files with sample precisions from 1 to 16), and PFM (i.e. floating
        point files), as determined by the file suffix.
        """
    img_file_funcs = {
        '.bmp': get_img_info,
        '.raw': get_img_info,
        '.pbm': get_img_info,
        '.pgm': get_img_info,
        '.ppm': get_img_info,
        '.jp2': get_img_info,  # TODO convert to tiff if JP2 not tile-ready.
        '.pdf': _rasterise_pdf,
        '.tif': _uncompress_tiff,
        '.tiff': _uncompress_tiff,
    }
    f = img_file_funcs.get(filepath.suffix.lower(), _convert_img_to_tiff)
    logger.debug('%s() to be applied to %s', f.__name__, filepath)
    return f(filepath)


def _scale_dimensions_to_fit(width: int, height: int, req_width: int, req_height: int) -> (int, int):
    """ For a given width and height, scale these such that they will fit within
        the required height and width by reducing them by an appropriate scale
        factor.
        Setting the precision of the Decimal context _may_ be included to allow
        for parity with .net components that use this precision (i.e. no off-by-one
        scaling issues).
        """
    if width <= req_width and height <= req_height:
        logger.debug('(%s, %s): Dimensions do not need scaling.')
        return width, height
    decimal.getcontext().prec = 17
    dec_width = decimal.Decimal(width)
    dec_height = decimal.Decimal(height)
    dec_req_width = decimal.Decimal(req_width)
    dec_req_height = decimal.Decimal(req_height)
    scale = min(dec_req_width/dec_width, dec_req_height/dec_height)
    logger.debug('(%s, %s): to fit within (%s, %s) requires a scale factor of %s',
                 dec_width, dec_height, dec_req_width, dec_req_height, scale)
    scaled_int_width = int((dec_width * scale).to_integral_exact())
    scaled_int_height = int((dec_height * scale).to_integral_exact())
    logger.debug('(%s, %s): scaled to (%s, %s)', dec_width,
                 dec_height, scaled_int_width, scaled_int_height)
    return scaled_int_width, scaled_int_height


def resize_and_save_img(img: Image, size: int, dest_path: pathlib.Path) -> Image:
    """ Resize a PIL Image so that it fits within a square of the provided size,
        and saves this file to the provided dest_path.
        Returns the Image to allow for progressive scaling down for multiple sizes,
        which is significantly faster than scaling down from a full resolution image.
        """
    scaled_width, scaled_height = _scale_dimensions_to_fit(
        img.width, img.height, size, size)
    img = img.resize((scaled_width, scaled_height), resample=Image.LANCZOS)
    logger.debug('Image resized to (%s, %s)', scaled_width, scaled_height)
    img.save(dest_path, quality=90)
    logger.debug('Resized image saved to: %s', dest_path)
    return img
