import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from LabManager import app, db, bcrypt
from LabManager.dbModels import User
from LabManager.auth.forms import RegistrationForm, LoginForm, UpdateAccountForm
from LabManager.auth.utils import save_profile_picture


auth = Blueprint("auth", __name__)


@auth.route("/logon", methods=["GET", "POST"])
def logon():
    form_signUp = RegistrationForm()
    form_signIn = LoginForm()

    # Account successfully created
    if form_signUp.submit_signUp.data and form_signUp.validate():
        new_person = Person(first_name=None, last_name=None, middle_name=None,
                            sex=None, birthday=None, occupation=None, institution=None,
                            timedelta=None)
        db.session.add(new_person)
        db.session.commit()

        hashed_password = bcrypt.generate_password_hash(form_signUp.password.data).decode("utf-8")
        new_user = User(username=form_signUp.username.data, email=form_signUp.email.data,
                        password=hashed_password, own_info=new_person)
        db.session.add(new_user)
        db.session.commit()
        
        flash(f"Account created for {form_signUp.username.data}. You can now Log In.", "success")
        return redirect(url_for("main.home"))
    
    # User successfully logged in
    if form_signIn.submit_signIn.data and form_signIn.validate():
        user = User.query.filter_by(email=form_signIn.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_signIn.password.data):
            login_user(user, remember=form_signIn.remember_me.data)
            next_page = request.args.get("next")
            flash("You have been logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Invalid credentials. Please check your email and password.", "error")

    return render_template("logon.html", title="User Login",
                            form_signUp=form_signUp, form_signIn=form_signIn)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@auth.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    user = User.query.filter_by(username=current_user.username).first()
    person_data = user.own_info

    requires_update = True if (person_data.first_name == None) else False


    if form.submit.data and form.validate():

        if form.picture.data:
            image_filepath = os.path.join(app.root_path, person_data.image_filepath)
            picture, path = save_profile_picture(form.picture.data, image_filepath)
            person_data.image_file = picture
            person_data.image_filepath = path

        current_user.username = form.username.data
        current_user.email = form.email.data
        person_data.first_name = form.first_name.data
        person_data.middle_name = form.middle_name.data
        person_data.last_name = form.last_name.data
        person_data.sex = form.sex.data
        person_data.birthday = form.birthday.data
        person_data.phone = form.phone.data
        person_data.occupation = form.occupation.data
        person_data.institution = form.institution.data

        db.session.add(current_user)
        db.session.add(person_data)
        db.session.commit()
        flash("You account information has been updated.", "success")

        return redirect(url_for("auth.account"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = person_data.first_name
        form.middle_name.data = person_data.middle_name
        form.last_name.data = person_data.last_name
        form.birthday.data = person_data.birthday
        form.sex.data = person_data.sex
        form.phone.data = person_data.phone
        form.occupation.data = person_data.occupation
        form.institution.data = person_data.institution


    image_file = url_for("static", filename="profile_pics/" + person_data.image_file)

    return render_template("account.html", title="User Account",
                            image_file=image_file, form=form,
                            requires_update=requires_update)
