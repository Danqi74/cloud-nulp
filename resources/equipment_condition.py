from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from sqlalchemy.exc import IntegrityError

from db import db
from models import EquipmentConditionModel
from schemas import EquipmentConditionSchema


blp = Blueprint("Equipment_condition", __name__, description="Operations on equipment conditions")


@blp.route("/equipment_condition/<int:equipment_condition_id>")
class equipment_condition(MethodView):

    @blp.response(200, EquipmentConditionSchema)
    def get(self, equipment_condition_id):
        equipment_condition = EquipmentConditionModel.query.get_or_404(equipment_condition_id)
        return equipment_condition

    def delete(self, equipment_condition_id):
        equipment_condition = EquipmentConditionModel.query.get_or_404(equipment_condition_id)
        try:
            db.session.delete(equipment_condition)
            db.session.commit()
            return {"message": "equipment_condition deleted."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

    def put(self, equipment_condition_id):
        equipment_condition = EquipmentConditionModel.query.get_or_404(equipment_condition_id)
        data = request.get_json()

        equipment_condition.name = data.get("name", equipment_condition.name)

        db.session.commit()

        return {"message": "equipment_condition updated successfully."}, 200


@blp.route("/equipment_condition")
class equipment_conditionPost(MethodView):
    def post(self):
        data = request.get_json()

        new_equipment_condition = EquipmentConditionModel(
            name=data["name"],
        )

        try:
            db.session.add(new_equipment_condition)
            db.session.commit()

            equipment_condition_schema = EquipmentConditionSchema()
            return equipment_condition_schema.dump(new_equipment_condition), 201

        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400


@blp.route("/equipment_conditions")
class GetAllequipment_conditions(MethodView):
    @blp.response(200, EquipmentConditionSchema(many=True))
    def get(self):
        return EquipmentConditionModel.query.all()