from db import db

class LaserCutterOrderEvaluationModel(db.Model):
    __tablename__ = 'laser_cutter_order_evaluation'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    quality_score = db.Column(db.Integer, nullable=False)