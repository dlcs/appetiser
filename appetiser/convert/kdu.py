import logging

import subprocess
import tempfile

from pathlib import Path
from PIL import (
    Image,
)
from PIL.Image import Image as PILImage

from .models import KDUCompressOptimisation
from .config import ConvertConfig

logger = logging.getLogger(__name__)

# Allows images of any size to be processed without raising a
# warning or an error.
Image.MAX_IMAGE_PIXELS = None

IMAGE_MODES = {
    "L": "-no_palette",
    "1": "-no_palette",
    "I;16B": "-no_palette",
    "RGB": "-jp2_space sRGB",
    "RGBA": "-jp2_space sRGB -jp2_alpha",
}


KDU_COMPRESS_TEMPLATES = {
    KDUCompressOptimisation.kdu_low: '{kdu_compress_path} -i {input_path} -o {output_path} Clevels=7 "Cblk={{64,64}}"'
    ' "Cuse_sop=yes" {image_mode} "ORGgen_plt=yes" "ORGtparts=R" "Corder=RPCL" -rate 0.5'
    ' "Cprecincts={{256,256}},{{256,256}},{{256,256}},{{128,128}},{{128,128}},{{64,64}},'
    '{{64,64}},{{32,32}},{{16,16}}"',
    KDUCompressOptimisation.kdu_med: '{kdu_compress_path} -i {input_path} -o {output_path} Clevels=7 "Cblk={{64,64}}"'
    ' "Cuse_sop=yes" {image_mode} "ORGgen_plt=yes" "ORGtparts=R" "Corder=RPCL" -rate 2'
    ' "Cprecincts={{256,256}},{{256,256}},{{256,256}},{{128,128}},{{128,128}},{{64,64}},'
    '{{64,64}},{{32,32}},{{16,16}}"',
    KDUCompressOptimisation.kdu_med_layers: '{kdu_compress_path} -i {input_path} -o {output_path} Clevels=7 "Cblk={{64,64}}"'
    ' "Cuse_sop=yes" {image_mode} "ORGgen_plt=yes" "ORGtparts=R" "Corder=RPCL" Clayers=6 -rate 2'
    ' "Cprecincts={{256,256}},{{256,256}},{{256,256}},{{128,128}},{{128,128}},{{64,64}},'
    '{{64,64}},{{32,32}},{{16,16}}"',
    KDUCompressOptimisation.kdu_high: '{kdu_compress_path} -i {input_path} -o {output_path} Clevels=7 "Cblk={{64,64}}"'
    ' "Cuse_sop=yes" {image_mode} "ORGgen_plt=yes" "ORGtparts=R" "Corder=RPCL" -rate 4'
    ' "Cprecincts={{256,256}},{{256,256}},{{256,256}},{{128,128}},{{128,128}},{{64,64}},'
    '{{64,64}},{{32,32}},{{16,16}}"',
    KDUCompressOptimisation.kdu_max: '{kdu_compress_path} -i {input_path} -o {output_path} Clevels=7 "Cblk={{64,64}}"'
    ' "Cuse_sop=yes" {image_mode} "ORGgen_plt=yes" "ORGtparts=R" "Corder=RPCL" -rate -'
    ' "Cprecincts={{256,256}},{{256,256}},{{256,256}},{{128,128}},{{128,128}},{{64,64}},'
    '{{64,64}},{{32,32}},{{16,16}}"',
}


def _run_kdu_command(kdu_command: str, env: dict):
    try:
        logger.debug("Running command: %s", kdu_command)
        subprocess.run(
            kdu_command, env=env, shell=True, check=True, capture_output=True
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"kdu command failed. Full output:{e.output}")
        raise e


def kdu_compress(
    config: ConvertConfig,
    source_path: Path,
    dest_path: Path,
    optimisation: KDUCompressOptimisation,
    image_mode: str,
) -> Path:
    """Uses the kdu_compress command to convert a source image
    (in BMP, RAW, PBM, PGM, PPM or TIFF formats) to a JPEG2000.
    """

    if image_mode not in IMAGE_MODES:
        raise ValueError(
            f"image_mode '{image_mode}' is not in known list for kdu_compress"
        )

    compress_env = {"LD_LIBRARY_PATH": config.KDU_LIB, "PATH": config.KDU_COMPRESS}

    kdu_compress_template = KDU_COMPRESS_TEMPLATES.get(
        optimisation, KDU_COMPRESS_TEMPLATES[KDUCompressOptimisation.kdu_med]
    )

    kdu_compress_command = kdu_compress_template.format(
        kdu_compress_path=config.KDU_COMPRESS,
        input_path=source_path,
        output_path=dest_path,
        image_mode=IMAGE_MODES.get(image_mode),
    )
    _run_kdu_command(kdu_compress_command, compress_env)
    return dest_path


def kdu_expand_to_image(config: ConvertConfig, source_path: Path) -> PILImage:
    """Uses the kdu_expand command to decompress a JPEG2000 image to a PIL
    Image.
    """

    kdu_expand_template = (
        "{kdu_expand_path} -i {input_path} -o {output_path} -quiet -num_threads 4"
    )

    expand_env = {"LD_LIBRARY_PATH": config.KDU_LIB, "PATH": config.KDU_EXPAND}

    with tempfile.TemporaryDirectory() as tmpdir:
        logger.debug(f"Created temporary directory: {tmpdir=}")
        output_file = Path(tmpdir) / source_path.with_suffix(".bmp").name
        logger.debug(f"Temporary output path: {output_file=}")
        kdu_expand_command = kdu_expand_template.format(
            kdu_expand_path=config.KDU_EXPAND,
            input_path=source_path,
            output_path=output_file,
        )
        _run_kdu_command(kdu_expand_command, expand_env)
        logger.debug(f"Opening file with PIL: {output_file=}")
        return Image.open(output_file)
