from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from flask import request

from db import db
from models import LaserCutterRepairModel
from schemas import LaserCutterRepairSchema


blp = Blueprint("Laser_repairs", __name__, description="Operations on laser repairs")


@blp.route("/laser_repair/<int:repair_id>")
class workerOrders(MethodView):
    @blp.response(200, LaserCutterRepairSchema)
    def get(self, repair_id):
        laser_repair = LaserCutterRepairModel.query.get_or_404(repair_id)
        return laser_repair

    def delete(self, repair_id):
        order = LaserCutterRepairModel.query.get_or_404(repair_id)
        try:
            db.session.delete(order)
            db.session.commit()
            return {"message": "order deleted."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

    def put(self, repair_id):
        order = LaserCutterRepairModel.query.get_or_404(repair_id)
        data = request.get_json()

        order.date_of_repair = data.get("date_of_repair", order.date_of_repair)
        order.laser_cutter_id = data.get("laser_cutter_id", order.laser_cutter_id)
        order.worker_id = data.get("worker_id", order.worker_id)

        try:
            db.session.commit()
            return {"message": "order updated successfully."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

@blp.route("/laser_repair")
class laser_repairPost(MethodView):
    def post(self):
        data = request.get_json()

        new_laser_repair = LaserCutterRepairModel(
            laser_cutter_id=data["laser_cutter_id"],
            date_of_repair=data["date_of_repair"],
            worker_id=data["worker_id"],
        )

        try:
            db.session.add(new_laser_repair)
            db.session.commit()

            laser_repair_schema = LaserCutterRepairSchema()
            return laser_repair_schema.dump(new_laser_repair), 201

        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400


@blp.route("/laser_repair/worker/<int:worker_id>")
class worker(MethodView):
    @blp.response(200, LaserCutterRepairSchema(many=True))
    def get(self, worker_id):
        laser_repairs = LaserCutterRepairModel.query.filter(LaserCutterRepairModel.worker_id == worker_id).all()
        return laser_repairs


@blp.route("/laser_repairs")
class GetAllworkerOrders(MethodView):
    @blp.response(200, LaserCutterRepairSchema(many=True))
    def get(self):
        return LaserCutterRepairModel.query.all()
