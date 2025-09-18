import subprocess
import logging
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
    """Displays the env variables used for configuration."""
    logger.debug("config endpoint accessed.")
    return convert_config


@app.post("/convert")
def convert(
    convert_config: Annotated[ConvertConfig, fastapi.Depends(get_convert_config)],
    convert_request: Annotated[
        ConvertRequest,
        fastapi.Body(
            openapi_examples={
                "convert": {
                    "summary": "Basic convert operation",
                    "description e": "A simple example operation",
                    "value": {
                        "imageId": "example_img.jpg",
                        "jobId": "example_img_job",
                        "origin": "example_img_origin",
                        "source": "/path/to/example_img.jpg",
                        "destination": "/dest/path/example_img.jp2",
                        "thumbIIIFSize": ["100,100", "400,400", "1000,1000"],
                        "thumbDir": "/dest/path/",
                        "operation": "ingest",
                        "optimisation": "kdu_med",
                    },
                }
            }
        ),
    ],
) -> ConvertResponse:
    logger.debug(f"convert endpoint request: {convert_request=}")
    try:

        operation_func = CONVERT_OPERATION_MAPPING[convert_request.operation]
        logger.info(f"Mapped {convert_request.operation=} to {operation_func}")
        response_kwargs = operation_func(config=convert_config, request=convert_request)
        response = ConvertResponse(
            jobId=convert_request.jobId,
            origin=convert_request.origin,
            optimisation=convert_request.optimisation,
            imageId=convert_request.imageId,
            **response_kwargs,
        )

        return response

    except fastapi.HTTPException as e:
        logger.error(e)
        raise e

    except Exception as e:
        logger.error(e)
        raise fastapi.HTTPException(
            status_code=500,
            detail=str(e),
        )
