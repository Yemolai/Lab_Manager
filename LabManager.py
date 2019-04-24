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

@app.route("/logon", methods=["GET", "POST"])
def logon():
    form_signUp = RegistrationForm()
    form_signIn = LoginForm()
    if form_signUp.submit_signUp.data and form_signUp.validate():
        flash(f"Account created for {form_signUp.username.data}. You can now Log In.", "success")
        return redirect(url_for("home"))
    if form_signIn.submit_signIn.data and form_signIn.validate():
        if form_signIn.email.data == "dummyemail@email.com" and form_signIn.password.data == "password": #Change this to appropriate database calls
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check your credentials.", "error")
    return render_template("logon.html", title="User Login", form_signUp=form_signUp, form_signIn=form_signIn)

if __name__ == '__main__':
    app.run(debug=True)
