from flask import Flask
from flask_restful import Api
from db import db
from flask_jwt_extended import JWTManager
from resources.task import Task
from resources.tasks import Tasks
from resources.user import UserRegister, UserLogin, TokenRefresh, UserLogout
from models.token_blocklist import TokenBlocklist

app = Flask(__name__)

jwt = JWTManager(app)

app.secret_key = "supersecretverydifficulttocrack"
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
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
    return {"msg": "invalid token"}


api.add_resource(Tasks, "/tasks")
api.add_resource(Task, "/task/<int:task_id>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

if __name__ == "__main__":
    app.run(debug=True)
