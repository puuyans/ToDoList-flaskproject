from flask import request
from flask.views import MethodView
from models.user import UserModel
from models.token_blocklist import TokenBlocklist
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

DUPLICATE_USER = "User already exists, choose another user!"
USER_CREATE_SUCCESSFUL = "User created successfully!"
LOGIN_FAILED = "Login failed! Invalid credentials!"
JWT_REVOKED = "User logged out!"


class UserService(MethodView):
    """
    In this class all the actions related to a user are handled, such as register login and logout
    This class is directly related to model.user
    """

    @classmethod
    def user_register(cls):
        data = request.get_json()
        if UserModel.find_username(username=data["username"]):
            return {"msg": DUPLICATE_USER}, 400

        new_user = UserModel(
            data["username"], data["name"], data["last"], data["password"]
        )
        new_user.save_to_db()
        return {"msg": USER_CREATE_SUCCESSFUL}, 201

    @classmethod
    def user_login(cls):
        data = request.get_json()
        user = UserModel.find_username(data["username"])
        if user and check_password_hash(user.user_password, data["password"]):
            access_token = create_access_token(identity=user.user_id, fresh=True)
            refresh_token = create_refresh_token(user.user_id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"msg": LOGIN_FAILED}, 401

    @classmethod
    @jwt_required()
    def user_logout(cls):
        jti = get_jwt()["jti"]
        token = TokenBlocklist(jti)
        token.save_db()
        return {"msg": JWT_REVOKED}

    @classmethod
    @jwt_required(refresh=True)
    def token_refresh(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


# class UserRegister(Resource):
#     def post(self):
#         data = request.get_json()
#         if UserModel.find_username(username=data["username"]):
#             return {"msg": DUPLICATE_USER}, 400
#
#         new_user = UserModel(data["username"], data["name"], data["last"], data["password"])
#         new_user.save_to_db()
#         return {"msg": USER_CREATE_SUCCESSFUL}, 201
#
#
# class UserLogin(MethodView):
#     @classmethod
#     def login(cls):
#         data = request.get_json()
#         user = UserModel.find_username(data["username"])
#         if user and check_password_hash(user.user_password, data["password"]):
#             access_token = create_access_token(identity=user.user_id, fresh=True)
#             refresh_token = create_refresh_token(user.user_id)
#             return {"access_token": access_token, "refresh_token": refresh_token}, 200
#         return {"msg": LOGIN_FAILED}, 401
#
#
# class UserLogout(Resource):
#     @jwt_required()
#     def post(self):
#         jti = get_jwt()["jti"]
#         token = TokenBlocklist(jti)
#         token.save_db()
#         return {"msg": JWT_REVOKED}
#
#
# class TokenRefresh(Resource):
#     @jwt_required(refresh=True)
#     def post(self):
#         current_user = get_jwt_identity()
#         new_token = create_access_token(identity=current_user, fresh=False)
#         return {"access_token": new_token}, 200
