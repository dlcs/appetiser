import logging
import os
import pathlib

from .kdu import (
    kdu_compress, 
    kdu_expand_to_image,
)

from .openjpeg import (
    openjpeg_compress,
    openjpeg_expand_to_image,        
)

logger = logging.getLogger(__name__)


class Processor(object):

    cmd_env_var_map = {
            'kdu': {
                'compress': [
                    'KDU_COMPRESS', 
                    'KDU_LIB', 
                    ]
                'expand': [
                    'KDU_EXPAND',
                    'KDU_LIB', 
                    ]
                },
            'opj': 
                'compress': [
                    'OPJ_COMPRESS', 
                    ],
                'decompress': [
                    'OPJ_DECOMPRESS', 
                    ],

    def __init__():
        for program, commands in cmd_env_var_map.items():
            for command, env_vars in commands.items():
                

    def _check_presence_of_var(var_name):
        env_var = os.environ.get(env_var_name)
        if not env_var
    path = pathlib.Path(env_var)
    if not path.exists():
                

            



    def compress_image_to_jp2():
        pass

    def expand_jp2_to_image():
        pass

def _determine_available_processors
KDU_COMPRESS = _get_path_from_env_var('KDU_COMPRESS')
KDU_EXPAND = _get_path_from_env_var('KDU_EXPAND')
KDU_LIB = _get_path_from_env_var('KDU_LIB')



def _parse_processor_name(optimisation: str) -> str:
    return optimisation.split(_)[0]

    


def expand_to_image():
    
    pass

def compress():
    pass
