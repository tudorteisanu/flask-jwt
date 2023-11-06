from extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


def generate_uuid():
    return uuid4()
    

class User(db.Model):
    updatebleFields = ['email', 'bio', 'username']
    __tablename__ = "users"
    id = db.Column(db.String(128), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    password = db.Column(db.Text())
    bio = db.Column(db.Text())
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())    

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def add(self, payload):
        for item in payload:
            if hasattr(self, item):
                setattr(self, item, payload[item])

        db.session.add(self)
        db.session.commit()

    def update(self, payload):
        for item in self.updatebleFields:
            if payload.get(item, None) is not None:
                setattr(self, item, payload[item])

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(128), nullable=True)
    create_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"<Token {self.jti}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()