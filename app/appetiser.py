import flask
import logging

import jp2
from .request_utils import (
    extract_process_kwargs,
    extract_response_items
)

application = flask.Flask(__name__)


@application.route('/convert', methods=['POST'])
def convert():
    json_data = flask.request.get_json()
    result = jp2.process(**extract_process_kwargs(json_data))

    return flask.jsonify({
        **format_response(result),
        **extract_response_items(json_data)
    })


if __name__ == '__main__':
    application.run(threaded=True, debug=True)
