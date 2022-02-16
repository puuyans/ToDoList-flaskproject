from flask import request
from flask_restful import Resource
from Model.UserModel import UserModel
from Model.TokenBlocklist import TokenBlocklist
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt


class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        if UserModel.find_username(username=data["username"]):
            return {"msg": "user already exists"}, 400
        else:
            new_user = UserModel(data['username'], data['name'], data['last'], data['password'])
        try:
            new_user.save_to_db()
            return {"msg": "user successfully created!"}, 201

        except:
            return {"msg": "something went wrong"}, 400


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = UserModel.find_username(data['username'])
        if user and check_password_hash(user.user_password, data['password']):
            access_token = create_access_token(identity=user.user_id, fresh=True)
            refresh_token = create_refresh_token(user.user_id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        return {"msg": "Invalid Credentials"}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        token = TokenBlocklist(jti)
        token.save_db()
        return {"msg": "JWT Revoked"}


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
