from flask import request, jsonify
from functools import wraps


class ApiRequest:
    @staticmethod
    def json(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request_headers = dict(request.headers)
            if "Content-Type" not in request_headers or "application/json" not in request_headers["Content-Type"]:
                return jsonify(code="01", msg="This API requires a JSON")
            if request.method is not "GET" and request.data is None:
                return jsonify(code="01", msg="A JSON data is required")

            return func(*args, **kwargs)
        return wrapper
