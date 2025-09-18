import logging
from .operations import (
    convert_image_to_jp2,
    create_thumbnails,
)

from .models import (
    ConvertOperation,
    ConvertRequest,
    ConvertResponse,
)
from .config import ConvertConfig

logger = logging.getLogger(__name__)


def convert_image(config: ConvertConfig, request: ConvertRequest) -> dict:
    logger.debug("Running")
    ingested_path, image_info = convert_image_to_jp2(
        config=config,
        source=request.source,
        destination=request.destination,
        optimisation=request.optimisation,
    )
    response_kwargs = {
        "jp2": ingested_path,
        "width": image_info.get("width"),
        "height": image_info.get("height"),
    }
    return response_kwargs


def create_derivatives(config: ConvertConfig, request: ConvertRequest) -> dict:
    image_info, thumbnail_info = create_thumbnails(
        config=config,
        source=request.source,
        thumb_iiif_size=request.thumbIIIFSizes,
        thumb_dir=request.thumbDir,
    )
    response_kwargs = {
        "width": image_info.get("width"),
        "height": image_info.get("height"),
        "thumbs": thumbnail_info,
    }
    return response_kwargs


def ingest(config: ConvertConfig, request: ConvertRequest) -> dict:
    ingested_path, image_info = convert_image_to_jp2(
        config=config,
        source=request.source,
        destination=request.destination,
        optimisation=request.optimisation,
    )
    _, derivative_info = create_thumbnails(
        config=config,
        source=ingested_path,
        thumb_iiif_size=request.thumbIIIFSizes,
        thumb_dir=request.thumbDir,
    )
    response_kwargs = {
        "jp2": ingested_path,
        "width": image_info.get("width"),
        "height": image_info.get("height"),
        "thumbs": derivative_info,
    }

    return response_kwargs


CONVERT_OPERATION_MAPPING = {
    ConvertOperation.ingest: ingest,
    ConvertOperation.image_only: convert_image,
    ConvertOperation.derivatives_only: create_derivatives,
}
