from flask import Flask
from flask_restful import Api
from db import db
from flask_jwt_extended import JWTManager
from Resources.TaskResource import Task
from Resources.TasksResource import Tasks
from Resources.UserResource import UserRegister, UserLogin

app = Flask(__name__)

jwt = JWTManager(app)


app.secret_key = 'supersecretverydifficulttocrack'
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Tasks, "/tasks")
api.add_resource(Task, "/task/<int:task_id>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
if __name__ == '__main__':
    app.run(debug=True)
