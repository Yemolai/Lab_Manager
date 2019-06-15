from flask import Blueprint, render_template
from flask_login import login_required


personnel = Blueprint("personnel", __name__)


@personnel.route("/personnel")
@login_required
def lab_personnel():
    return render_template("personnel.html", title="Laboratory Personnel")

@personnel.route("/frequency")
@login_required
def frequency():
    return render_template("frequency.html", title="Laboratory Frequency")
