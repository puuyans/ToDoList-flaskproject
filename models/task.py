from datetime import datetime
from app import db
from typing import Dict, List


class TaskModel(db.Model):
    __tablename__ = "tasks"
    task_id = db.Column(db.Integer, primary_key=True)
    task_text = db.Column(db.String(100), nullable=False)
    task_created_date = db.Column(db.DateTime(), nullable=False)
    task_finished_date = db.Column(db.DateTime(), nullable=True)
    task_finished = db.Column(db.Boolean(), nullable=False)
    task_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    users = db.relationship("UserModel")

    def __init__(self, text: str):
        self.task_id = None
        self.task_text = text
        self.task_created_date = datetime.now()
        self.task_finished_date = None
        self.task_finished = 0
        self.task_user_id = None

    def __repr__(self) -> Dict:
        return {
            "task_id": self.task_id,
            "task_text": self.task_text,
            "task_created_date": str(self.task_created_date),
            "task_finished_date": str(self.task_finished_date),
            "task_finished": "No" if self.task_finished == 0 else "Yes",
        }

    def save_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_task_id(cls, task_id: int) -> "TaskModel":
        task = cls.query.filter_by(task_id=task_id).first()
        if task:
            return task

    def delete_task(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all_tasks(cls, user_id: int) -> List["TaskModel"]:
        return cls.query.filter_by(task_user_id=user_id).all()

    @classmethod
    def task_status(cls, task_id: int) -> int:
        task = cls.query.filter_by(task_id=task_id).first()
        return task.task_finished
