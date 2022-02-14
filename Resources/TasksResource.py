from flask import request
from flask_restful import Resource
from Model.TaskModel import TaskModel
from flask_jwt_extended import jwt_required, get_jwt_identity


class Tasks(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        new_task = TaskModel(data["text"])
        new_task.task_user_id = user_id
        if new_task:
            new_task.save_db()
            return {"msg": "Task Created Successfully!"}, 201
        return {"msg": "Try again"}, 400

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        tasks = TaskModel.all_tasks(user_id)
        all_tasks = []
        for task in tasks:
            all_tasks.append(task.task_text)

        return {"tasks": all_tasks}
