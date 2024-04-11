import json
from flask import Response
from flask_restful import abort


def simple_message_response(message, status = 200):
    return Response(
        response=json.dumps({
            "message": message
        }),
        status=status,
        mimetype="application/json"
    )


def simple_message_error(message):
    return abort(404, message=message)
