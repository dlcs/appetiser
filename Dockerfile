FROM python:3.13-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.8.13 /uv /uvx /bin/

ENV APPETISER_DIR=/opt/appetiser
ENV TMPDIR=$APPETISER_DIR/tmp
ENV OUTPUT_DIR=$APPETISER_DIR/out/

RUN apt-get update -y && apt-get install -y \
  cmake \
  netpbm \
  ghostscript \
  libgs10 \
  libgs10-common \
  libffi-dev \
  libjpeg-turbo-progs \
  libtiff5-dev \
  libjpeg62-turbo-dev \
  zlib1g-dev \
  liblcms2-dev \
  libwebp-dev \
  tcl8.6-dev \
  tk8.6-dev \
  python3-tk \
  libharfbuzz-dev \
  libfribidi-dev \
  && rm -rf /var/lib/apt/lists/*

COPY ./appetiser/ $APPETISER_DIR/appetiser/
COPY ./pyproject.toml $APPETISER_DIR
COPY ./uv.lock $APPETISER_DIR
COPY ./run_appetiser.sh $APPETISER_DIR

RUN chmod +x $APPETISER_DIR/run_appetiser.sh

LABEL org.opencontainers.image.source=https://github.com/dlcs/appetiser

RUN mkdir $TMPDIR $OUTPUT_DIR
WORKDIR $APPETISER_DIR
RUN uv sync --locked --no-dev

CMD ["./run_appetiser.sh"]
