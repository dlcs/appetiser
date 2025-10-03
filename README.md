# appetiser

Replacement for jp2iser/tizer. Converts various image resources into JPEG2000 and a collection of thumbnails.

## Dependencies

### Kakadu

Appetiser is dependent on being able to access the compiled binaries for Kakadu as a tarball. In production it is expected that this will be an S3 file location that appetiser has access to at run-time, set with the environment variable: 
```sh
KDU_BINARIES=s3://bucket/path-/to/kdu/binaries.tar
```

### Python 
Python dependencies for appetiser are managed using [uv](https://docs.astral.sh/uv/). 

Development and testing dependencies should be added using the `--dev` flag, e.g. 

```sh
uv add --dev httpx
```

### OS 
## Running locally

A [docker-compose.yml](./docker-compose.yml) file is provided for local development. 
```bash
# build
docker build -t appetiser:latest .

# run
docker run -it --rm -p 5080:80 appetiser:latest
```

Appetiser needs access to Kakadu binaries. The default location of these binaries is specified by the `KAKADU_APPS_LOCATION` environment variable. Relevant AWS credentials will need to be passed to the docker container.

You will also need a volume mount for reading/writing images. Files are not passed as part of the request, instead a `source` parameter points to the file on disk.

e.g.
```bash
docker run -it --rm -p 5080:80 \
-e KAKADU_APPS_LOCATION=s3://my-s3-bucket/kdu77-apps.tar.gz \
-e AWS_ACCESS_KEY_ID=mykey \
-e AWS_SECRET_ACCESS_KEY=mysecretkey \
-v /path/to/scratch:/scratch \
appetiser:latest
```

### Docker Compose

There is a docker-compose file to ease running above, see .env.dist for example .env file.

```bash
docker-compose up
```

## Converting an Image

Make a POST to `/convert` to start conversion process. The source image must be in a folder location that is accessible to the appetiser application.

Sample payload (all folder locations are relative to `/opt/appetiser/`):

```json
{
    "imageId": "test-appetiser",
    "jobId": "test-appetiser_job",
    "source": "/scratch/test-image.jpg",
    "thumbSizes": [ 30, 100, 400 ],
    "operation": "ingest",
    "optimisation": "kdu_med",
    "origin": "my_origin",
    "destination": "/scratch/out/the_converted.jp2",
    "thumbDir": "/scratch/out/thumbnails/"
}
```

> Note that the destination _must_ end in "jp2" or kdu_compress call will fail.
