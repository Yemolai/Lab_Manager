import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from LabManager import app, db, bcrypt
from LabManager.forms import RegistrationForm, LoginForm, UpdateAccountForm
from LabManager.dbModels import *


def save_profile_picture(form_picture, image_path):
    """
    Logic to update account pictures. Used on the '/account'
    route. Generates random filename and concatenates to the
    original file extensions before saving it to the system.
    Also resizes the image using the Pillow Package. Returns
    the filename to be applied on the database.
    """
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    pic_filename = random_hex + file_ext
    pic_path = os.path.join(app.root_path, "static/profile_pics", pic_filename)
    
    if image_path != os.path.join(app.root_path, "static/profile_pics", "default.jpg"):
        os.remove(image_path)

    output_size = (125, 125)
    output_pic = Image.open(form_picture)
    output_pic.thumbnail(output_size)
    
    output_pic.save(pic_path)

    return pic_filename, os.path.join("static/profile_pics", pic_filename)


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


@app.route("/notices/new", methods=["GET", "POST"])
@login_required
def add_notice():
    return render_template("add_notice.html", title="New Notice")


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

    return render_template("logon.html", title="User Login",
                            form_signUp=form_signUp, form_signIn=form_signIn)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account", methods=["GET", "POST"])
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

        return redirect(url_for("account"))

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
