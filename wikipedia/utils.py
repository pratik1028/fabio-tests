from flask import Response, jsonify

from wikipedia.constants import SUCCESS


def http_json_response(
    data=None,
    message="",
    status_code=SUCCESS,
    error=False
):
    if error:
        resp = {'status': 'error', 'message': message}
        return jsonify(resp), status_code
    else:
        resp = {'status': 'success'}
        if message:
            resp['message'] = message
        if data or not message:
            resp['data'] = data
        return jsonify(resp), status_code
