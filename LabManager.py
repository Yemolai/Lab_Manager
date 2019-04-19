from flask import Flask, render_template, url_for, flash, redirect
from logon import RegistrationForm, LoginForm

app = Flask(__name__)

app.config["SECRET_KEY"] = 'changeme' #Mandatory to change this on deploy

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

@app.route("/register", methods=["GET", "POST"])
def register():
    #Create instance of form to send to the application
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}.", "flash-success")
        return redirect(url_for("home"))
    #Pass the form as an argument to render_template()
    return render_template("signup.html", title="User Registration", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "dummyemail@email.com" and form.password.data == "password": #Change this to appropriate database calls
            flash("You have been logged in!", "flash-success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check credentials.", "flash-fail")
    return render_template("signin.html", title="User Login", form=form)

if __name__ == '__main__':
    app.run(debug=True)
