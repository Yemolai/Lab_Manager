from flask import Blueprint, render_template
from flask_login import login_required


calendar = Blueprint("calendar", __name__)


@calendar.route("/calendar")
@login_required
def lab_calendar():
    return render_template("calendar.html", title="Calendar")
