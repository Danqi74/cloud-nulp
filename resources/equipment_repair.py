from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from flask import request

from db import db
from models import EquipmentRepairModel
from schemas import EquipmentRepairSchema


blp = Blueprint("Equipment_repairs", __name__, description="Operations on equipment repairs")


@blp.route("/equipment_repair/<int:repair_id>")
class workerOrders(MethodView):
    @blp.response(200, EquipmentRepairSchema)
    def get(self, repair_id):
        equipment_repair = EquipmentRepairModel.query.get_or_404(repair_id)
        return equipment_repair

    def delete(self, repair_id):
        order = EquipmentRepairModel.query.get_or_404(repair_id)
        try:
            db.session.delete(order)
            db.session.commit()
            return {"message": "order deleted."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

    def put(self, repair_id):
        order = EquipmentRepairModel.query.get_or_404(repair_id)
        data = request.get_json()

        order.date_of_repair = data.get("date_of_repair", order.date_of_repair)
        order.equipment_id = data.get("equipment_id", order.equipment_id)
        order.worker_id = data.get("worker_id", order.worker_id)

        try:
            db.session.commit()
            return {"message": "order updated successfully."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

@blp.route("/equipment_repair")
class equipment_repairPost(MethodView):
    def post(self):
        data = request.get_json()

        new_equipment_repair = EquipmentRepairModel(
            equipment_id=data["equipment_id"],
            date_of_repair=data["date_of_repair"],
            worker_id=data["worker_id"],
        )

        try:
            db.session.add(new_equipment_repair)
            db.session.commit()

            equipment_repair_schema = EquipmentRepairSchema()
            return equipment_repair_schema.dump(new_equipment_repair), 201

        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400


@blp.route("/equipment_repair/worker/<int:worker_id>")
class worker(MethodView):
    @blp.response(200, EquipmentRepairSchema(many=True))
    def get(self, worker_id):
        equipment_repairs = EquipmentRepairModel.query.filter(EquipmentRepairModel.worker_id == worker_id).all()
        return equipment_repairs


@blp.route("/equipment_repairs")
class GetAllworkerOrders(MethodView):
    @blp.response(200, EquipmentRepairSchema(many=True))
    def get(self):
        return EquipmentRepairModel.query.all()
