from db import db
from uuid import uuid4
from time import time

CONFIRMATION_EXPIRATION_TIME = 1800  # 30 min


class ConfirmationModel(db.Model):
    __tablename__ = "confirmations"

    confirm_id = db.Column(db.String(50), primary_key=True)
    confirm_expire = db.Column(db.Integer, nullable=False)
    confirm_finished = db.Column(db.Boolean, nullable=False)
    confirm_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    users = db.relationship("UserModel")

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.confirm_user_id = user_id
        self.confirm_id = uuid4().hex
        self.confirm_expiration = int(time()) + CONFIRMATION_EXPIRATION_TIME
        self.confirm_finished = False

    @classmethod
    def find_by_id(cls, _id: str) -> "ConfirmationModel":
        return cls.query.filter_by(confirm_id=_id).first()

    @property
    def expired(self):
        return time() > self.confirm_expiration  # compare current time with expiry date

    def force_to_expire(self):
        if not self.expired:
            self.confirm_expiration = int(time())
            self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
