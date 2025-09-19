from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from flask import request

from db import db
from models import LaserCutterOrderModel, UserModel
from schemas import LaserCutterOrderSchema


blp = Blueprint("Laser_orders", __name__, description="Operations on laser orders")


@blp.route("/laser_order/<int:order_id>")
class UserOrders(MethodView):
    @blp.response(200, LaserCutterOrderSchema)
    def get(self, order_id):
        laser_order = LaserCutterOrderModel.query.get_or_404(order_id)
        return laser_order

    def delete(self, order_id):
        order = LaserCutterOrderModel.query.get_or_404(order_id)
        try:
            db.session.delete(order)
            db.session.commit()
            return {"message": "order deleted."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

    def put(self, order_id):
        order = LaserCutterOrderModel.query.get_or_404(order_id)
        data = request.get_json()

        order.laser_cutter_id = data.get("laser_cutter_id", order.laser_cutter_id)
        order.time_of_end = data.get("time_of_end", order.time_of_end)
        order.time_of_start = data.get("time_of_start", order.time_of_start)
        order.user_id = data.get("user_id", order.user_id)

        try:
            db.session.commit()
            return {"message": "order updated successfully."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

@blp.route("/laser_order")
class laser_orderPost(MethodView):
    def post(self):
        data = request.get_json()

        new_laser_order = LaserCutterOrderModel(
            laser_cutter_id=data["laser_cutter_id"],
            time_of_end=data["time_of_end"],
            time_of_start=data["time_of_start"],
            user_id=data["user_id"],
        )

        try:
            db.session.add(new_laser_order)
            db.session.commit()

            laser_order_schema = LaserCutterOrderSchema()
            return laser_order_schema.dump(new_laser_order), 201

        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400


@blp.route("/laser_order/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, LaserCutterOrderSchema(many=True))
    def get(self, user_id):
        laser_orders = LaserCutterOrderModel.query.filter(LaserCutterOrderModel.user_id == user_id).all()
        return laser_orders

@blp.route("/laser_order/team/<int:team_id>")
class TeamOrders(MethodView):
    @blp.response(200, LaserCutterOrderSchema(many=True))
    def get(self, team_id):
        users = UserModel.query.filter(UserModel.team_id == team_id).all()
        users_id = [user.id for user in users]
        team_orders = []
        for user_id in users_id:
            for order in LaserCutterOrderModel.query.filter(LaserCutterOrderModel.user_id == user_id).all():
                team_orders.append(order)
        return team_orders

@blp.route("/laser_orders")
class GetAllUserOrders(MethodView):
    @blp.response(200, LaserCutterOrderSchema(many=True))
    def get(self):
        return LaserCutterOrderModel.query.all()
