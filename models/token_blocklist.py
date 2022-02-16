from db import db
from datetime import datetime


class TokenBlocklist(db.Model):
    __tablename__ = "token"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, jti):
        self.id = None
        self.jti = jti
        self.created_at = datetime.now()

    def save_db(self):
        db.session.add(self)
        db.session.commit()
