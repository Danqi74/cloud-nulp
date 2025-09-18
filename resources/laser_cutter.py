from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from flask import request

from db import db
from models import LaserCutterModel
from schemas import LaserCutterSchema


blp = Blueprint("Laser_cutters", __name__, description="Operations on laser cutters")


@blp.route("/laser_cutter/<int:laser_id>")
class Userlasers(MethodView):
    @blp.response(200, LaserCutterSchema)
    def get(self, laser_id):
        laser_cutter = LaserCutterModel.query.get_or_404(laser_id)
        return laser_cutter

    def delete(self, laser_id):
        laser = LaserCutterModel.query.get_or_404(laser_id)
        try:
            db.session.delete(laser)
            db.session.commit()
            return {"message": "laser deleted."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

    def put(self, laser_id):
        laser = LaserCutterModel.query.get_or_404(laser_id)
        data = request.get_json()

        laser.equipment_condition_id = data.get("equipment_condition_id", laser.equipment_condition_id)
        laser.model = data.get("model", laser.model)
        laser.serial_number = data.get("serial_number", laser.serial_number)

        try:
            db.session.commit()
            return {"message": "laser updated successfully."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

@blp.route("/laser_cutter")
class laser_cutterPost(MethodView):
    def post(self):
        data = request.get_json()

        new_laser_cutter = LaserCutterModel(
            equipment_condition_id=data["equipment_condition_id"],
            model=data["model"],
            serial_number=data["serial_number"],
        )

        try:
            db.session.add(new_laser_cutter)
            db.session.commit()

            laser_cutter_schema = LaserCutterSchema()
            return laser_cutter_schema.dump(new_laser_cutter), 201

        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400


@blp.route("/laser_cutters")
class GetAllLasers(MethodView):
    @blp.response(200, LaserCutterSchema(many=True))
    def get(self):
        return LaserCutterModel.query.all()
