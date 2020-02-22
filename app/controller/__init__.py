from flask import Blueprint
from flask import jsonify

from app.libs.decorators import ApiRequest

api = Blueprint("api", __name__, url_prefix="/api/v1")
api_request = ApiRequest


class JsonResponse:
    @staticmethod
    def success_resp(code="00", msg="success", data={}, nav=None):
        if nav is not None:
            return jsonify(code=code, msg=msg, data=data, nav=nav)
        else:
            return jsonify(code=code, msg=msg, data=data)

    @staticmethod
    def failed_resp(code="01", msg="failed"):
        return jsonify(code=code, msg=msg)


from app.controller.v1 import manage_todo
