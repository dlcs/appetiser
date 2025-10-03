import pytest
import tempfile
import pathlib
import collections
from collections.abc import (
    Generator,
)

from .utils import (
    is_responsive_404,
)

SharedHostContainerDirectory = collections.namedtuple(
    "SharedHostContainerDirectory", ["host_path", "container_path"]
)


@pytest.fixture(scope="session")
def tests_dir():
    return pathlib.Path(__file__).resolve().parent


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return pathlib.Path(__file__).resolve().parent / "docker-compose.test.yml"


@pytest.fixture(scope="session")
def appetiser_service(docker_ip, docker_services):
    """
    Ensure that Django service is up and responsive.
    """

    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("appetiser", 8000)
    url = "http://{}:{}".format(docker_ip, port)
    url404 = f"{url}/missing"
    docker_services.wait_until_responsive(
        timeout=300.0, pause=0.1, check=lambda: is_responsive_404(url404)
    )
    return url


@pytest.fixture(scope="session")
def fixtures_dir(tests_dir) -> SharedHostContainerDirectory:
    """Relies on mounting the local fixtures directory to the `/test_fixtures` location
    in the `volumes` block of the docker-compose.test.yml file.
    """
    return SharedHostContainerDirectory(
        host_path=(tests_dir / "fixtures"),
        container_path=pathlib.Path("/test_fixtures"),
    )


@pytest.fixture(scope="session")
def output_dir(tests_dir) -> Generator[SharedHostContainerDirectory, None, None]:
    """Relies on mounting a local output directory to the `/test_output` location
    in the `volumes` block of the docker-compose.test.yml file.
    """
    with tempfile.TemporaryDirectory(dir=(tests_dir / "output")) as tmpdir:
        host_path = pathlib.Path(tmpdir)
        yield SharedHostContainerDirectory(
            host_path=host_path,
            container_path=pathlib.Path(f"/test_output/{host_path.name}"),
        )
