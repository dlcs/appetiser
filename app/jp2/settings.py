import logging
import os
import pathlib
import collections

logger = logging.getLogger(__name__)

def _get_path_from_env_var(env_var_name: str) -> pathlib.Path:
    """ Retrieve a path from an environment variable, checking both that it
        and the file or directory it points to are present.
        """
    env_var = os.environ.get(env_var_name)
    if not env_var:
        raise NameError(
            f'{env_var_name} is not present as an environment variable')
    path = pathlib.Path(env_var)
    if not path.exists():
        raise FileNotFoundError(
            f'{env_var} is not an existing file or directory')
    logger.info('%s has valid path %s', env_var_name, env_var)
    return path

def _get_related_env_vars(*env_var_names: str):
    env_vars = []
    for env_var_name in env_var_names: 
        try: 
            path = _get_path_from_env_var(env_var_name)
        except Exception e: 
            logger.error(e)
            path = None
        env_vars.append(path)
    if not all(env_vars): 
        logger.info('Missing rel{}')

    return env_vars

OUTPUT_DIR = _get_path_from_env_var('OUTPUT_DIR')

KDU_LIB, KDU_EXPAND, KDU_COMPRESS = _get_related_env_vars('KDU_LIB', 'KDU_COMPRESS', 'KDU_EXPAND')
KDU_AVAILABLE = all(KDU_LIB, KDU_EXPAND, KDU_COMPRESS)
OPJ_COMPRESS, OPJ_DECOMPRESS = _get_related_env_vars('OPJ_COMPRESS', 'OPJ_DECOMPRESS')
OPJ_AVAILABLE = all(OPJ_COMPRESS, OPJ_DECOMPRESS)
