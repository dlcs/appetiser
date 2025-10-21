from pydantic import conint
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class ConvertConfig(BaseSettings):
    KDU_COMPRESS: Path
    KDU_EXPAND: Path
    KDU_LIB: Path
    OUTPUT_DIR: Path
    JPEG_QUALITY: conint(ge=0, le=100) = 90
    model_config = SettingsConfigDict(case_sensitive=True)
