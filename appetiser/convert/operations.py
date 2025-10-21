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


def _parse_iiif_size_str(
    iiif_size_str: str, src_width: int, src_height: int
) -> tuple[(int | None), (int | None)]:
    pattern_match = IIIF_SIZE_STR_PATTERN.match(iiif_size_str)
    if not pattern_match:
        raise ValueError(f"Invalid IIIF Size string: {iiif_size_str=}")
    match_groups = pattern_match.groupdict()
    logger.debug(f"Parsing: {iiif_size_str=}")
    logger.debug(f"Source image size: {src_width}, {src_height}")
    # iiif_size_str is like f"!{img_width},{img_height}"
    # !w,h
    # The extracted region is scaled so that the width and height of the returned image are not greater than w and h, while maintaining the aspect ratio.
    # The returned image must be as large as possible but not larger than the extracted region, w or h, or server-imposed limits.
    if match_groups["img_width"] and match_groups["img_height"]:
        logger.debug("Match like `!w,h`")
        img_width = int(match_groups["img_width"])
        img_height = int(match_groups["img_height"])
        logger.debug(f"Matched: {img_width=} {img_height=}")
        if img_width >= src_width and img_height >= src_height:
            width = None
            height = None
        else:
            if src_width >= src_height:
                width = img_width
                height = None
            else:
                width = None
                height = img_height
    # iiif_size_str is like f"^{upscale_width},{upscale_height}"
    # ^w,h
    # The width and height of the returned image are exactly w and h.
    # The aspect ratio of the returned image may be significantly different than the extracted region, resulting in a distorted image.
    # If w and/or h are greater than the corresponding pixel dimensions of the extracted region, the extracted region is upscaled.
    elif match_groups["upscale_width"] and match_groups["upscale_height"]:
        logger.debug("Match like `^w,h`")
        width = int(match_groups["upscale_width"])
        height = int(match_groups["upscale_height"])
        logger.debug(f"Matched: {width=} {height=}")
    # iiif_size_str is like f"{width},{height}"
    # w,h
    # The width and height of the returned image are exactly w and h.
    # The aspect ratio of the returned image may be significantly different than the extracted region, resulting in a distorted image.
    # The values of w and h must not be greater than the corresponding pixel dimensions of the extracted region.
    elif match_groups["width"] and match_groups["height"]:
        logger.debug("Match like `w,h`")
        width = int(match_groups["width"])
        height = int(match_groups["height"])
        logger.debug(f"Matched: {width=} {height=}")
        if width >= src_width and height >= src_height:
            width = None
            height = None
        elif width >= src_width:
            width = src_width
        elif height >= src_height:
            height = src_height
    # iiif_size_str is like f"^{upscale_just_width},"
    # ^w,
    # The extracted region should be scaled so that the width of the returned image is exactly equal to w.
    # If w is greater than the pixel width of the extracted region, the extracted region is upscaled.
    elif match_groups["upscale_just_width"]:
        logger.debug("Match like `^w,`")
        width = int(match_groups["upscale_just_width"])
        logger.debug(f"Matched: {width=}")
        height = None
    # iiif_size_str is like f"{just_width},"
    # w,
    # The extracted region should be scaled so that the width of the returned image is exactly equal to w.
    # The value of w must not be greater than the width of the extracted region.
    elif match_groups["just_width"]:
        logger.debug("Match like `w,`")
        just_width = int(match_groups["just_width"])
        logger.debug(f"Matched: {just_width=}")
        width = just_width
        if just_width >= src_width:
            width = None
        height = None
    # iiif_size_str is like f"^,{upscale_just_height}"
    # ^,h
    # The extracted region should be scaled so that the height of the returned image is exactly equal to h.
    # If h is greater than the pixel height of the extracted region, the extracted region is upscaled.
    elif match_groups["upscale_just_height"]:
        logger.debug("Match like `^,h`")
        width = None
        height = int(match_groups["upscale_just_height"])
        logger.debug(f"Matched: {height=}")
    # iiif_size_str is like f",{just_height}"
    # ,h
    # The extracted region should be scaled so that the height of the returned image is exactly equal to h.
    # The value of h must not be greater than the height of the extracted region.
    elif match_groups["just_height"]:
        logger.debug("Match like `,h`")
        width = None
        just_height = int(match_groups["just_height"])
        logger.debug(f"Matched: {just_height=}")
        height = just_height
        if just_height >= src_height:
            height = None
    else:
        raise ValueError(f"Invalid IIIF Size string: {iiif_size_str=}")

    logger.debug(f"Parsed image size: ({height=}, {width=})")
    return width, height


def _calculate_thumb_info(
    iiif_size_str: str, src_width: int, src_height: int, thumb_dir: Path, file_name: str
) -> ThumbInfo | None:

    req_width, req_height = _parse_iiif_size_str(
        iiif_size_str=iiif_size_str, src_width=src_width, src_height=src_height
    )
    if req_width or req_height:
        scaled_width, scaled_height = scale_dimensions_to_fit(
            src_width, src_height, req_width, req_height
        )
        dest_path = thumb_dir / f"{file_name}_{scaled_width}_{scaled_height}.jpg"

        return ThumbInfo(
            path=dest_path,
            width=scaled_width,
            height=scaled_height,
        )

    else:
        return None


def create_thumbnails(
    config: ConvertConfig,
    source: Path,
    thumb_iiif_size: List[str],
    thumb_dir: Path,
):
    """Manages the creation of derivatives (only thumbnails at present) for a given image file,
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

    calculated_thumb_info = list(
        filter(
            None,
            [
                _calculate_thumb_info(
                    iiif_size_str=iiif_size_str,
                    src_width=src_img.width,
                    src_height=src_img.height,
                    thumb_dir=thumb_dir,
                    file_name=source.stem,
                )
                for iiif_size_str in thumb_iiif_size
            ],
        )
    )
    # Deduplicate using the thumb path as a unique key
    calculated_thumb_info = {
        calc_thumb_info.path: calc_thumb_info
        for calc_thumb_info in calculated_thumb_info
    }
    calculated_thumb_info = calculated_thumb_info.values()

    for calc_thumb_info in sorted(
        calculated_thumb_info, reverse=True, key=lambda x: x.width
    ):
        img = resize_and_save_img(
            img=src_img,
            width=calc_thumb_info.width,
            height=calc_thumb_info.height,
            dest_path=calc_thumb_info.path,
            config=config
        )
        thumbnail_info.append(
            ThumbInfo(
                path=calc_thumb_info.path,
                width=img.width,
                height=img.height,
            )
        )
    return src_img_info, thumbnail_info
