from flask import request
from flask_restful import Resource
from Model.TaskModel import TaskModel


class Tasks(Resource):
    def post(self):
        data = request.get_json()
        new_task = TaskModel(data["text"])
        if new_task:
            new_task.save_db()
            return {"msg": "Task Created Successfully!"}, 201
        return {"msg": "Try again"}, 400

    def get(self):
        tasks = TaskModel.all_tasks()
        all_tasks = []
        for task in tasks:
            all_tasks.append(task.task_text)

        return {"tasks": all_tasks}
