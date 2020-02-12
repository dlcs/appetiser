import logging
import subprocess

logger = logging.getLogger(__name__)


def run_command(command: str, env: dict):
    try:
        logger.debug("Running command: %s", command)
        subprocess.run(command, env=env, shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise e
