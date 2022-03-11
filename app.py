from flask import Flask
from db import db
from flask_jwt_extended import JWTManager
from resources.task import Task
from resources.user import UserService
from models.token_blocklist import TokenBlocklist
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
jwt = JWTManager(app)

app.secret_key = os.environ.get("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
db.init_app(app)


# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {"msg": "invalid token!"}, 401


# viewing all tasks and create a new task
app.add_url_rule("/tasks", view_func=Task.manage_all_tasks, methods=["POST", "GET"])

# actions for a specific task such as update, delete and view
app.add_url_rule(
    "/task/<int:task_id>",
    view_func=Task.manage_task,
    methods=["GET", "DELETE", "PUT"],
)

# actions for a user such as login logout or register
app.add_url_rule(
    "/register",
    view_func=UserService.user_register,
    methods=["POST"],
)

app.add_url_rule(
    "/login",
    view_func=UserService.user_login,
    methods=["POST"],
)

app.add_url_rule(
    "/logout",
    view_func=UserService.user_logout,
    methods=["POST"],
)

app.add_url_rule(
    "/refresh",
    view_func=UserService.token_refresh,
    methods=["POST"],
)

app.add_url_rule(
    "/activate/<int:user_id>",
    "activate",
    view_func=UserService.activate_user,
    methods=["PUT"],
)

if __name__ == "__main__":
    app.run(debug=True)
