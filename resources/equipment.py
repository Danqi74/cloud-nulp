from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from flask import request
from flask_jwt_extended import jwt_required

from db import db
from models import EquipmentModel
from schemas import EquipmentSchema


blp = Blueprint("Equipments", __name__, description="Operations on equipment")


@blp.route("/equipment/<int:equipment_id>")
class UserEquipments(MethodView):
    @jwt_required()
    @blp.response(200, EquipmentSchema)
    def get(self, equipment_id):
        equipment = EquipmentModel.query.get_or_404(equipment_id)
        return equipment

    @jwt_required()
    def delete(self, equipment_id):
        equipment = EquipmentModel.query.get_or_404(equipment_id)
        try:
            db.session.delete(equipment)
            db.session.commit()
            return {"message": "equipment deleted."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

    @jwt_required()
    def put(self, equipment_id):
        equipment = EquipmentModel.query.get_or_404(equipment_id)
        data = request.get_json()

        equipment.equipment_condition_id = data.get("equipment_condition_id", equipment.equipment_condition_id)
        equipment.equipment_type_id = data.get("equipment_type_id", equipment.equipment_type_id)
        equipment.model = data.get("model", equipment.model)
        equipment.serial_number = data.get("serial_number", equipment.serial_number)

        try:
            db.session.commit()
            return {"message": "equipment updated successfully."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

@blp.route("/equipment")
class equipmentPost(MethodView):
    @jwt_required()
    def post(self):
        data = request.get_json()

        new_equipment = EquipmentModel(
            equipment_condition_id=data["equipment_condition_id"],
            equipment_type_id=data["equipment_type_id"],
            model=data["model"],
            serial_number=data["serial_number"],
        )

        try:
            db.session.add(new_equipment)
            db.session.commit()

            equipment_schema = EquipmentSchema()
            return equipment_schema.dump(new_equipment), 201

        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400


@blp.route("/equipments")
class GetAllequipments(MethodView):
    @jwt_required()
    @blp.response(200, EquipmentSchema(many=True))
    def get(self):
        return EquipmentModel.query.all()
