from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    display_name = db.Column(db.String(50), nullable=False)  # Добавлено поле display_name
    _password_hash = db.Column(db.String(128), nullable=False)
    relationship_status = db.Column(db.String(10), nullable=False)
    partner_nick = db.Column(db.String(50), nullable=True)
    profile_picture = db.Column(db.String(100), nullable=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
