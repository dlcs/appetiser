import re
from pydantic import (
    BaseModel,
    StringConstraints,
    FilePath,
    DirectoryPath,
)
from enum import Enum
from pathlib import Path
from typing import (
    Annotated,
    List,
)

IIIF_SIZE_STR_PATTERN = re.compile(
    # r"^!?(?P<width>\d+),(?P<height>\d+)|(?P<just_width>\d+),|,(?P<just_height>\d+)$"
    # r"^!(?P<img_width>\d+),(?P<img_height>\d+)|\^(?P<upscale_width>\d+),(?P<upscale_height>\d+)|(?P<width>\d+),(?P<height>\d+)|\^(?P<upscale_just_width>\d+),|(?P<just_width>\d+),|\^,(?P<upscale_just_height>\d+)|,(?P<just_height>\d+)$"
    r"^!(?P<img_width>\d+),(?P<img_height>\d+)$|^\^(?P<upscale_width>\d+),(?P<upscale_height>\d+)$|^(?P<width>\d+),(?P<height>\d+)$|^\^(?P<upscale_just_width>\d+),$|^(?P<just_width>\d+),$|^\^,(?P<upscale_just_height>\d+)$|^,(?P<just_height>\d+)$"
)


# Using an enum as the source of truth for the function mapping ensures that invalid operations
# are caught at the stage of model validation.
class ConvertOperation(str, Enum):
    ingest = "ingest"
    image_only = "image-only"
    derivatives_only = "derivatives-only"


class KDUCompressOptimisation(str, Enum):
    kdu_low = "kdu_low"
    kdu_med = "kdu_med"
    kdu_med_layers = "kdu_med_layers"
    kdu_high = "kdu_high"
    kdu_max = "kdu_max"


class ThumbInfo(BaseModel):
    path: Path
    width: int
    height: int


class ConvertRequest(BaseModel):
    jobId: str
    imageId: str
    origin: str
    source: FilePath
    operation: ConvertOperation
    destination: Path | None = None
    thumbDir: DirectoryPath | None = None
    thumbIIIFSizes: List[
        Annotated[str, StringConstraints(pattern=IIIF_SIZE_STR_PATTERN)]
    ] = []
    optimisation: KDUCompressOptimisation | None = None


class ConvertResponse(BaseModel):
    jobId: str
    imageId: str
    origin: str
    optimisation: KDUCompressOptimisation | None = None
    jp2: FilePath = ""
    height: int
    width: int
    thumbs: List[ThumbInfo] = []
