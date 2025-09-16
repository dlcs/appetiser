import logging
import os
import pathlib

logger = logging.getLogger(__name__)


def _get_path_from_env_var(env_var_name: str) -> pathlib.Path:
    """ Retrieve a path from an environment variable, checking both that it
        and the file or directory it points to are present.
        """
    env_var = os.environ.get(env_var_name)
    if not env_var:
        raise NameError(
            '{} is not present as an environment variable'.format(env_var_name))
    path = pathlib.Path(env_var)
    if not path.exists():
        raise FileNotFoundError(
            '{} is not an existing file or directory'.format(env_var))
    logger.info('%s has valid path %s', env_var_name, env_var)
    return path


KDU_COMPRESS = _get_path_from_env_var('KDU_COMPRESS')
KDU_EXPAND = _get_path_from_env_var('KDU_EXPAND')
KDU_LIB = _get_path_from_env_var('KDU_LIB')
OUTPUT_DIR = _get_path_from_env_var('OUTPUT_DIR')
