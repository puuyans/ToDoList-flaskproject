from flask import request
from flask_restful import Resource
from Model.TaskModel import TaskModel


class Task(Resource):
    def delete(self, task_id):
        task = TaskModel.find_task_id(task_id)
        if task:
            task.delete_task()
            return {"msg": "Task deleted"}, 200
        return {"msg": "No task found"}, 404

    def get(self, task_id):
        task = TaskModel.find_task_id(task_id)
        if task:
            return task.__repr__(), 200
        return {"msg": "No task found"}, 404

    def put(self, task_id):
        data = request.get_json()
        try:
            item = TaskModel.find_task_id(task_id)
            item.task_text = data["text"]
            item.save_db()
            return {"msg": "Task updated successfully"}, 200
        except:
            return {"msg": "Task not found"}, 404
