# appetiser

Replacement for jp2iser/tizer. Converts various image resources into JPEG2000 and a collection of thumbnails.

## Getting Started

The easiest way to get this running is using Docker.

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
    "destination": "/opt/appetiser/out/the_converted.jp2",
    "thumbDir": "/opt/appetiser/out/thumbnails/"
}
```  
