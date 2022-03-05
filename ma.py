from marshmallow import Schema, fields, INCLUDE, EXCLUDE
from datetime import datetime as dt


class BookSchema(Schema):
    title = fields.Str()
    author = fields.Str(required=True)
    description = fields.Str()
    date = fields.Function()


class Book:
    def __init__(self, title, author, description, date):
        self.title = title
        self.author = author
        self.description = description
        self.date = date



incoming_data = {
    "title": "abbas",
    "author": "booazar",
    "description": "test",
    "date" : dt.now()
}

book_schema = BookSchema(unknown=INCLUDE)
new_book = book_schema.load(incoming_data)
b1 = Book(**new_book)
print(b1.__dict__)