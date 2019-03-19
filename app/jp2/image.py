import io
import logging
import pathlib
import subprocess

from PIL import (
    Image,
    ImageCms,
)

import settings as app_settings

logger = logging.getLogger(__name__)


def is_tile_optimised_jp2(filepath: pathlib.Path) -> bool:
    """ Determines if a file is a JPEG2000 and whether it is optimised.
        TODO: check for optimisation rather than just based on extension.
        """
    return filepath.suffix == '.jp2'


def _get_img_mode(filepath: pathlib.Path) -> (pathlib.Path, str):
    """ For file formats that don't require conversion or other preparation
        before being converted to JPEG2000, this will open the file
        and get the image mode for use in the conversion process.
        """
    logger.debug('%s: file does not require preparation', filepath)
    with Image.open(filepath) as img:
        img_mode = img.mode
        logger.debug('%s: image mode %s', filepath, img_mode)
    return filepath, img_mode


def _uncompress_tiff(filepath: pathlib.Path) -> (pathlib.Path, str):
    """ Checks whether a tiff file has been saved with compression,
        and if so, will save an uncompressed version under a new name.
        While the image is open gets the image mode for use in the
        conversion process.
        """
    with Image.open(filepath) as img:
        img_mode = img.mode
        logger.debug('%s: image mode %s', filepath, img_mode)
        compression = img.info.get('compression')
        if compression != 'raw':
            logger.debug(
                '%s: uses compression method %s', filepath, compression)
            tiff_filepath = filepath.parent / ('raw_' + filepath.name)
            logger.debug('%s: saving as raw to %s', filepath, tiff_filepath)
            img.save(tiff_filepath, compression=None)
            filepath = tiff_filepath
    return filepath, img_mode


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
        logger.debug('%s: icc colour profile %s', img_filename,
                     img_colour_profile.profile_description)
        sRGB_profile = ImageCms.createProfile('sRGB')
        logger.debug('%s: converting colour profile from %s to %s',
                     img_filename,
                     img_colour_profile.profile_description,
                     sRGB_profile.profile_description
                     )
        img = ImageCms.profileToProfile(
            img, img_colour_profile, sRGB_profile)

    return img


def _convert_img_to_tiff(filepath: pathlib.Path) -> (pathlib.Path, str):
    """ Attempts to open a file with Pillow, correct image orienation,
        set the colour profile, and save the image as a tiff.
        While the image is open gets the image mode for use in the
        conversion process.
        """
    with Image.open(filepath) as img:
        img_filename = img.filename
        img_mode = img.mode
        logger.debug('%s: image mode %s', filepath, img_mode)
        img = _correct_img_orientation(img, img_filename)
        img = _convert_img_colour_profile(img, img_filename)
        tiff_filepath = filepath.parent.joinpath(
            'raw_' + filepath.stem).with_suffix('.tiff')
        logger.debug('%s: saving as raw to %s',
                     filepath, tiff_filepath)
        img.save(tiff_filepath, compression=None)
    return tiff_filepath, img_mode


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
        '.bmp': _get_img_mode,
        '.raw': _get_img_mode,
        '.pbm': _get_img_mode,
        '.pgm': _get_img_mode,
        '.ppm': _get_img_mode,
        '.jp2': _get_img_mode,  # TODO convert to tiff if JP2 not tile-ready.
        '.pdf': _rasterise_pdf,
        '.tif': _uncompress_tiff,
        '.tiff': _uncompress_tiff,
    }
    f = img_file_funcs.get(filepath.suffix, _convert_img_to_tiff)
    logger.debug('%s() to be applied to %s', f.__name__, filepath)
    return f(filepath)


def _kdu_compress(img_source_path: pathlib.Path, optimisation: str, image_mode: str) -> pathlib.Path:

    image_modes = {
        'L': '-no_palette',
        '1': '-no_palette',
        'RGB': '-jp2_space sRGB',
        'RGBA': '-jp2_space sRGB -jp2_alpha'
    }

    kdu_compress_templates = {
        'kdu_low':  '{kdu_path} -i {input_path} -o {output_path} Clevels=7 "Cblk={{64,64}}"'
        ' "Cuse_sop=yes" {image_mode} "ORGgen_plt=yes" "ORGtparts=R" "Corder=RPCL" -rate 0.5'
        ' "Cprecincts={{256,256}},{{256,256}},{{256,256}},{{128,128}},{{128,128}},{{64,64}},'
        '{{64,64}},{{32,32}},{{16,16}}"',
        'kdu_med':  '{kdu_path} -i {input_path} -o {output_path} Clevels=7 "Cblk={{64,64}}"'
        '"Cuse_sop=yes" {image_mode} "ORGgen_plt=yes" "ORGtparts=R" "Corder=RPCL" -rate 2'
        '"Cprecincts={{256,256}},{{256,256}},{{256,256}},{{128,128}},{{128,128}},{{64,64}},'
        '{{64,64}},{{32,32}},{{16,16}}"',
        'kdu_med_layers':  '{kdu_path} -i {input_path} -o {output_path} Clevels=7 "Cblk={{64,64}}"'
        ' "Cuse_sop=yes" {image_mode} "ORGgen_plt=yes" "ORGtparts=R" "Corder=RPCL" Clayers=6 -rate 2'
        ' "Cprecincts={{256,256}},{{256,256}},{{256,256}},{{128,128}},{{128,128}},{{64,64}},'
        '{{64,64}},{{32,32}},{{16,16}}"',
        'kdu_high': '{kdu_path} -i {input_path} -o {output_path} Clevels=7 "Cblk={{64,64}}"'
        ' "Cuse_sop=yes" {image_mode} "ORGgen_plt=yes" "ORGtparts=R" "Corder=RPCL" -rate 4'
        ' "Cprecincts={{256,256}},{{256,256}},{{256,256}},{{128,128}},{{128,128}},{{64,64}},'
        '{{64,64}},{{32,32}},{{16,16}}"',
        'kdu_max':  '{kdu_path} -i {input_path} -o {output_path} Clevels=7 "Cblk={{64,64}}"'
        ' "Cuse_sop=yes" {image_mode} "ORGgen_plt=yes" "ORGtparts=R" "Corder=RPCL" -rate -'
        ' "Cprecincts={{256,256}},{{256,256}},{{256,256}},{{128,128}},{{128,128}},{{64,64}},'
        '{{64,64}},{{32,32}},{{16,16}}"',
    }

    compress_env = {
        'LD_LIBRARY_PATH': KDU_LIB,
        'PATH': KDU_COMPRESS
    }

    kdu_compress_template = kdu_compress_templates.get(
        optimisation, kdu_compress_templates['kdu_med'])

    kdu_compress_command = kdu_compress_template.format(
        kdu_path=KDU_COMPRESS,
        input_path=img_source_path,
        output_path=jp2_output_path,
        image_mode=image_mode
    )

    try:
        result_code = subprocess.run(kdu_compress_command,
                                     env=compress_env,
                                     shell=True,
                                     check=True
                                     )
    except CalledProcessError as e:
        return


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
