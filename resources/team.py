from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from sqlalchemy.exc import IntegrityError

from db import db
from models import TeamModel
from schemas import TeamSchema


blp = Blueprint("Teams", __name__, description="Operations on teams")


@blp.route("/team/<int:team_id>")
class Team(MethodView):

    @blp.response(200, TeamSchema)
    def get(self, team_id):
        team = TeamModel.query.get_or_404(team_id)
        return team

    def delete(self, team_id):
        team = TeamModel.query.get_or_404(team_id)
        try:
            db.session.delete(team)
            db.session.commit()
            return {"message": "team deleted."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

    def put(self, team_id):
        team = TeamModel.query.get_or_404(team_id)
        data = request.get_json()

        team.name = data.get("name", team.name)

        db.session.commit()

        return {"message": "team updated successfully."}, 200


@blp.route("/team")
class TeamPost(MethodView):
    def post(self):
        data = request.get_json()

        new_team = TeamModel(
            name=data["name"],
        )

        try:
            db.session.add(new_team)
            db.session.commit()

            team_schema = TeamSchema()
            return team_schema.dump(new_team), 201

        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400


@blp.route("/teams")
class GetAllTeams(MethodView):
    @blp.response(200, TeamSchema(many=True))
    def get(self):
        return TeamModel.query.all()


@blp.route('/team/insert')
class insert_records(MethodView):
    def post(self):
        try:
            for i in range(1, 11):
                record = TeamModel(name=f"Noname{i}")
                db.session.add(record)
            db.session.commit()
            return {"message": f"10 records inserted into team in column name"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500