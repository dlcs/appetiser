import flask
import logging

from app.jp2.convert import (
    process
)
from app.json_utils import (
    extract_process_kwargs,
    extract_response_items,
    add_iiif_info_json
)

appetiser = flask.Flask(__name__)


@appetiser.route('/ping', methods=['GET'])
def ping():
    return flask.jsonify(
        {'status': 'working'}
    )


@appetiser.route('/convert', methods=['POST'])
def convert():
    json_data = flask.request.get_json()
    result = process(**extract_process_kwargs(json_data))
    proto_reponse = {
        **result,
        **extract_response_items(json_data)
    }
    response = add_iiif_info_json(proto_reponse)
    return flask.jsonify(response)


if __name__ == '__main__':
    appetiser.run(threaded=True, debug=True)
