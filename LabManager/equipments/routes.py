from flask import Blueprint, render_template
from flask_login import login_required


equipments = Blueprint("equips", __name__)


@equipments.route("/inventory")
@login_required
def inventory():
    return render_template("inventory.html", title="Equipment Inventory")


@equipments.route("/lendings")
@login_required
def lendings():
    return render_template("lendings.html", title="Equipment Lendings")


@equipments.route("/technical")
@login_required
def technical():
    return render_template("technical.html", title="Technical Issues")
