from flask import Blueprint, render_template
from flask_login import login_required


fieldtrips = Blueprint("fieldtrips", __name__)


@fieldtrips.route("/fieldtrips")
@login_required
def lab_fieldtrips():
    return render_template("fieldtrips.html", title="Field Trips")
