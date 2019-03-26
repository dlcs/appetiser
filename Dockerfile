FROM python:3.7-alpine

EXPOSE 80

RUN apk add --update --no-cache --virtual=run-deps

#libtiff (required by Pillow for i/o of .tiff files)

# TODO Set tmpdir so that it's an env variable found by python.
RUN pip3 install --no-cache-dir -r /requirements.txt

CMD ["uwsgi", "--http", "0.0.0.0:80", "--master", "--module", "", "--processes", "1"]
