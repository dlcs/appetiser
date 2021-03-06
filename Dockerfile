FROM python:3.7-slim-stretch

ENV KAKADU_APPS_LOCATION s3://dlcs-dlcservices-bootstrap-objects/kdu77-apps.tar.gz
ENV APPETISER_DIR /opt/appetiser
ENV TMPDIR $APPETISER_DIR/tmp
ENV OUTPUT_DIR $APPETISER_DIR/out/

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

COPY . $APPETISER_DIR
RUN chmod +x $APPETISER_DIR/run_tests.sh
RUN chmod +x $APPETISER_DIR/run_appetiser.sh

RUN pip3 install --no-cache-dir -r $APPETISER_DIR/requirements.txt

RUN mkdir $TMPDIR $OUTPUT_DIR
WORKDIR $APPETISER_DIR

EXPOSE 80
CMD $APPETISER_DIR/run_appetiser.sh
