import logging
import pathlib
import subprocess
import tempfile

from PIL import (
    Image,
)

from .settings import (
    KDU_COMPRESS,
    KDU_EXPAND,
    KDU_LIB
)

logger = logging.getLogger(__name__)

# Allows images of any size to be processed without raising a
# warning or an error.
Image.MAX_IMAGE_PIXELS = None


def _run_kdu_command(kdu_command: str, env: dict):
    try:
        logger.debug('Running command: %s', kdu_command)
        subprocess.run(kdu_command,
                       env=env,
                       shell=True,
                       check=True,
                       capture_output=True
                       )
    except subprocess.CalledProcessError as e:
        logger.error(f"kdu command failed. Full output:{e.output}")
        raise e


def kdu_compress(source_path: pathlib.Path, dest_path: pathlib.Path,
                 optimisation: str, image_mode: str) -> pathlib.Path:
    """ Uses the kdu_compress command to convert a source image
        (in BMP, RAW, PBM, PGM, PPM or TIFF formats) to a JPEG2000.
        """

    image_modes = {
        'L': '-no_palette',
        '1': '-no_palette',
        'RGB': '-jp2_space sRGB',
        'RGBA': '-jp2_space sRGB -jp2_alpha'
    }

    if image_mode not in image_modes:
        logger.warning(f"image_mode '{image_mode}' is not in known list")

    kdu_compress_templates = {
        'kdu_low':  '{kdu_compress_path} -i {input_path} -o {output_path} Clevels=7 "Cblk={{64,64}}"'
        ' "Cuse_sop=yes" {image_mode} "ORGgen_plt=yes" "ORGtparts=R" "Corder=RPCL" -rate 0.5'
        ' "Cprecincts={{256,256}},{{256,256}},{{256,256}},{{128,128}},{{128,128}},{{64,64}},'
        '{{64,64}},{{32,32}},{{16,16}}"',
        'kdu_med':  '{kdu_compress_path} -i {input_path} -o {output_path} Clevels=7 "Cblk={{64,64}}"'
        ' "Cuse_sop=yes" {image_mode} "ORGgen_plt=yes" "ORGtparts=R" "Corder=RPCL" -rate 2'
        ' "Cprecincts={{256,256}},{{256,256}},{{256,256}},{{128,128}},{{128,128}},{{64,64}},'
        '{{64,64}},{{32,32}},{{16,16}}"',
        'kdu_med_layers':  '{kdu_compress_path} -i {input_path} -o {output_path} Clevels=7 "Cblk={{64,64}}"'
        ' "Cuse_sop=yes" {image_mode} "ORGgen_plt=yes" "ORGtparts=R" "Corder=RPCL" Clayers=6 -rate 2'
        ' "Cprecincts={{256,256}},{{256,256}},{{256,256}},{{128,128}},{{128,128}},{{64,64}},'
        '{{64,64}},{{32,32}},{{16,16}}"',
        'kdu_high': '{kdu_compress_path} -i {input_path} -o {output_path} Clevels=7 "Cblk={{64,64}}"'
        ' "Cuse_sop=yes" {image_mode} "ORGgen_plt=yes" "ORGtparts=R" "Corder=RPCL" -rate 4'
        ' "Cprecincts={{256,256}},{{256,256}},{{256,256}},{{128,128}},{{128,128}},{{64,64}},'
        '{{64,64}},{{32,32}},{{16,16}}"',
        'kdu_max':  '{kdu_compress_path} -i {input_path} -o {output_path} Clevels=7 "Cblk={{64,64}}"'
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
        kdu_compress_path=KDU_COMPRESS,
        input_path=source_path,
        output_path=dest_path,
        image_mode=image_modes.get(image_mode)
    )
    _run_kdu_command(kdu_compress_command, compress_env)


def kdu_expand_to_image(filepath: pathlib.Path) -> Image:
    """ Uses the kdu_expand command to decompress a JPEG2000 image to a PIL
        Image.
        #TODO - is `-reduce` required in kdu_expand call?
        """

    kdu_expand_template = '{kdu_expand_path} -i {input_path} -o {output_path} -quiet -num_threads 4'

    expand_env = {
        'LD_LIBRARY_PATH': KDU_LIB,
        'PATH': KDU_EXPAND
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        logger.debug('Created tmpdir: %s', tmpdir)
        output_file = pathlib.Path(tmpdir) / filepath.with_suffix('.bmp').name
        logger.debug('Temporary output path: %s', output_file)
        kdu_expand_command = kdu_expand_template.format(
            kdu_expand_path=KDU_EXPAND,
            input_path=filepath,
            output_path=output_file
        )
        _run_kdu_command(kdu_expand_command, expand_env)
        logger.debug('%s: Opening file with PIL', output_file)
        return Image.open(output_file)
