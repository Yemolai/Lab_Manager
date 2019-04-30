from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from LabManager import app, db, bcrypt
from LabManager.logon import RegistrationForm, LoginForm
from LabManager.dbModels import User, Frequency_Event, Lending_Event, Technical_Issues, Notice

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/frequency")
@login_required
def frequency():
    return render_template("frequency.html", title="Laboratory Frequency")

@app.route("/personnel")
@login_required
def personnel():
    return render_template("personnel.html", title="Laboratory Personnel")

@app.route("/lendings")
@login_required
def lendings():
    return render_template("lendings.html", title="Equipment Lendings")

@app.route("/technical")
@login_required
def technical():
    return render_template("technical.html", title="Technical Issues")

@app.route("/inventory")
@login_required
def inventory():
    return render_template("inventory.html", title="Equipment Inventory")

@app.route("/fieldtrips")
@login_required
def fieldtrips():
    return render_template("fieldtrips.html", title="Field Trips")

@app.route("/notices")
@login_required
def notices():
    return render_template("notices.html", title="Notice Board")

@app.route("/news")
def news():
    return render_template("news.html", title="News")

@app.route("/calendar")
@login_required
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
        hashed_password = bcrypt.generate_password_hash(form_signUp.password.data).decode("utf-8")
        new_user = User(username=form_signUp.username.data, email=form_signUp.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Account created for {form_signUp.username.data}. You can now Log In.", "success")
        return redirect(url_for("home"))
    
    # User successfully logged in
    if form_signIn.submit_signIn.data and form_signIn.validate():
        user = User.query.filter_by(email=form_signIn.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_signIn.password.data):
            login_user(user, remember=form_signIn.remember_me.data)
            next_page = request.args.get("next")
            flash("You have been logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Invalid credentials. Please check your email and password.", "error")

    return render_template("logon.html", title="User Login", form_signUp=form_signUp, form_signIn=form_signIn)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="User Account")
