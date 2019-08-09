from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from LabManager import db
from LabManager.dbModels import Inventory, Lendings, TechnicalIssues
from LabManager.maSchemas import equipment_schema, equipments_schema


equipments = Blueprint("equips", __name__)


@equipments.route("/inventory")
@login_required
def inventory():
    return render_template("inventory.html", title="Equipment Inventory")


@equipments.route("/inventory/all", methods=["GET"])
def inventory_all():
    inventory = Inventory.query.all()
    result = equipments_schema.dump(inventory)

    return jsonify(result.data)


@equipments.route("/inventory/<id>", methods=["GET"])
def inventory_fetch(id):
    equipment = Inventory.query.get(id)
    result = equipment_schema.dump(equipment)

    return jsonify(result.data)


@equipments.route("/inventory/add", methods=["POST"])
def inventory_add():
    name = request.json["name"]
    description = request.json["description"]
    new_equip = Inventory(name=name, description=description)
    db.session.add(new_equip)
    db.session.commit()

    return equipment_schema.jsonify(new_equip)


@equipments.route("/inventory/update/<id>", methods=["PUT"])
def inventory_put(id):
    equipment = Inventory.query.get(id)
    name = request.json["name"]
    description = request.json["description"]
    equipment.name = name
    equipment.description = description
    db.session.commit()

    return equipment_schema.jsonify(equipment)


@equipments.route("/inventory/delete/<id>", methods=["DELETE"])
def inventory_del(id):
    equipment = Inventory.query.get(id)
    db.session.delete(equipment)
    db.session.commit()

    return equipment_schema.jsonify(equipment)


@equipments.route("/lendings")
@login_required
def lendings():
    return render_template("lendings.html", title="Equipment Lendings")


@equipments.route("/technical")
@login_required
def technical():
    return render_template("technical.html", title="Technical Issues")
