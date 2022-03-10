from flask import request, make_response, render_template
from flask.views import MethodView
from models.user import UserModel
from models.token_blocklist import TokenBlocklist
from models.email import EmailModel
from werkzeug.security import check_password_hash
from marshmallow import ValidationError, EXCLUDE
from sqlalchemy.exc import SQLAlchemyError
from schemas.user import UserLoginSchema, UserRegisterSchema
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

DUPLICATE_USER = "User already exists, choose another username!"
USER_CREATE_SUCCESSFUL = "User created successfully!"
LOGIN_FAILED = "Login failed! Invalid credentials!"
JWT_REVOKED = "User logged out!"
USER_CREATE_FAILED = "Could not create new user"
EMAIL_ACTIVATED_FALSE = "User email is not activated!"
USER_NOT_FOUND = "Username not found!"
USER_ACTIVATED_SUCCESS = "User activated successfully!"
USER_ALREADY_CONFIRMED = "This user is already activated!"
DUPLICATE_EMAIL = "Email already exists, choose another email!"

login_schema = UserLoginSchema(unknown=EXCLUDE)
register_schema = UserRegisterSchema(unknown=EXCLUDE)


class UserService(MethodView):
    """
    In this class all the actions related to a user are handled, such as register login and logout
    This class is directly related to model.user
    """

    @classmethod
    def user_register(cls):
        # creating a dictionary of incoming json data
        try:
            get_json = request.get_json()
            data = register_schema.load(get_json)
        except ValidationError as err:
            return err.messages, 400

        # checking for duplicate username in db
        try:
            cls._duplicate_user(data["username"])
        except ValidationError as err:
            return {"error": err.messages}, 400

        # checking for duplicate email
        try:
            cls._duplicate_email(data["email"])
        except ValidationError as err:
            return {"error": err.messages}, 400

        # TODO r&d about rollback transition
        # inserting the new user data in db
        try:
            cls._create_user(data)
            new_user = UserModel.find_username(data["username"])
            EmailModel.send_confirmation_email(new_user.user_id, new_user.user_email)
            return {"msg": USER_CREATE_SUCCESSFUL}, 201
        except ConnectionError:
            return {"msg": USER_CREATE_FAILED}, 400

    @classmethod
    def _duplicate_user(cls, request_username: str):
        if UserModel.find_username(username=request_username):
            raise ValidationError(DUPLICATE_USER, field_name="Username")

    @classmethod
    def _duplicate_email(cls, request_email: str):
        if UserModel.find_email(request_email):
            raise ValidationError(DUPLICATE_EMAIL, field_name="Email")

    @classmethod
    def _create_user(cls, data: dict):
        new_user = UserModel(
            data["username"], data["name"], data["last"], data["email"], data["password"]
        )
        new_user.save_to_db()
        return new_user

    @classmethod
    def user_login(cls):
        try:
            get_json = request.get_json()
            data = login_schema.load(get_json)
        except ValidationError as err:
            return err.messages, 400

        try:
            user = UserModel.find_username(data["username"])
        except SQLAlchemyError:
            return {"msg": LOGIN_FAILED}, 404

        if user and check_password_hash(user.user_password, data["password"]):
            if user.user_activated:
                access_token = create_access_token(identity=user.user_id, fresh=True)
                refresh_token = create_refresh_token(user.user_id)
                return {
                           "access_token": access_token,
                           "refresh_token": refresh_token,
                       }, 200
            return {"msg": EMAIL_ACTIVATED_FALSE}, 400
        return {"msg": LOGIN_FAILED}, 400

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

    @classmethod
    def activate_user(cls, user_id: int):
        user = UserModel.find_user_by_id(user_id)
        if user:
            if user.user_activated == 1:
                return {"msg": USER_ALREADY_CONFIRMED}, 409
            user.user_activated = 1
            user.save_to_db()
            headers = {"Content-Type": "text/html"}
            return make_response(render_template("confirmation_page.html", email=user.user_email, name=user.user_name),
                                 headers)
        return {"msg": USER_NOT_FOUND}, 404
