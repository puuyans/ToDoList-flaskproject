from marshmallow import validate, ValidationError








def is_even(value):
    if value % 2 != 0:
        raise ValidationError("Not an even value.")

validator = validate.And(validate.Range(min=0), is_even)
validator(2)

