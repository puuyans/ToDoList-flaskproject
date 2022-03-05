from marshmallow import Schema, fields, ValidationError
from models.user import UserModel


def duplicate_user(request_username):
    if UserModel.find_username(username=request_username):
        raise ValidationError("Duplicate User from schema")



class UserSchema(Schema):
    class Meta:
        load_only = ()
        dump_only = ()

    username = fields.Str(required=True, validate=duplicate_user)
    name = fields.Str()
    last = fields.Str()
    password = fields.Str(required=True)
