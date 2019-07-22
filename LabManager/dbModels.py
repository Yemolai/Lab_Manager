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


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String)
    person = db.relationship('Person', backref='person_genre', lazy=True)

    def __repr__(self):
        return f"Genre({self.genre_name})"


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    birthday = db.Column(db.Date)
    occupation = db.Column(db.Text)
    institution = db.Column(db.String(100))
    imagefile = db.Column(db.String(20), nullable=False, default='default.jpg')
    imagefile_path = db.Column(db.String, nullable=False, default=os.path.join("static/profile_pics", "default.jpg"))
    type_id = db.Column(db.Integer, db.ForeignKey(PersonType.id))
    genre_id = db.Column(db.Integer, db.ForeignKey(Genre.id))
    account = db.relationship('User', backref='own_info', lazy=True)
    frequency = db.relationship('FrequencyEvent', backref='person_frequency', lazy=True)
    field_events = db.relationship("FieldEvent", secondary=lambda: helper_field_person, back_populates="personnel")

    def __repr__(self):
        name = (f"{self.first_name} {self.middle_name} {self.last_name}") if middle_name else (f"{self.first_name} {self.last_name}")
        return f"{self.person_type}({name}, {self.sex}, birthday {self.birthday}, {self.occupation}, {self.institution}, {self.image_file})"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey(Person.id))
    notices = db.relationship('Notices', backref='author', lazy=True)

    def __repr__(self):
        return f"User({self.username}, {self.email})"


class FrequencyEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    entry_time = db.Column(db.Time, nullable=False)
    exit_time = db.Column(db.Time, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey(Person.id))

    def __repr__(self):
        return f"FrequencyEvent({self.person_id}, {self.date}, {self.entry_time}, {self.exit_time})"


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    imagefile = db.Column(db.String(20), default='default.jpg')
    imagefile_path = db.Column(db.String, default=os.path.join("static/equip_pics", "default.jpg"))
    lendings = db.relationship('LendingEvent', backref='equipment', lazy=True)
    issues = db.relationship('TechnicalIssues', backref='equipment', lazy=True)
    field_events = db.relationship("FieldEvent", secondary=lambda: helper_field_equips, back_populates="equipments")

    def __repr__(self):
        if self.return_date and self.solution_date:
            status = "Available"
        else:
            status = "Unavailable"

        return f"Equipment({self.name}, {status})"


class Lendings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lend_date = db.Column(db.Date, nullable=False)
    return_expected = db.Column(db.Date, nullable=False)
    return_done = db.Column(db.Date, nullable=True)
    observations = db.Column(db.Text)
    inventory_id = db.Column(db.Integer, db.ForeignKey(Inventory.id))

    def __repr__(self):
        return f"LendingEvent({self.inventory_id}, {self.lend_date}, {self.expected_return}, {self.return_date}, {self.observations})"
    

class TechnicalIssues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    report_date = db.Column(db.Date, default=datetime.utcnow)
    solution_date = db.Column(db.Date, nullable=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey(Inventory.id))

    def __repr__(self):
        if self.solution_date:
            return f"Issue({self.equipment_id}, {self.description}, in {self.report_date}, solved in {self.solution_date})"    
            
        return f"Issue({self.equipment_id}, {self.description}, in {self.report_date}. Not solved.)"
    

class Notices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=True)
    archived = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __repr__(self):
        return f"Notice({self.title}, {self.date}, by {self.author.first_name} {self.author.last_name})"

class FieldEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    date_start = db.Column(db.Date)
    date_end_expected = db.Column(db.Date)
    date_end_done = db.Column(db.Date)
    observations = db.Column(db.Text)
    personnel = db.relationship("Person", secondary=lambda: association_table, back_populates="field_events")
    lendings = db.relationship("Inventory", secondary=lambda: association_table, back_populates="field_events")

    def __repr__(self):
        return f"FieldEvent({self.location}, start in {self.date_start})"


helper_field_person = db.Table("helper_field_person",
    db.Column('Person', db.Integer, db.ForeignKey(Person.id)),
    db.Column('FieldEvent', db.Integer, db.ForeignKey(FieldEvent.id))
)

helper_field_equips = db.Table("helper_field_equips",
    db.Column('Inventory', db.Integer, db.ForeignKey(Inventory.id)),
    db.Column('FieldEvent', db.Integer, db.ForeignKey(FieldEvent.id))
)
