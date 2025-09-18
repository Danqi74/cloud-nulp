from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from flask import request

from db import db
from models import LaserCutterOrderEvaluationModel
from schemas import LaserCutterOrderEvaluationSchema


blp = Blueprint("Laser_orders_evaluation", __name__, description="Operations on laser orders")

@blp.route("/laser_evaluation/<int:id>")
class LaserCutterOrderEvaluation(MethodView):

    @blp.response(200, LaserCutterOrderEvaluationSchema)
    def get(self, id):
        evaluation = LaserCutterOrderEvaluationModel.query.get_or_404(id)
        return evaluation

    def delete(self, id):
        evaluation = LaserCutterOrderEvaluationModel.query.get_or_404(id)
        try:
            db.session.delete(evaluation)
            db.session.commit()
            return {"message": "evaluation deleted."}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400

    def put(self, id):
        evaluation = LaserCutterOrderEvaluationModel.query.get_or_404(id)
        data = request.get_json()

        evaluation.quality_score = data.get("quality_score", evaluation.quality_score)

        db.session.commit()

        return {"message": "evaluation updated successfully."}, 200


@blp.route("/laser_evaluation")
class LaserCutterOrderEvaluationPost(MethodView):
    def post(self):
        data = request.get_json()

        new_evaluation = LaserCutterOrderEvaluationModel(
            order_id=data["order_id"],
            quality_score=data["quality_score"],
        )

        try:
            db.session.add(new_evaluation)
            db.session.commit()

            evaluation_schema = LaserCutterOrderEvaluationSchema()
            return evaluation_schema.dump(new_evaluation), 201

        except IntegrityError as e:
            db.session.rollback()
            return {"message": "Unique constraint violation: {}".format(e.orig)}, 400


@blp.route("/laser_evaluations")
class GetAllLaserCutterOrderEvaluations(MethodView):
    @blp.response(200, LaserCutterOrderEvaluationSchema(many=True))
    def get(self):
        return LaserCutterOrderEvaluationModel.query.all()

def get_column_stat(operation):
    table = LaserCutterOrderEvaluationModel
    if not table:
        return None

    column = getattr(table, "quality_score", None)

    if column is None:
        return None

    if operation == 'MAX':
        result = db.session.query(func.max(column)).scalar()
    elif operation == 'MIN':
        result = db.session.query(func.min(column)).scalar()
    elif operation == 'SUM':
        result = db.session.query(func.sum(column)).scalar()
    elif operation == 'AVG':
        result = db.session.query(func.avg(column)).scalar()
    else:
        return None

    return result

@blp.route("/laser_evaluation/stat")
class GetColumnStat(MethodView):
    def get(self):
        data = request.get_json()

        result = get_column_stat(data["operation"])

        if result is None:
            return {'message': 'Invalid table, column, or operation.'}, 400

        return {'result': result}, 200