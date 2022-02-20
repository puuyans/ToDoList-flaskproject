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


class Task(MethodView):
    @jwt_required(fresh=True)
    def delete(self, task_id: int):
        user_id = get_jwt_identity()
        task = TaskModel.find_task_id(task_id)
        if not task:
            return {"msg": TASK_NOT_FOUND}, 404
        if task.task_user_id != user_id:
            return {"msg": NOT_AUTHORIZED_DELETE}, 403
        if task.task_user_id == user_id and task:
            return {"msg": TASK_DELETED_SUCCESSFULLY}, 200

    @jwt_required()
    def get(self, task_id: int):
        user_id = get_jwt_identity()
        task = TaskModel.find_task_id(task_id)
        if not task:
            return {"msg": TASK_NOT_FOUND}, 404
        if task.task_user_id != user_id:
            return {"msg": NOT_AUTHORIZED_VIEW}, 403
        if task and task.task_user_id == user_id:
            return task.__repr__(), 200

    @jwt_required()
    def put(self, task_id: int):
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
    def patch(self, task_id: int):
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
