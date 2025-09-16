import subprocess

from .json_utils import (
    extract_process_kwargs,
    extract_response_items,
    add_iiif_info_json,
)
from .jp2.convert import process
import flask
import logging
import logging.config

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "DEBUG", "handlers": ["wsgi"]},
    }
)

app = flask.Flask(__name__)


@app.errorhandler(500)
def server_error(e):
    return flask.jsonify(status="server error", message=str(e)), 500


@app.route("/ping", methods=["GET"])
def ping():
    return flask.jsonify(status="working")


@app.route("/convert", methods=["POST"])
def convert():
    json_data = flask.request.get_json()
    app.logger.info("Processing request data: %s", json_data)
    try:
        result = process(**extract_process_kwargs(json_data))
        proto_reponse = {**result, **extract_response_items(json_data)}
        response = add_iiif_info_json(proto_reponse)
        app.logger.info("Response: %s", json_data)
        return flask.jsonify(response)
    except FileNotFoundError as fileError:
        app.logger.exception("Error: %s", fileError)
        return flask.jsonify(status="file not found", message=str(fileError)), 400
    except subprocess.CalledProcessError as subprocess_error:
        app.logger.exception("Error: %s", subprocess_error.stderr)
        return (
            flask.jsonify(status="kakadu error", message=str(subprocess_error.stderr)),
            500,
        )
    except Exception as general_error:
        app.logger.exception("Error: %s", general_error)

        return flask.jsonify(status="server error", message=str(general_error)), 500


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
