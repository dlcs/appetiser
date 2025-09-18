import logging
import shutil
from enum import Enum
from pathlib import Path
from typing import List

from .kdu import (
    KDUCompressOptimisation,
    kdu_compress,
    kdu_expand_to_image,
)
from .image import (
    is_tile_optimised_jp2,
    get_img_info,
    prepare_source_file,
    scale_dimensions_to_fit,
    resize_and_save_img,
)
from .models import (
    IIIF_SIZE_STR_PATTERN,
    ThumbInfo,
)


from PIL import (
    Image,
)

from .config import ConvertConfig

logger = logging.getLogger(__name__)


def convert_image_to_jp2(
    config: ConvertConfig,
    source: Path,
    destination: Path,
    optimisation: KDUCompressOptimisation,
) -> tuple[Path, dict]:
    """Manages the initial conversion of the provided source image file to a
    tile optimised JPEG2000 file using the provide kdu optimisation type.
    """
    prepared_source, image_info = prepare_source_file(source)
    if is_tile_optimised_jp2(prepared_source):
        logger.debug("Already a JPEG2000, copying: {source=} -> {destination=}")
        shutil.copy(source, destination)
        return destination, image_info
    else:
        image_mode = image_info.get("mode")
        logger.debug(
            "Converting with colour profile: {prepared_source=}, {image_mode=}"
        )
        logger.debug(
            "%s: Being used for conversion to JPEG2000, with colour mode: %s",
            prepared_source,
            image_mode,
        )
        kdu_compress(
            config=config,
            source_path=prepared_source,
            dest_path=destination,
            optimisation=optimisation,
            image_mode=image_mode,
        )
        return destination, image_info


def _parse_iiif_size_str(iiif_size_str: str) -> tuple[(int | None), (int | None)]:
    pattern_match = IIIF_SIZE_STR_PATTERN.match(iiif_size_str)
    if not pattern_match:
        raise ValueError(f"Invalid IIIF Size string: {iiif_size_str=}")
    match_groups = pattern_match.groupdict()
    if match_groups["width"] and match_groups["height"]:
        width = int(match_groups["width"])
        height = int(match_groups["height"])
    elif match_groups["just_width"]:
        width = int(match_groups["just_width"])
        height = None
    elif match_groups["just_height"]:
        width = None
        height = int(match_groups["just_height"])
    else:
        raise ValueError(f"Invalid IIIF Size string: {iiif_size_str=}")
    return width, height


def _calculate_thumb_info(
    iiif_size_str: str, src_height: int, src_width: int, thumb_dir: Path, file_name: str
) -> ThumbInfo:

    req_width, req_height = _parse_iiif_size_str(iiif_size_str)
    scaled_width, scaled_height = scale_dimensions_to_fit(
        src_width, src_height, req_width, req_height
    )

    dest_path = thumb_dir / f"{file_name}_{scaled_width}_{scaled_height}.jpg"

    return ThumbInfo(
        path=dest_path,
        width=scaled_width,
        height=scaled_height,
    )


def create_thumbnails(
    config: ConvertConfig,
    source: Path,
    thumb_iiif_size: List[str],
    thumb_dir: Path,
):
    """Manages the creation of derivatives (only thumbnails at present) for a given JPEG2000 file,
    returning information about the derivatives and where they're located.
    """
    if source.suffix.lower() == ".jp2":
        logger.debug(f"Converting JP2 image using kdu_expand: {source=}")
        src_img = kdu_expand_to_image(config=config, source_path=source)
    else:
        logger.debug(f"Opening file with PIL: {source=}")
        src_img = Image.open(source)

    src_img_info = {"width": src_img.width, "height": src_img.height}
    thumbnail_info = []

    calculated_thumb_info = [
        _calculate_thumb_info(
            iiif_size_str=iiif_size_str,
            src_height=src_img.height,
            src_width=src_img.width,
            thumb_dir=thumb_dir,
            file_name=source.stem,
        )
        for iiif_size_str in thumb_iiif_size
    ]
    for calc_thumb_info in sorted(
        calculated_thumb_info, reverse=True, key=lambda x: x.width
    ):
        img = resize_and_save_img(
            img=src_img,
            width=calc_thumb_info.width,
            height=calc_thumb_info.height,
            dest_path=calc_thumb_info.path,
        )
        thumbnail_info.append(
            ThumbInfo(
                path=calc_thumb_info.path,
                width=img.width,
                height=img.height,
            )
        )
    return src_img_info, thumbnail_info
