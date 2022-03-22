from functools import wraps
import json
import os
from flask import jsonify, request
import logging

logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')

def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            gunicorn_logger.debug("get json requests:")
            for k,v in request.json.items():
                gunicorn_logger.debug(f"{k}: {v}")
        except Exception as e:
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 400
        return f(*args, **kw)

    return wrapper


def validate_json_param(params=[]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                for i in params:
                    assert i in request.json
            except AssertionError as e:
                return jsonify({"error": f"post data keys must have all of {params}"}), 400
            return f(*args, **kw)

        return wrapper
    return decorator

