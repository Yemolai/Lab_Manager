import os
from datetime import datetime
from flask_login import UserMixin
from LabManager import db, login_manager

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    image_filepath = db.Column(db.String, nullable=False, default=os.path.join("static/profile_pics", "default.jpg"))
    password = db.Column(db.String(60), nullable=False)
    notices = db.relationship('Notice', backref='author', lazy=True)

    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.image_file})"


class Frequency_Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    institution = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    entry_time = db.Column(db.Time, nullable=False)
    exit_time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f"Frequency_Event({self.name}, {self.institution}, {self.date}, {self.entry_time}, {self.exit_time})"


class Lending_Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    equipment = db.Column(db.Text, nullable=False)
    lend_date = db.Column(db.Date, nullable=False)
    expected_return_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    observations = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"Lending_Event({self.name}, {self.equipment}, {self.lend_date}, {self.expected_return_date}, {self.return_date}, {self.observations})"
    

class Technical_Issues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    report_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    solution_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"Issue({self.equipment}, {self.description}, {self.name}, {self.report_date}, {self.solution_date})"
    

class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=True)
    archived = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Notice({self.title}, {self.date}, {self.content})"
