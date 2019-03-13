FROM python:3.7-alpine

EXPOSE 80

RUN apk add --update --no-cache --virtual=run-deps

RUN pip3 install --no-cache-dir -r /requirements.txt

CMD ["uwsgi", "--http", "0.0.0.0:80", "--master", "--module", "schema_validation:application", "--processes", "1"]
