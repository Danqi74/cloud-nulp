from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from sqlalchemy.exc import IntegrityError

from db import db
from models import EquipmentTypeModel
from schemas import EquipmentTypeSchema


blp = Blueprint("Equipment_type", __name__, description="Operations on equipment types")


@blp.route("/equipment_type/<int:equipment_type_id>")
class equipment_type(MethodView):

    @blp.response(200, EquipmentTypeSchema)
    def get(self, equipment_type_id):
        equipment_type = EquipmentTypeModel.query.get_or_404(equipment_type_id)
        return equipment_type

    def delete(self, equipment_type_id):
        equipment_type = EquipmentTypeModel.query.get_or_404(equipment_type_id)
        try:
            db.session.delete(equipment_type)
            db.session.commit()
            return {"message": "equipment_type deleted."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

    def put(self, equipment_type_id):
        equipment_type = EquipmentTypeModel.query.get_or_404(equipment_type_id)
        data = request.get_json()

        equipment_type.name = data.get("name", equipment_type.name)

        db.session.commit()

        return {"message": "equipment_type updated successfully."}, 200


@blp.route("/equipment_type")
class equipment_typePost(MethodView):
    def post(self):
        data = request.get_json()

        new_equipment_type = EquipmentTypeModel(
            name=data["name"],
        )

        try:
            db.session.add(new_equipment_type)
            db.session.commit()

            equipment_type_schema = EquipmentTypeSchema()
            return equipment_type_schema.dump(new_equipment_type), 201

        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400


@blp.route("/equipment_types")
class GetAllequipment_types(MethodView):
    @blp.response(200, EquipmentTypeSchema(many=True))
    def get(self):
        return EquipmentTypeModel.query.all()