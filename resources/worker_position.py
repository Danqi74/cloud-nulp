from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from sqlalchemy.exc import IntegrityError

from db import db
from models import WorkerPositionModel
from schemas import WorkerPositionSchema


blp = Blueprint("Workers_position", __name__, description="Operations on worker positions")


@blp.route("/worker_position/<int:worker_position_id>")
class WorkerPosition(MethodView):

    @blp.response(200, WorkerPositionSchema)
    def get(self, worker_position_id):
        worker_position = WorkerPositionModel.query.get_or_404(worker_position_id)
        return worker_position

    def delete(self, worker_position_id):
        worker_position = WorkerPositionModel.query.get_or_404(worker_position_id)
        try:
            db.session.delete(worker_position)
            db.session.commit()
            return {"message": "worker_position deleted."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

    def put(self, worker_position_id):
        worker_position = WorkerPositionModel.query.get_or_404(worker_position_id)
        data = request.get_json()

        worker_position.name = data.get("name", worker_position.name)

        db.session.commit()

        return {"message": "worker_position updated successfully."}, 200


@blp.route("/worker_position")
class WorkerPositionPost(MethodView):
    def post(self):
        data = request.get_json()

        new_worker_position = WorkerPositionModel(
            name=data["name"],
        )

        try:
            db.session.add(new_worker_position)
            db.session.commit()

            worker_position_schema = WorkerPositionSchema()
            return worker_position_schema.dump(new_worker_position), 201

        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400


@blp.route("/worker_positions")
class GetAllWorkerPositions(MethodView):
    @blp.response(200, WorkerPositionSchema(many=True))
    def get(self):
        return WorkerPositionModel.query.all()