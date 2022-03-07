from marshmallow import Schema, fields, validate, pre_load


class TaskSchema(Schema):
    class Meta:
        load_only = ()
        dump_only = ()

    text = fields.String(required=True, validate=validate.Length(min=1, max=100))
    finished = fields.Boolean(required=True)

    @pre_load
    def strip_text(self, item, many, **kwargs):
        if "text" in item:
            item["text"] = item["text"].strip()
        return item
