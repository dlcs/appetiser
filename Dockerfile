FROM python:3.13-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.8.13 /uv /uvx /bin/

ENV APPETISER_DIR=/opt/appetiser
ENV TMPDIR=$APPETISER_DIR/tmp
ENV OUTPUT_DIR=$APPETISER_DIR/out/

RUN apt-get update -y && apt-get install -y \
  cmake=3.31.6-2 \
  netpbm=2:11.10.02-1 \
  ghostscript=10.05.1~dfsg-1 \
  libffi-dev=3.4.8-2 \
  libjpeg-turbo-progs=1:2.1.5-4 \
  libtiff5-dev=4.7.0-3 \
  libjpeg62-turbo-dev=1:2.1.5-4 \
  zlib1g-dev=1:1.3.dfsg+really1.3.1-1+b1 \
  #libfreetype6-dev \
  liblcms2-dev=2.16-2 \
  libwebp-dev=1.5.0-0.1 \
  tcl8.6-dev=8.6.16+dfsg-1 \
  tk8.6-dev=8.6.16-1 \
  python3-tk=3.13.5-1\
  libharfbuzz-dev=10.2.0-1+b1 \
  libfribidi-dev=1.0.16-1

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
