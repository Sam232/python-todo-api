# manage_todo.py service

import logging
import datetime

from app.model.todo import Todo, Status

# setup logger
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class ManageTodo:
    @staticmethod
    # add todo_
    def add_new_todo(todo):
        try:
            result = ManageTodo.check_todo_exist(name=todo.get("name"))

            if "error" in result:
                response = {
                    "todo_added": False,
                    "msg": result["error"]
                }

            elif result["todo_exist"]:
                response = {
                    "todo_added": False,
                    "msg": "Todo name already exist"
                }

            else:
                todo_data = Todo()
                todo_data.name = todo.get("name")
                todo_data.end_date = todo.get("end_date")

                if "description" in todo:
                    print(todo)
                    todo_data.description = todo.get("description")

                todo_data.save()

                todo = todo_data
                log.info("New todo created successfully "+str(todo.to_dict()))

                response = {
                    "todo_added": True,
                    "msg": "Todo created successfully"
                }

            return response

        except Exception as exp:
            log.error("Error occurred while adding a todo with the name, [{}].\nError: {}".format(todo.get("name"), exp))

            response = {
                "todo_added": False,
                "msg": str(exp)
            }
            return response

    @staticmethod
    # check whether todo_ exist
    def check_todo_exist(**kwargs):
        try:
            if "name" in kwargs:
                todo = Todo.objects(name=kwargs["name"], status=Status.STARTED.value).first()

                if todo is not None:
                    log.error("Todo with the name [{}] already exist".format(kwargs["name"]))

                    result = {
                        "todo_exist": True,
                        "msg": "Todo name [{}] already exist".format(kwargs["name"])
                    }

                else:
                    result = {
                        "todo_exist": False
                    }

                return result
            elif "id" in kwargs:
                todo = Todo.objects(id=kwargs["id"]).first()

                if todo is not None:
                    log.info("Provided todo Id[{}] matches a todo's Id".format(kwargs["id"]))

                    result = {
                        "todo_exist": True
                    }

                else:
                    log.warning("Provided todo Id[{}] does not match any todo's Id".format(kwargs["id"]))
                    result = {
                        "todo_exist": False,
                        "msg": "No todo's Id matches the provided Id"
                    }

                return result

        except Exception as exp:
            log.error("Error occurred while checking whether todo with the {}, [{}] already exist.\nError: {}".format(kwargs["name"] if kwargs["name"] else kwargs["id"], "name" if kwargs["name"] else "id", exp))

            result = {
                "error": "Error occurred, try again"
            }
            return result

    @staticmethod
    # find todo_ by name otherwise fetch all todos
    def find_user_todo(name):
        try:
            if name is not None:
                todo = Todo.objects(name=name).first()

                if todo is not None:
                    log.info("Todo fetched")

                    response = {
                        "todo_exist": True,
                        "data": todo.to_dict()
                    }

                else:
                    log.info("No todo exist with the name [{}]".format(name))

                    response = {
                        "todo_exist": False,
                        "msg": "Todo does not exist"
                    }

            else:
                todo_list = []
                todo_object = Todo.objects().order_by("end_date")

                if len(todo_object) > 0:
                    for todo in todo_object:
                        todo_list.append(todo.to_dict())

                    log.info("Todos fetched")

                    response = {
                        "todo_exist": True,
                        "data": todo_list
                    }
                else:
                    log.info("No todos exist")

                    response = {
                        "todo_exist": False,
                        "msg": "No todo added"
                    }

            return response

        except Exception as exp:
            log.error("Error occurred while checking whether todo with the name, [{}] exist.\nError: {}".format(name, exp))

            result = {
                "error": "Error occurred, try again"
            }
            return result

    @staticmethod
    # check todo_ name duplicate
    def todo_name_duplicate(*args):
        try:
            todo_duplicate = Todo.objects(id__ne=args[0], name=args[1]).first()

            if todo_duplicate is not None:
                result = {
                    "todo_name_duplicate": True,
                    "msg": "Todo name already taken"
                }

            elif todo_duplicate is None:
                result = {
                    "todo_name_duplicate": False,
                }

            else:
                log.warning("Unable to check todo duplicate")
                result = {
                    "error": "Unable to check todo duplicate",
                }

            return result

        except Exception as exp:
            log.error("Error occurred while checking todo name [{}] duplicate.\nError: {}".format(args[1], exp))

            result = {
                "error": "Error occurred, try again"
            }
            return result

    @staticmethod
    # update a todo_
    def update_todo(todo):
        try:
            todo_check = ManageTodo.check_todo_exist(id=todo["id"])

            print("todo check result", todo_check)

            if "error" in todo_check:
                log.error("Error occurred while trying to update the todo with the id[{}].".format(todo["id"]))
                result = {
                    "error": "Error occurred, try again"
                }

            elif todo_check["todo_exist"]:
                if "name" in todo:
                    todo_duplicate = ManageTodo.todo_name_duplicate(todo["id"], todo["name"])

                    if "error" in todo_duplicate:
                        log.error("Error occurred while trying to update the todo with the id[{}].".format(todo["id"]))
                        result = {
                            "error": "Error occurred, try again"
                        }

                        return result
                    elif todo_duplicate["todo_name_duplicate"] is True:
                        result = {
                            "todo_updated": False,
                            "msg": todo_duplicate["msg"]
                        }

                        return result
                    elif todo_duplicate["todo_name_duplicate"] is False:
                        result = ManageTodo.complete_todo_update(todo)
                    else:
                        result = {
                            "todo_updated": False,
                            "msg": "Unable to update todo, try again"
                        }
                else:
                    result = ManageTodo.complete_todo_update(todo)

            else:
                result = {
                    "todo_updated": False,
                    "msg": todo_check["msg"]
                }

            return result

        except Exception as exp:
            log.error("Error occurred while trying to update the todo with the id[{}].\nError: {}".format(todo["id"], exp))

            result = {
                "error": "Error occurred, try again"
            }
            return result

    @staticmethod
    # complete todo_ update
    def complete_todo_update(todo):
        todo_update = Todo.objects(id=todo["id"]).first()

        if "name" in todo:
            todo_update.name = todo["name"]
        if "status" in todo:
            todo_update.status = todo["status"]
        if "end_date" in todo:
            todo_update.end_date = todo["end_date"]
        if "description" in todo:
            todo_update.description = todo["description"]

        todo_update.modified_at = datetime.datetime.today()

        todo_update.save()
        update_result = todo_update.to_dict()

        log.info("Todo with the Id[{}] has been updated. {}".format(todo_update.id, str(update_result)))
        result = {
            "todo_updated": True,
            "msg": "Todo updated successfully"
        }

        return result

    @staticmethod
    # delete a user todo_
    def delete_todo(todo_id):
        try:
            todo_check = ManageTodo.check_todo_exist(id=todo_id)

            if "error" in todo_check:
                log.error("Error occurred while trying to update the todo with the id[{}].".format(todo_id))
                result = {
                    "error": "Error occurred, try again"
                }

            elif todo_check["todo_exist"]:
                todo = Todo.objects(id=todo_id).delete()

                log.info("Todo with the Id [{}] has been deleted successfully. {}".format(todo_id, str(todo)))
                result = {
                    "todo_deleted": True,
                    "msg": "Todo deleted successfully"
                }

            else:
                result = {
                    "todo_deleted": False,
                    "msg": "Provided Id does not match any todo's Id"
                }

            return result

        except Exception as exp:
            log.error("Error occurred while trying to delete the todo with the id[{}].\nError: {}".format(todo_id, exp))

            result = {
                "error": "Error occurred, try again"
            }
            return result


