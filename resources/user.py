from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text

from db import db
from models import UserModel
from schemas import UserSchema


blp = Blueprint("Users", __name__, description="Operations on users")


@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

    def put(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        data = request.get_json()

        user.name = data.get("name", user.name)
        user.surname = data.get("surname", user.surname)
        user.email = data.get("email", user.email)
        user.team_id = data.get("team_id", user.team_id)

        db.session.commit()

        return {"message": "User updated successfully."}, 200


@blp.route("/user")
class UserPost(MethodView):
    def post(self):
        data = request.get_json()

        new_user = UserModel(
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            team_id=data.get("team_id")
        )

        try:
            db.session.add(new_user)
            db.session.commit()

            user_schema = UserSchema()
            return user_schema.dump(new_user), 201

        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400


@blp.route("/users")
class GetUsers(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()


@blp.route("/users/team/<int:team_id>")
class TempGetUsers(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self, team_id):
        users = UserModel.query.filter(UserModel.team_id == team_id).all()
        return users


@blp.route("/user/raw", methods=["POST"])
class UserRawInsert(MethodView):
    def post(self):
        data = request.get_json()
        
        sql_query = text("""
            INSERT INTO user (name, surname, email, team_id) 
            VALUES (:name, :surname, :email, :team_id)
        """)
        
        try:
            db.session.execute(sql_query, {
                "name": data["name"],
                "surname": data["surname"],
                "email": data["email"],
                "team_id": data.get("team_id")
            })
            db.session.commit()
            return {"message": "User inserted successfully."}, 201
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400