from db import db


class UserModel(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String(20))
    user_name = db.Column(db.String(20))
    user_last = db.Column(db.String(20))
    user_password = db.Column(db.String(100))
    user_admin = db.Column(db.Boolean)

    def __init__(self, username, name, last, password):
        self.user_id = None
        self.user_username = username
        self.user_name = name
        self.user_last = last
        self.user_password = password
        self.user_admin = 0

    @classmethod
    def find_user_by_id(cls, userid):
        user = cls.query.filter_by(user_id=userid).first_or_404()
        if user:
            return user

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
