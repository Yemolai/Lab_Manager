from flask import Flask, render_template, url_for

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
