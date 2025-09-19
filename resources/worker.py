from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from sqlalchemy.exc import IntegrityError

from db import db
from models import WorkerModel
from schemas import WorkerSchema


blp = Blueprint("Workers", __name__, description="Operations on workers")


@blp.route("/worker/<int:worker_id>")
class Worker(MethodView):

    @blp.response(200, WorkerSchema)
    def get(self, worker_id):
        worker = WorkerModel.query.get_or_404(worker_id)
        return worker

    def delete(self, worker_id):
        worker = WorkerModel.query.get_or_404(worker_id)
        try:
            db.session.delete(worker)
            db.session.commit()
            return {"message": "Worker deleted."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

    def put(self, worker_id):
        worker = WorkerModel.query.get_or_404(worker_id)
        data = request.get_json()

        worker.name = data.get("name", worker.name)
        worker.surname = data.get("surname", worker.surname)
        worker.email = data.get("email", worker.email)
        worker.address = data.get("address", worker.address)
        worker.phone_number = data.get("phone_number", worker.phone_number)
        worker.worker_position_id = data.get("worker_position_id", worker.worker_position_id)

        db.session.commit()

        return {"message": "worker updated successfully."}, 200


@blp.route("/worker")
class WorkerPost(MethodView):
    def post(self):
        data = request.get_json()

        new_worker = WorkerModel(
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            address=data["address"],
            phone_number=data["phone_number"],
            worker_position_id=data["worker_position_id"]
        )

        try:
            db.session.add(new_worker)
            db.session.commit()

            worker_schema = WorkerSchema()
            return worker_schema.dump(new_worker), 201

        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400


@blp.route("/workers")
class GetAllWorkers(MethodView):
    @blp.response(200, WorkerSchema(many=True))
    def get(self):
        return WorkerModel.query.all()