from db import db

class WorkerPositionModel(db.Model):
    __tablename__ = 'worker_position'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # workers = db.relationship('WorkerModel', backref='worker_position', lazy=True)