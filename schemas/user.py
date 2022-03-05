from marshmallow import Schema, fields, validate, pre_load


class UserRegisterSchema(Schema):
    class Meta:
        load_only = ()
        dump_only = ()

    username = fields.Str(required=True, validate=validate.Length(min=3, max=20))
    name = fields.Str(required=True, validate=validate.Length(min=3, max=20))
    last = fields.Str(required=True, validate=validate.Length(min=3, max=20))
    password = fields.Str(required=True, validate=validate.Length(min=3, max=20))

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
        return item


class UserLoginSchema(Schema):
    class Meta:
        load_only = ()
        dump_only = ()

    password = fields.Str(required=True, validate=validate.Length(min=3, max=20))
    username = fields.Str(required=True, validate=validate.Length(min=3, max=20))

    @pre_load
    def strip_username(self,item, **kwargs):
        if "username" in item:
            item["username"] = item["username"].strip()
        return item
