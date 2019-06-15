from flask import Blueprint, render_template


news = Blueprint("news", __name__)


@news.route("/news")
def lab_news():
    return render_template("news.html", title="News")

