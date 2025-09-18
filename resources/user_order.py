from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from flask import request

from db import db
from models import UserOrderModel, UserModel, EquipmentModel
from schemas import UserOrderSchema

from datetime import datetime


blp = Blueprint("User_orders", __name__, description="Operations on orders")


@blp.route("/user_order/<int:order_id>")
class UserOrders(MethodView):
    @blp.response(200, UserOrderSchema)
    def get(self, order_id):
        user_order = UserOrderModel.query.get_or_404(order_id)
        return user_order

    def delete(self, order_id):
        order = UserOrderModel.query.get_or_404(order_id)
        try:
            db.session.delete(order)
            db.session.commit()
            return {"message": "order deleted."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

    def put(self, order_id):
        order = UserOrderModel.query.get_or_404(order_id)
        data = request.get_json()

        order.equipment_id = data.get("equipment_id", order.equipment_id)
        order.time_of_order = data.get("time_of_order", order.time_of_order)
        order.user_id = data.get("user_id", order.user_id)

        try:
            db.session.commit()
            return {"message": "order updated successfully."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400


@blp.route("/user_order")
class user_orderPost(MethodView):
    def post(self):
        data = request.get_json()

        new_user_order = UserOrderModel(
            equipment_id=data["equipment_id"],
            time_of_order=data["time_of_order"],
            user_id=data["user_id"],
        )

        try:
            db.session.add(new_user_order)
            db.session.commit()

            user_order_schema = UserOrderSchema()
            return user_order_schema.dump(new_user_order), 201

        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400


@blp.route("/user_order/str")
class user_order_by_str(MethodView):
    def post(self):
        data = request.get_json()

        user = UserModel.query.filter_by(name=data["user_name"], surname=data["user_surname"]).first()
        if not user:
            abort(404, message="User not found.")

        equipment = EquipmentModel.query.filter_by(serial_number=data["equipment_serial_number"]).first()
        if not equipment:
            abort(404, message="Equipment not found.")

        try:
            current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            new_link = UserOrderModel(user_id=user.id, equipment_id=equipment.id, time_of_order=current_time)
            db.session.add(new_link)
            db.session.commit()
            return {"message": "Link created successfully."}, 201
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Error creating link: {}".format(e.orig)}, 400


@blp.route("/user_order/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserOrderSchema(many=True))
    def get(self, user_id):
        user_orders = UserOrderModel.query.filter(UserOrderModel.user_id == user_id).all()
        return user_orders

@blp.route("/user_order/team/<int:team_id>")
class TeamOrders(MethodView):
    @blp.response(200, UserOrderSchema(many=True))
    def get(self, team_id):
        users = UserModel.query.filter(UserModel.team_id == team_id).all()
        users_id = [user.id for user in users]
        team_orders = []
        for user_id in users_id:
            for order in UserOrderModel.query.filter(UserOrderModel.user_id == user_id).all():
                team_orders.append(order)
        return team_orders

@blp.route("/user_orders")
class GetAllUserOrders(MethodView):
    @blp.response(200, UserOrderSchema(many=True))
    def get(self):
        return UserOrderModel.query.all()
