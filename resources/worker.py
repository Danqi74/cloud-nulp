from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from sqlalchemy.exc import IntegrityError

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    jwt_required,
)
from passlib.hash import pbkdf2_sha256

from db import db
from models import WorkerModel
from schemas import WorkerSchema, LoginSchema, WorkerRegisterSchema
from blocklist import BLOCKLIST


blp = Blueprint("Workers", __name__, description="Operations on workers")


@blp.route("/worker/<int:worker_id>")
class Worker(MethodView):
    @jwt_required()
    @blp.response(200, WorkerSchema)
    def get(self, worker_id):
        worker = WorkerModel.query.get_or_404(worker_id)
        return worker

    @jwt_required()
    def delete(self, worker_id):
        worker = WorkerModel.query.get_or_404(worker_id)
        try:
            db.session.delete(worker)
            db.session.commit()
            return {"message": "Worker deleted."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

    @blp.arguments(WorkerSchema, required=False)
    def put(self, data, worker_id):
        worker = WorkerModel.query.get_or_404(worker_id)

        worker.name = data.get("name", worker.name)
        worker.surname = data.get("surname", worker.surname)
        worker.email = data.get("email", worker.email)
        worker.address = data.get("address", worker.address)
        worker.phone_number = data.get("phone_number", worker.phone_number)
        worker.worker_position_id = data.get("worker_position_id", worker.worker_position_id)

        db.session.commit()

        return {"message": "worker updated successfully."}, 200


@blp.route("/register")
class WorkerPost(MethodView):
    @blp.arguments(WorkerRegisterSchema, required=True)
    def post(self, data):
        new_worker = WorkerModel(
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            password=pbkdf2_sha256.hash(data["password"]),
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


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, data):
        worker = WorkerModel.query.filter(
            WorkerModel.email == data["email"]
        ).first()

        if worker and pbkdf2_sha256.verify(data["password"], worker.password):
            access_token = create_access_token(identity=str(worker.id), fresh=True)
            refresh_token = create_refresh_token(str(worker.id))
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class WorkerLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

@blp.route("/workers")
class GetAllWorkers(MethodView):
    @jwt_required()
    @blp.response(200, WorkerSchema(many=True))
    def get(self):
        return WorkerModel.query.all()