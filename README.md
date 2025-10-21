# appetiser

Replacement for jp2iser/tizer. Converts various image resources into JPEG2000 and a collection of thumbnails.


## Dependencies

### Kakadu

Appetiser is dependent on being able to access the compiled binaries for Kakadu as a tarball. In production it is expected that this will be an S3 file location that appetiser has access to at run-time, set with the environment variable: 

```sh
KDU_BINARIES=s3://bucket/path-/to/kdu/binaries.tar
```

This is downloaded to the location `/kdu_src/kdu.tar` within the running container. convert

For local development using docker compose, the `./local_data/kdu_src` directory is mapped to `/kdu_src` within the appetiser container. A copy of the Kakadu binaries should be placed in the `./local_data/kdu_src/` directory, and symlinked to `./local_data/kdu_src/kdu.tar` 

### Python 
Python dependencies for appetiser are managed using [uv](https://docs.astral.sh/uv/). This is the case both for app dependencies, that are installed by uv in the docker image, and development dependencies, that are used for testing and tooling. 

Development and testing dependencies should be added using the `--dev` flag, e.g. 

```sh
uv add --dev httpx
```

Although the app is containerised, it will be necessary to install the project dependencies for local development via:
```sh 
uv sync
```

### OS

Pillow has a number of OS level dependencies for dealing with various image formats that are installed in the Docker image. As we're installing Pillow through `uv` (previously `pip`) rather than `apt` this is required to ensure support for the required image formats. These seem to correspond with the [External libraries](https://pillow.readthedocs.io/en/stable/installation/building-from-source.html) in the Pillow docs.

## Running locally

A [docker-compose.yml](./docker-compose.yml) file is provided for local development. This contains a number of volume mappings for local files, so the following must exist in the local directory: 

- `./local_data/kdu_src`: Directory containing the Kakadu binaries as described [above](#kakadu). gitingored.
- `./local_data/output`: Output directory mapped to `/test_output` and used in API examples and tests. gitignored.  

## Running tests 

Integration tests can be found in [./tests](./tests) and should be run with: 
```sh 
uv run pytest
```

These tests are dependent on `pytest-docker`, and use the [./tests/docker-compose.test.yml](./tests/docker-compose.test.yml) file. 


## API Documentation 

OpenAPI docs for the appetiser API can be found at [http://localhost:8000/docs](http://localhost:8000/docs) on a locally running instance of appetiser. These provide documentation and examples for the `convert/` endpoint, along with expected types. 

## Customising

The following environment variables can be used to configure the service

| EnvVar         | Description                                     | Default |
| -------------- | ----------------------------------------------- | ------- |
| `JPEG_QUALITY` | Integer, 0-100, controls thumbnail jpeg quality | 90      |