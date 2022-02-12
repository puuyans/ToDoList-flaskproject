from flask import Flask
from flask_restful import Api
from db import db
from Resources.TaskResource import Task
from Resources.TasksResource import Tasks
from Resources.UserResource import UserRegister

app = Flask(__name__)

api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Tasks, "/tasks")
api.add_resource(Task, "/task/<int:task_id>")
api.add_resource(UserRegister, "/User")
if __name__ == '__main__':
    app.run()
