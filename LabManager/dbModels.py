import os
from datetime import datetime
from flask_login import UserMixin
from LabManager import db, login_manager

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class PersonType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String)
    person = db.relationship('Person', backref='person_type', lazy=True)

    def __repr__(self):
        return f"PersonType({self.type_name})"


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    sex = db.Column(db.String)
    birthday = db.Column(db.Date)
    occupation = db.Column(db.Text)
    institution = db.Column(db.String(100))
    timedelta = db.Column(db.Interval)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    image_filepath = db.Column(db.String, nullable=False, default=os.path.join("static/profile_pics", "default.jpg"))
    type_id = db.Column(db.Integer, db.ForeignKey(PersonType.id))
    account = db.relationship('User', backref='own_info', lazy=True)
    frequency = db.relationship('FrequencyEvent', backref='person', lazy=True)

    def __repr__(self):
        name = (f"{self.first_name} {self.middle_name} {self.last_name}") if middle_name else (f"{self.first_name} {self.last_name}")
        return f"{self.person_type}({name}, {self.sex}, birthday {self.birthday}, {self.occupation}, {self.institution}, {self.image_file})"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey(Person.id))
    notices = db.relationship('Notice', backref='author', lazy=True)

    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.own_info})"


class FrequencyEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey(Person.id))
    date = db.Column(db.Date, nullable=False)
    entry_time = db.Column(db.Time, nullable=False)
    exit_time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f"FrequencyEvent({self.person}, {self.date}, {self.entry_time}, {self.exit_time})"


class EquipmentInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=1)
    image_file = db.Column(db.String(20), default='default.jpg')
    image_filepath = db.Column(db.String, default=os.path.join("static/equip_pics", "default.jpg"))
    lendings = db.relationship('LendingEvent', backref='equipment', lazy=True)
    issues = db.relationship('TechnicalIssues', backref='equipment', lazy=True)

    def __repr__(self):
        if self.return_date and self.solution_date:
            status = "Available"
        else:
            status = "Unavailable"

        return f"Equipment({self.equipment_name}, {self.quantity}, {status})"


class LendingEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey(EquipmentInventory.id))
    lend_date = db.Column(db.Date, nullable=False)
    expected_return = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    observations = db.Column(db.Text)

    def __repr__(self):
        return f"LendingEvent({self.equipment}, {self.lend_date}, {self.expected_return}, {self.return_date}, {self.observations})"
    

class TechnicalIssues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey(EquipmentInventory.id))
    issue_description = db.Column(db.Text, nullable=False)
    report_date = db.Column(db.Date, default=datetime.utcnow)
    solution_date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        if self.solution_date:
            return f"Issue({self.equipment}, {self.issue_description}, in {self.report_date}, solved in {self.solution_date})"    
            
        return f"Issue({self.equipment}, {self.issue_description}, in {self.report_date}. Not solved.)"
    

class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=True)
    archived = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Notice({self.title}, {self.date}, by {self.author.first_name} {self.author.last_name})"
