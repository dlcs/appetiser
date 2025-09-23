import logging
import traceback
import fastapi
from typing import Annotated
from functools import lru_cache

from .convert import (
    ConvertRequest,
    ConvertResponse,
    CONVERT_OPERATION_MAPPING,
    ConvertConfig,
)


logging.basicConfig(format="%(levelname)s - %(name)s: %(message)s", level=logging.DEBUG)

logger = logging.getLogger(__name__)
app = fastapi.FastAPI(title="appetiser")


@lru_cache
def get_convert_config():
    return ConvertConfig()


@app.get("/ping")
def ping():
    """Healthcheck endpoint."""
    logger.debug("ping endpoint accessed.")
    return {"status": "working"}


@app.get("/config")
def appetiser_config(
    convert_config: Annotated[ConvertConfig, fastapi.Depends(get_convert_config)],
) -> ConvertConfig:
    """Displays the env variables used for app configuration."""
    logger.debug("config endpoint accessed.")
    return convert_config


@app.post("/convert")
def convert(
    convert_config: Annotated[ConvertConfig, fastapi.Depends(get_convert_config)],
    convert_request: Annotated[
        ConvertRequest,
        fastapi.Body(
            openapi_examples={
                "ingest": {
                    "summary": "Ingest operation",
                    "description": "Ingest of a jpg, creating a jp2 and thumbnails.",
                    "value": {
                        "imageId": "ingest_example_image",
                        "jobId": "ingest_example_image_job",
                        "origin": "ingest_example_image_origin",
                        "source": "/test_fixtures/Ms_W_102/fol_73r_detail.jpg",
                        "destination": "/test_output/fol_73r_detail.jp2",
                        "thumbIIIFSizes": ["100,", ",400", "!1000,1000"],
                        "thumbDir": "/test_output/",
                        "operation": "ingest",
                        "optimisation": "kdu_med",
                    },
                },
                "image-only": {
                    "summary": "Image-only operation",
                    "description": "Ingest of a tiff, creating a jp2, using the `kdu_max` optimisation.",
                    "value": {
                        "imageId": "image_only_example_image",
                        "jobId": "image_only_example_image_job",
                        "origin": "image_only_example_image_origin",
                        "source": "/test_fixtures/Ms_W_102/fol_73v_detail.tiff",
                        "destination": "/test_output/fol_73v_detail.tiff",
                        "operation": "image-only",
                        "optimisation": "kdu_max",
                    },
                },
                "derivatives-only": {
                    "summary": "Derivatives-only operation",
                    "description": "Ingest of a jpg, creating a thumbnails.",
                    "value": {
                        "imageId": "derivatives_only_example_image",
                        "jobId": "derivatives_only_example_image_job",
                        "origin": "derivatives_only_example_image_origin",
                        "source": "/test_fixtures/Ms_W_102/fol_73r_detail.jpg",
                        "thumbIIIFSizes": [
                            "100,",
                            "250,",
                            ",500",
                            "!1000,1000",
                            "!2000,2000",
                        ],
                        "thumbDir": "/test_output/",
                        "operation": "derivatives-only",
                    },
                },
            }
        ),
    ],
) -> ConvertResponse:
    logger.debug(f"convert endpoint request: {convert_request=}")
    try:

        operation_func = CONVERT_OPERATION_MAPPING[convert_request.operation]
        logger.info(f"Mapped {convert_request.operation=} to {operation_func}")
        response_kwargs = operation_func(config=convert_config, request=convert_request)

        copied_kwargs = {
            "jobId": convert_request.jobId,
            "origin": convert_request.origin,
            "imageId": convert_request.imageId,
        }
        if convert_request.optimisation:
            copied_kwargs["optimisation"] = convert_request.optimisation

        response = ConvertResponse(
            **copied_kwargs,
            **response_kwargs,
        )
        return response

    except fastapi.HTTPException as e:
        logger.error(e)
        raise e

    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(e)
        raise fastapi.HTTPException(
            status_code=500,
            detail=str(e),
        )
