FROM python:3.7-slim-stretch

ENV KAKADU_APPS_LOCATION s3://dlcs-dlcservices-bootstrap-objects/kdu77-apps.tar.gz
ENV APPETISER_DIR /opt/appetiser
ENV TMPDIR $APPETISER_DIR/tmp
ENV OUTPUT_DIR $APPETISER_DIR/out/

RUN apt-get update -y && apt-get install -y gcc

#RUN apk add --update --no-cache libc-dev \
#                                gcc \
#                                bash \
#                                # Pillow deps
 #                               jpeg-dev \
#                                zlib-dev \
#                                freetype-dev \
#                                lcms2-dev \
#                                openjpeg-dev \
#                                tiff-dev \
#                                tk-dev \
#                                tcl-dev \
#                                harfbuzz-dev \
#                                fribidi-dev

COPY . $APPETISER_DIR
RUN chmod +x $APPETISER_DIR/run_tests.sh
RUN chmod +x $APPETISER_DIR/run_appetiser.sh

RUN pip3 install --no-cache-dir -r $APPETISER_DIR/requirements.txt

RUN mkdir $TMPDIR $OUTPUT_DIR
WORKDIR $APPETISER_DIR

EXPOSE 80
CMD $APPETISER_DIR/run_appetiser.sh
