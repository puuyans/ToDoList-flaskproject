from db import db
from werkzeug.security import generate_password_hash


class UserModel(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String(20))
    user_name = db.Column(db.String(20))
    user_last = db.Column(db.String(20))
    user_password = db.Column(db.String(100))
    user_admin = db.Column(db.Boolean)

    def __init__(self, username: str, name: str, last: str, password: str):
        self.user_id = None
        self.user_username = username
        self.user_name = name
        self.user_last = last
        self.user_password = generate_password_hash(password)
        self.user_admin = 0

    @classmethod
    def find_user_by_id(cls, user_id: int) -> "UserModel":
        user = cls.query.filter_by(user_id=user_id).first_or_404()
        if user:
            return user

    @classmethod
    def find_username(cls, username: str) -> "UserModel":
        user = cls.query.filter_by(user_username=username).one()
        return user

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
