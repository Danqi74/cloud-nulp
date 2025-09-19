from db import db

class WorkerModel(db.Model):
    __tablename__ = 'worker'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15))
    address = db.Column(db.String(255))
    worker_position_id = db.Column(db.Integer, db.ForeignKey('worker_position.id'), nullable=False)

    worker_position = db.relationship('WorkerPositionModel', backref='worker')