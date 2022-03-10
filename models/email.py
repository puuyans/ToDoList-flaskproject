from app import db
from requests import Response, post
from flask import request, url_for

MAIL_API_KEY = "4faa4e607cf85ce40b724e88724704f5-1b237f8b-3c5f7a62"
FROM_EMAIL = "sandbox55d3306fe6304c488c73a50d48091582.mailgun.org"
MAILGUN = "https://api.mailgun.net/v3/sandbox55d3306fe6304c488c73a50d48091582.mailgun.org/messages"


class EmailModel(db.Model):
    __tablename__ = "emails"
    email_id = db.Column(db.Integer, primary_key=True)
    email_subject = db.Column(db.String(50), nullable=False)
    email_body = db.Column(db.String(500), nullable=False)
    email_type = db.Column(db.String(10), nullable=False, unique=True)

    def __init__(self, subject: str, body: str, email_type: str):
        self.email_id = None
        self.email_subject = subject
        self.email_body = body
        self.email_type = email_type

    @classmethod
    def _find_by_type(cls, email_type: str) -> "EmailModel":
        email = cls.query.filter_by(email_type=email_type).first()
        return email

    @classmethod
    def send_confirmation_email(cls, user_id: int, user_email: str) -> Response:
        link = request.url_root[:-1] + url_for("activate", user_id=user_id)
        email = cls._find_by_type(email_type="Confirmation")
        return post(MAILGUN,
                    auth=("api", MAIL_API_KEY),
                    data={"from": f"T0 D0 App! <mailgun@{FROM_EMAIL}>",
                          "to": user_email,
                          "subject": email.email_subject,
                          "text": email.email_body.format(link)})