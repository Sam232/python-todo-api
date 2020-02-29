# manage_todo.py controller
from datetime import datetime

from flask import request
import json
import logging

from app.controller import api, api_request, JsonResponse
from app.service.v1.manage_todo import ManageTodo

# logger setup
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


# create new user_todo route
@api.route("/add-todo", methods=["POST"])
@api_request.json
def add_new_todo():
    try:
        request_data = json.loads(request.data.decode("utf-8"))

        if "name" not in request_data:
            log.error("Name field must be provided")
            return JsonResponse.failed_resp(msg="Name field must be provided")

        elif "end_date" not in request_data:
            log.error("End date must be provided")
            return JsonResponse.failed_resp(msg="End date field must be provided")

        elif datetime.strptime(request_data["end_date"], "%Y-%m-%d").date().__lt__(datetime.today().date()):
            log.error("End date must not be less than current date")
            return JsonResponse.failed_resp(msg="End date must not be less than current date")

        else:
            result = ManageTodo.add_new_todo(request_data)

            if result["todo_added"]:
                return JsonResponse.success_resp(msg=result["msg"])
            else:
                return JsonResponse.failed_resp(msg=result["msg"])

    except Exception as exp:
        print(str(exp))
        return JsonResponse.failed_resp(msg="Error occurred while adding new todo.\nError: {}".format(str(exp)))


# find user_todo
@api.route("/user-todo", methods=["GET"])
def find_todo_by_name():
    try:
        todo = request.args.to_dict()

        if "name" in todo:
            log.info("Finding a single todo with the name [{}]".format(todo["name"]))
            result = ManageTodo.find_user_todo(todo["name"])

            if "error" in result:
                return JsonResponse.failed_resp(msg=result["error"])

            else:
                if result["todo_exist"] is True:
                    return JsonResponse.success_resp(data=result["data"])
                else:
                    return JsonResponse.failed_resp(msg=result["msg"])

        else:
            log.info("Finding all user todos")
            result = ManageTodo.find_user_todo(None)

            if "error" in result:
                return JsonResponse.failed_resp(msg=result["error"])

            else:
                if result["todo_exist"] is True:
                    return JsonResponse.success_resp(data=result["data"])
                else:
                    return JsonResponse.failed_resp(msg=result["msg"])

    except Exception as exp:
        return JsonResponse.failed_resp(msg="Error occurred while finding a todo.\nError: {}".format(str(exp)))


# update user todo_
@api.route("/update-todo", methods=["PUT"])
@api_request.json
def update_user_todo():
    try:
        request_param = request.args.to_dict()
        request_body = json.loads(request.data.decode("utf-8"))
        todo = {}

        if "id" in request_param:
            todo["id"] = request_param["id"]

            if len(request_body) > 0:
                if "name" in request_body:
                    todo["name"] = request_body["name"]
                if "status" in request_body:
                    todo["status"] = request_body["status"]
                if "end_date" in request_body:
                    todo["end_date"] = request_body["end_date"]
                if "description" in request_body:
                    todo["description"] = request_body["description"]

                result = ManageTodo.update_todo(todo)

                if "error" in result:
                    return JsonResponse.failed_resp(msg=result["error"])

                else:
                    if result["todo_updated"] is True:
                        return JsonResponse.success_resp(msg=result["msg"])
                    else:
                        return JsonResponse.failed_resp(msg=result["msg"])

            else:
                return JsonResponse.failed_resp(msg="Nothing to update")

        else:
            return JsonResponse.failed_resp(msg="Todo id parameter is required")

    except Exception as exp:
        return JsonResponse.failed_resp(msg="Error occurred while trying to update todo.\nError: {}".format(str(exp)))


# delete todo_
@api.route("/delete-todo", methods=["DELETE"])
def delete_user_todo():
    request_param = request.args.to_dict()

    if "id" in request_param:
        todo_id = request_param["id"]
        result = ManageTodo.delete_todo(todo_id)

        if "error" in result:
            return JsonResponse.failed_resp(msg=result["error"])

        else:
            if result["todo_deleted"] is True:
                return JsonResponse.success_resp(msg=result["msg"])
            else:
                return JsonResponse.failed_resp(msg=result["msg"])

    else:
        return JsonResponse.failed_resp(msg="Todo id parameter is required")





















