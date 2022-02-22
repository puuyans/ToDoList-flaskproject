from flask import request
from flask.views import MethodView
from models.task import TaskModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

TASK_NOT_FOUND = "Task not found"
NOT_AUTHORIZED_DELETE = "Only creator of the task can delete the task"
NOT_AUTHORIZED_VIEW = "Only creator of the task can view the task"
NOT_AUTHORIZED_MODIFY = "Only creator of the task can modify the task"
TASK_DELETED_SUCCESSFULLY = "Task deleted successfully!"
FINISHED_TASK_MODIFY = "This task is finished and cannot be modified!"
TASK_UPDATED_SUCCESSFULLY = "Task updated successfully!"
TASK_FINISHED_SUCCESSFULLY = "Task finished successfully!"
NO_TASKS_FOUND = "No task found for this user!"
TASK_CREATED_SUCCESSFULLY = "Task created successfully!"
TASK_CREATED_FAILED = "Creating new task failed!"


class Task(MethodView):
    """
    In this class all the actions related to tasks are handled.
    There are two approaches, for the first one there is no need for id: viewing all tasks and creating a new one
    The second one is actions related to a specific task which requires a task_id: deleting, updating, viewing
    This class is directly related to model.user
    """

    @classmethod
    def manage_all_tasks(cls):
        if request.method == "POST":
            return cls._create_task()
        elif request.method == "GET":
            return cls._view_all_tasks()

    @classmethod
    @jwt_required()
    def _view_all_tasks(cls):
        user_id = get_jwt_identity()
        tasks = TaskModel.all_tasks(user_id)
        all_tasks = []
        for task in tasks:
            all_tasks.append(task.task_text)
        if all_tasks:
            return {"tasks": all_tasks}, 200
        return {"msg": NO_TASKS_FOUND}, 404

    @classmethod
    @jwt_required()
    def _create_task(cls):
        user_id = get_jwt_identity()
        data = request.get_json()
        new_task = TaskModel(data["text"])
        new_task.task_user_id = user_id
        if new_task:
            new_task.save_db()
            return {"msg": TASK_CREATED_SUCCESSFULLY}, 201
        return {"msg": TASK_CREATED_FAILED}, 400

    @classmethod
    @jwt_required()
    def manage_task(cls, task_id: int):
        if request.method == "GET":
            return cls._view_task(task_id)
        elif request.method == "DELETE":
            return cls._delete_task(task_id)
        elif request.method == "PUT":
            return cls._modify_task(task_id)

    @classmethod
    @jwt_required(fresh=True)
    def _delete_task(cls, task_id: int):
        user_id = get_jwt_identity()
        task = TaskModel.find_task_id(task_id)
        if not task:
            return {"msg": TASK_NOT_FOUND}, 404
        if task.task_user_id != user_id:
            return {"msg": NOT_AUTHORIZED_DELETE}, 403
        if task.task_user_id == user_id and task:
            return {"msg": TASK_DELETED_SUCCESSFULLY}, 200

    @classmethod
    @jwt_required()
    def _view_task(cls, task_id: int):
        user_id = get_jwt_identity()
        task = TaskModel.find_task_id(task_id)
        if not task:
            return {"msg": TASK_NOT_FOUND}, 404
        if task.task_user_id != user_id:
            return {"msg": NOT_AUTHORIZED_VIEW}, 403
        if task and task.task_user_id == user_id:
            return task.__repr__(), 200

    @jwt_required()
    def _modify_task(self, task_id: int):
        data = request.get_json()
        task = TaskModel.find_task_id(task_id)
        user_id = get_jwt_identity()
        if not task:
            return {"msg": TASK_NOT_FOUND}, 404
        if task.task_user_id != user_id:
            return {"msg": NOT_AUTHORIZED_MODIFY}, 403
        if task.task_finished == 1:
            return {"msg": FINISHED_TASK_MODIFY}, 403
        if task and task.task_user_id == user_id:
            task.task_text = data["text"]
            task.save_db()
            return {"msg": TASK_UPDATED_SUCCESSFULLY}, 200

    @jwt_required()
    def _finish_task(self, task_id: int):
        user_id = get_jwt_identity()
        task = TaskModel.find_task_id(task_id)
        if not task:
            return {"msg": TASK_NOT_FOUND}, 404
        if task.task_user_id != user_id:
            return {"msg": NOT_AUTHORIZED_MODIFY}, 403
        if task.task_finished == 1:
            return {"msg": FINISHED_TASK_MODIFY}, 403
        if task and task.task_user_id == user_id:
            task.task_finished_date = datetime.now()
            task.task_finished = 1
            task.save_db()
            return {"msg": TASK_FINISHED_SUCCESSFULLY}, 200