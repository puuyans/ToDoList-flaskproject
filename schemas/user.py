from marshmallow import Schema, fields, validate, pre_load, ValidationError
import re


def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, email):
        raise ValidationError("Not a valid Email, please check!")


class UserRegisterSchema(Schema):
    class Meta:
        load_only = ()
        dump_only = ()

    username = fields.Str(required=True, validate=validate.Length(min=3, max=20))
    name = fields.Str(required=True, validate=validate.Length(min=3, max=20))
    last = fields.Str(required=True, validate=validate.Length(min=3, max=20))
    password = fields.Str(required=True, validate=validate.Length(min=3, max=20))
    email = fields.Str(required=True, validate=validate.And(validate.Length(min=3, max=30), validate_email))

    # strip input data
    @pre_load(
        pass_many=True,
    )
    def strip_data(self, item, many, **kwargs):
        if "username" in item:
            item["username"] = item["username"].strip()
        if "name" in item:
            item["name"] = item["name"].strip()
        if "last" in item:
            item["last"] = item["last"].strip()
        if "email" in item:
            item["email"] = item["email"].strip()
        return item


class UserLoginSchema(Schema):
    class Meta:
        load_only = ()
        dump_only = ()

    password = fields.Str(required=True, validate=validate.Length(min=3, max=20))
    username = fields.Str(required=True, validate=validate.Length(min=3, max=20))

    @pre_load
    def strip_username(self, item, **kwargs):
        if "username" in item:
            item["username"] = item["username"].strip()
        return item
