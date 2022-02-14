from flask import request
from flask_restful import Resource
from Model.TaskModel import TaskModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime


class Task(Resource):

    @jwt_required()
    def delete(self, task_id):
        user_id = get_jwt_identity()
        task = TaskModel.find_task_id(task_id)
        if task and task.task_user_id == user_id:
            task.delete_task()
            return {"msg": "Task deleted"}, 200
        return {"msg": "No task found or not authorized"}, 401

    @jwt_required()
    def get(self, task_id):
        user_id = get_jwt_identity()
        task = TaskModel.find_task_id(task_id)
        if task and task.task_user_id == user_id:
            return task.__repr__(), 200
        return {"msg": "No task found or not authorized"}, 401

    @jwt_required()
    def put(self, task_id):
        data = request.get_json()
        task = TaskModel.find_task_id(task_id)
        user_id = get_jwt_identity()
        if task.task_finished == 1:
            return {"msg": "This task is finished and cannot be modified!"}
        if task and task.task_user_id == user_id:
            task.task_text = data["text"]
            task.save_db()
            return {"msg": "Task updated successfully"}, 200

        return {"msg": "No task found or not authorized"}, 401

    @jwt_required()
    def patch(self, task_id):
        user_id = get_jwt_identity()
        task = TaskModel.find_task_id(task_id)
        if task and task.task_user_id == user_id:
            task.task_finished_date = datetime.now()
            task.task_finished = 1
            task.save_db()
            return {"msg": "Task finished successfully"}, 200

        return {"msg": "No task found or not authorized"}, 401
