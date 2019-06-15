from flask import Blueprint, render_template
from flask_login import login_required


notices = Blueprint("notices", __name__)


@notices.route("/notices")
@login_required
def lab_notices():
    return render_template("notices.html", title="Notice Board")


@notices.route("/notices/new", methods=["GET", "POST"])
@login_required
def add_notice():
    return render_template("add_notice.html", title="New Notice")
