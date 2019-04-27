from flask import render_template, url_for, flash, redirect
from LabManager import app
from LabManager.logon import RegistrationForm, LoginForm
from LabManager.dbModels import User, Frequency_Event, Lending_Event, Technical_Issues, Notice

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
