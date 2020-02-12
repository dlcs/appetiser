from app.json_utils import (
    extract_process_kwargs,
    extract_response_items,
    add_iiif_info_json,
)
from app.convert import process
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

appetiser = flask.Flask(__name__)

# Import after setup of logging to allow inclusion of
# initialisation logging in wsgi stdout.


@appetiser.errorhandler(500)
def server_error(e):
    return flask.jsonify(status="server error", message=str(e)), 500


@appetiser.route("/ping", methods=["GET"])
def ping():
    return flask.jsonify(status="working")


@appetiser.route("/convert", methods=["POST"])
def convert():
    json_data = flask.request.get_json()
    appetiser.logger.info("Processing request data: %s", json_data)
    result = process(**extract_process_kwargs(json_data))
    proto_reponse = {**result, **extract_response_items(json_data)}
    response = add_iiif_info_json(proto_reponse)
    appetiser.logger.info("Response: %s", json_data)
    return flask.jsonify(response)


if __name__ == "__main__":
    appetiser.run(threaded=True, debug=True)
