from flask import request
from flask_restful import Resource
from Model.UserModel import UserModel


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

    def get(self):
        return {"msg": "something went wrong"}
