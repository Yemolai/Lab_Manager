from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from logon import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = 'changeme' #Mandatory to change this on deploy
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
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



@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/frequency")
def frequency():
    return render_template("frequency.html", title="Personel Frequency")

@app.route("/lendings")
def lendings():
    return render_template("lendings.html", title="Equipment Lendings")

@app.route("/technical")
def technical():
    return render_template("technical.html", title="Technical Issues")

@app.route("/notices")
def notices():
    return render_template("notices.html", title="Notice Board")

@app.route("/news")
def news():
    return render_template("news.html", title="News")

@app.route("/calendar")
def calendar():
    return render_template("calendar.html", title="Calendar")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/logon", methods=["GET", "POST"])
def logon():
    form_signUp = RegistrationForm()
    form_signIn = LoginForm()

    # Account successfully created
    if form_signUp.submit_signUp.data and form_signUp.validate():
        flash(f"Account created for {form_signUp.username.data}. You can now Log In.", "success")
        return redirect(url_for("home")) # redirect to home
    
    # User successfully logged in
    if form_signIn.submit_signIn.data and form_signIn.validate():
        passw = form_signIn.password.data
        email = form_signIn.email.data
        default_email = "dummyemail@email.com"
        default_passw = "password"
        # Change this to appropriate database calls
        if email == default_email and passw == default_passw:
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials.", "error")
    return render_template("logon.html", title="User Login", form_signUp=form_signUp, form_signIn=form_signIn)

if __name__ == '__main__':
    app.run(debug=True)
