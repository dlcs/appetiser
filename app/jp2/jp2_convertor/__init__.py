import logging
import os
import pathlib

from .kdu import (
    kdu_compress, 
    kdu_expand_to_image,
)

from .openjpeg import (
    openjpeg_compress,
    openjpeg_decompress,        
)

from settings import (
        KDU_AVAILABLE, 
        OPJ_AVAILABLE, 
) 

logger = logging.getLogger(__name__)


def func_from_optimisation(function_options: dict, optimisation: str):
    func_availability = {
            'kdu': KDU_AVAILABLE, 
            'opj': OPJ_AVAILABLE, 
            }
    key = optimisation.split('_')[0]
    if (function := function_options.get(key)): 
        if func_availability.get(key): 
            logger.info('')
            return function 
        else:
            logger.error('')
            return "this backend not available"
    else: 
        logger.error('')
        return "don't know about this backend"


def compress(source_path: pathlib.Path, dest_path: pathlib.Path, optimisation: str, image_mode: str) -> pathlib.Path:
    compress_backend_options = {
            'kdu': kdu_compress, 
            'opj': openjpeg_compress, 
            }
    compress_function = func_from_optimisation(compress_backend_options, optimisation)
    return compress_function(source_path, dest_path, optimisation, image_mode)

            
def expand_to_image(filepath: pathlib.Path) -> Image:
    expand_backend_options = {
            'kdu': kdu_expand_to_image, 
            'opj': openjpeg_decompress, 
            }
    expand_function = func_from_optimisation(compress_backend_options, optimisation)
