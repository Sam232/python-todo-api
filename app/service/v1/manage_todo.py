# manage_todo.py service

import logging

from app.model.todo import Todo, Status

# setup logger
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class ManageTodo:
    @staticmethod
    def add_new_todo(todo):
        try:
            result = ManageTodo.check_todo_exist(todo.get("name"))

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
    def check_todo_exist(name):
        try:
            todo = Todo.objects(name=name, status=Status.STARTED.value).first()

            if todo is not None:
                log.error("Todo with the name [{}] already exist".format(name))

                result = {
                    "todo_exist": True,
                    "msg": "Todo name already exist"
                }

            else:
                result = {
                    "todo_exist": False
                }

            return result

        except Exception as exp:
            log.error("Error occurred while checking whether todo with the name, [{}] already exist.\nError: {}".format(name, exp))

            result = {
                "error": "Error occurred, try again"
            }
            return result

    @staticmethod
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
