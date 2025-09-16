FROM python:3.13-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.8.13 /uv /uvx /bin/

# ENV KAKADU_APPS_LOCATION s3://dlcs-dlcservices-bootstrap-objects/kdu77-apps.tar.gz
ENV APPETISER_DIR /opt/appetiser
ENV TMPDIR $APPETISER_DIR/tmp
ENV OUTPUT_DIR $APPETISER_DIR/out/
ENV HTTP_TIMEOUT 60

RUN apt-get update -y && apt-get install -y cmake \
  netpbm \
  ghostscript \
  libffi-dev \
  libjpeg-turbo-progs \
  libtiff5-dev \
  libjpeg62-turbo-dev \
  zlib1g-dev \
  libfreetype6-dev \
  liblcms2-dev \
  libwebp-dev \
  tcl8.6-dev \
  tk8.6-dev \
  python3-tk \
  libharfbuzz-dev \
  libfribidi-dev

COPY ./appetiser/ $APPETISER_DIR/appetiser/
COPY ./pyproject.toml $APPETISER_DIR
COPY ./uv.lock $APPETISER_DIR
COPY ./run_appetiser.sh $APPETISER_DIR

RUN ls $APPETISER_DIR
RUN chmod +x $APPETISER_DIR/run_appetiser.sh

LABEL org.opencontainers.image.source=https://github.com/dlcs/appetiser

RUN mkdir $TMPDIR $OUTPUT_DIR
WORKDIR $APPETISER_DIR
RUN uv sync --locked

EXPOSE 80
CMD $APPETISER_DIR/run_appetiser.sh
