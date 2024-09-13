from . import db

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    full_name = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f'<UserProfile {self.username}>'
